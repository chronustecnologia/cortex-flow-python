from typing import Any, Dict, List

from openai import OpenAI
from providers.base_provider import AIProvider


class OpenaiProvider(AIProvider):
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
        temperature = configs["temperature"]
        max_tokens = configs["max_tokens"]

        client = OpenAI(api_key=api_key)

        messages_list = self._prepare_messages(messages, prompts)
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages_list,
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content

    def _validate_configs(self, configs: Dict[str, Any]) -> None:
        required_fields = {
            "api_key": "API key",
            "model_name": "Model name",
            "temperature": "Temperature",
            "max_tokens": "Max tokens"
        }
        
        for field, name in required_fields.items():
            if not configs.get(field):
                raise ValueError(f"{name} é obrigatório para o OpenAI")

    def _prepare_messages(
        self, 
        messages: List[Dict[str, str]], 
        current_prompt: str
    ) -> List[Dict[str, str]]:
        messages_list = []
        
        if messages and len(messages) > 0:
            messages_list.extend(messages)
        
        messages_list.append({"role": "user", "content": current_prompt})
        
        return messages_list
