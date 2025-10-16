from typing import Any, Dict, List

from google import genai
from google.genai import types
from providers.base_provider import AIProvider

class GeminiProvider(AIProvider):
    def __init__(self, max_chunk_size: int = 4000):
        super().__init__(max_chunk_size)

    async def generate_text(
        self, 
        prompts: str, 
        messages: List[Dict[str, str]], 
        configs: Dict[str, Any]
    ) -> str:
        self._validate_configs(configs)
        
        api_key = configs["api_key"]
        model_name = configs["model_name"]

        client = genai.Client(api_key=api_key)

        history = self._prepare_messages(messages)
        
        chat = client.chats.create(model=model_name, history=history)
        
        response = chat.send_message(prompts)

        return response.text

    def _validate_configs(self, configs: Dict[str, Any]) -> None:
        """Valida as configurações obrigatórias."""
        required_fields = {
            "api_key": "API key",
            "model_name": "Model name"
        }
        
        for field, name in required_fields.items():
            if not configs.get(field):
                raise ValueError(f"{name} é obrigatório para o OpenAI")

    def _prepare_messages(
        self, 
        messages: List[Dict[str, str]], 
    ) -> List[Dict[str, str]]:
        history = []
        
        if messages and len(messages) > 0:
            for message in messages:
                history.append(types.Content(role=message["role"], parts=[types.Part.from_text(message[""])]))
        
        return history
