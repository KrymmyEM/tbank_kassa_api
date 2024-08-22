import json
import hashlib
from typing import Dict, Any

import aiohttp
from pydantic import BaseModel

from tbank_models import *


class TClient:
    PRODUCT_URL = "https://securepay.tinkoff.ru/v2/"
    TEST_URL = "https://rest-api-test.tinkoff.ru/v2/"

    def __init__(self, terminalKey: str, password: str, testMode: bool = False):
        if len(terminalKey)  > 20:
            raise ValueError("Terminal key length more than 20")

        self.terminalKey = terminalKey
        self.password = password
        self.workUrl = self.TEST_URL if testMode else self.PRODUCT_URL

    
    def _tokenGenerator(self, **kwargs):
        token_params = {key: value for key, value in kwargs.items() if not isinstance(value, dict)}
        token_params['Password'] = self.password
        sorted_params = sorted(token_params.keys())
        concatenated_string = ''
        for param in sorted_params:
            data = token_params[param]
            if data:
                concatenated_string += str(data)
        token = hashlib.sha256(concatenated_string.encode('utf-8')).hexdigest()
        return token

    def _keyToCamelCase(self, key):
        parts = key.split('_')
        camel_case_key = ''.join(part.capitalize() for part in parts)
        return camel_case_key

    
    def to_camel_case(self, key):
        parts = key.split('_')
        camel_case_key = ''.join(part.capitalize() for part in parts)
        return camel_case_key


    def convert_kwargs_to_camel_case(self, kwargs):
        return {self.to_camel_case(k): v for k, v in kwargs.items()}



    def _checkRequiredKeys(required_keys: list, payload_keys: list):
        for key in payload_keys:
            if key not in required_keys:
                return False

        return True

    async def _post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Выполнение POST-запроса к API.
        """
        url = self.workUrl + endpoint
        headers = {'Content-Type': 'application/json'}
        
        # Генерация токена
        data['Token'] = self._tokenGenerator(**data)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as response:
                return await response.text()


    async def send_model(self, model: BaseModel):
        payload = model.dict(exclude_none=True)
        payload["TerminalKey"] = self.terminalKey
        payload_keys = payload.keys()

        if isinstance(model, Init):
            result = await self._post("Init", payload)
            print(result)
    
