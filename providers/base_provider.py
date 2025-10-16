from abc import ABC, abstractmethod
from typing import List, Dict, Any
from openai import OpenAI


class AIProvider(ABC):
    def __init__(self, max_chunk_size: int = 4000):
        self.max_chunk_size = max_chunk_size

    @abstractmethod
    async def generate_text(self, prompts: str, messages: List[Dict[str, str]], configs: Dict[str, Any]) -> str:
        pass

    def split_prompt_into_chunks(self, prompt: str) -> List[str]:
        """Divide prompt em chunks menores baseado no max_chunk_size."""
        if len(prompt) <= self.max_chunk_size:
            return [prompt]
        
        chunks = []
        words = prompt.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_length = len(word) + 1  # +1 para espaço
            if current_length + word_length > self.max_chunk_size and current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = [word]
                current_length = word_length
            else:
                current_chunk.append(word)
                current_length += word_length
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    async def generate_text_in_chunks(
        self, 
        prompt: str, 
        messages: List[Dict[str, str]], 
        configs: Dict[str, Any]
    ) -> str:
        """
        Gera texto dividindo o prompt em chunks se necessário.
        
        Args:
            prompt: Texto do prompt atual
            messages: Histórico de mensagens
            configs: Configurações da API
            
        Returns:
            Resposta consolidada
        """
        chunks = self.split_prompt_into_chunks(prompt)
        
        # Se couber em um chunk, envia normalmente
        if len(chunks) == 1:
            return await self.generate_text(prompt, messages, configs)
        
        # Processa múltiplos chunks
        responses = []
        for i, chunk in enumerate(chunks):
            # Adiciona contexto sobre qual parte está sendo processada
            chunk_prompt = f"[Parte {i+1}/{len(chunks)}]\n\n{chunk}"
            response = await self.generate_text(chunk_prompt, messages, configs)
            responses.append(response)
        
        # Consolida todas as respostas
        consolidated = "\n\n".join(responses)
        return consolidated
