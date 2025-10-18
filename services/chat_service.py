from datetime import datetime, timezone
import json
from typing import List
from fastapi import HTTPException, status
from requests import Session

from models.conversation import Conversation
from models.message import Message
from providers.gemini_provider import GeminiProvider
from providers.openai_provider import OpenaiProvider
from schemas.chat import ChatRequest, ChatResponse
from schemas.conversation import ConversationCreate
from schemas.message import MessageCreate
from services.database_service import database_service
from services.ai_model_service import ai_model_service
from services.parameter_service import parameter_service
from services.conversation_service import conversation_service
from services.message_service import message_service

class ChatService:
    def __init__(self):
        self.database_service = database_service
        self.ai_model_service = ai_model_service
        self.parameter_service = parameter_service
        self.conversation_service = conversation_service
        self.message_service = message_service
    
    async def send(self, db: Session, request: ChatRequest):
        conversation = self._update_conversation(db, request)

        try:
            if not self.database_service.exists(db=db, id= request.database_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Database não encontrado"
                )

            database_schema = self.database_service.get_database_schema_json(
                db=db, 
                database_id=request.database_id
            )

            json_string = database_schema.model_dump_json(indent=2, exclude_none=True)

            prompt = self._build_prompt(db, json_string,request.prompt)

            # _process_with_ai is async — await it so execution completes before returning
            response = await self._process_with_ai(db, request.ai_model_id, conversation.id, prompt)

            # _process_with_ai already returns a ChatResponse
            return response
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Erro ao processar chat: {str(e)}"
            )

    def _build_prompt(self, db: Session, database_schema, message) -> str:
        parameter = parameter_service.get_by_code(db=db, code="001")

        if not parameter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Parâmetro não encontrado"
            )
        
        prompt_template = parameter.value
        prompt_template = prompt_template.replace("{SCHEMA_DATABASE}", database_schema)
        prompt_template = prompt_template.replace("{PROMPT}", message)

        return prompt_template

    async def _process_with_ai(self, db: Session, ai_model_id: int, conversation_id: int, prompt: str):
        ai_model = ai_model_service.get(db, ai_model_id)

        if not ai_model:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Modelo de IA não encontrado"
            )
        
        messages = self._messages_to_dict(self.message_service.get_by_conversation_id(db, conversation_id))
        response = ""
        
        try:
            configs = json.loads(ai_model.configs)

            if ai_model.type == "CHATGPT":
                provider = OpenaiProvider()
            elif ai_model.type == "GEMINI":
                provider = GeminiProvider()
            elif ai_model.type == "CLAUDE":
                provider = GeminiProvider()
            elif ai_model.type == "DEEPSEEK":
                provider = GeminiProvider()
            else:
                provider = None

            response = await provider.generate_text(
                prompt=prompt,
                messages=messages,
                configs=configs
            )

            # Atualiza a mensagem no banco de dados
            self._update_message(db, conversation_id, response, ai_model.type)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Falha ao tentar obter configurações do modelo de IA"
            )

        return ChatResponse(message=response)

    def _update_conversation(
        self,
        db: Session,
        request: ChatRequest
    ) -> Conversation:
        parameter = parameter_service.get_by_code(db=db, code="002")

        if not parameter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Parâmetro 002 não encontrado"
            )
        
        now = datetime.now(timezone.utc)
        
        if request.conversation_id:
            conversation = self.conversation_service.get(db, request.conversation_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Conversa {request.conversation_id} não encontrada"
                )
        else:
            title = request.prompt[:50] + "..." if len(request.prompt) > 50 else request.prompt
            conversation = self.conversation_service.create(
                db,
                ConversationCreate(
                    title=title,
                    created_at=now,
                    is_favorite=False
                )
            )
        
            self.message_service.create(
                db,
                MessageCreate(
                    text=parameter.value,
                    created_at=now,
                    agent="system",
                    conversation_id=conversation.id
                )
            )

        self.message_service.create(
            db,
            MessageCreate(
                text=request.prompt,
                created_at=now,
                agent="user",
                conversation_id=conversation.id
            )
        )
        
        return conversation

    def _update_message(self, db: Session, conversation_id: int, message: str, ai_model: str):
        now = datetime.now(timezone.utc)

        if ai_model == "CHATGPT":
            agent = "assistant"
        elif ai_model == "GEMINI":
            agent = "model"
        elif ai_model == "CLAUDE":
            agent = ""
        elif ai_model == "DEEPSEEK":
            agent = ""
        else:
            agente = ""

        self.message_service.create(
            db,
            MessageCreate(
                text=message,
                created_at=now,
                agent=agent,
                conversation_id=conversation_id
            )
        )

    def _messages_to_dict(self, messages: List[Message]):
        return [{"role": msg.agent.lower(), "content": msg.text} for msg in messages]

chat_service = ChatService()
