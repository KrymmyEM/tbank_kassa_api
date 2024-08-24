import json
from typing import Dict, Any

import aiohttp
from pydantic import BaseModel

from tbank_models import *
from funcs import tokenBuilder


class TClient:
    PRODUCT_URL = "https://securepay.tinkoff.ru/v2/"
    TEST_URL = "https://rest-api-test.tinkoff.ru/v2/"

    def __init__(self, terminalKey: str, password: str, testMode: bool = False):
        if len(terminalKey)  > 20:
            raise ValueError("Terminal key length more than 20")

        self.terminalKey = terminalKey
        self.password = password
        self.workUrl = self.TEST_URL if testMode else self.PRODUCT_URL


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
        data['Token'] = tokenBuilder(self.password, **data)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, data=json.dumps(data)) as response:
                return await response.text()


    async def send_model(self, model: BaseModel):
        payload = model.dict(exclude_none=True)
        payload["TerminalKey"] = self.terminalKey
        payload_keys = payload.keys()

        result = {}

        if isinstance(model, Init):
            result = await self._post("Init", payload)
            
        return result
    

    def pars_notification(self, data: Union[str, dict]):
        if isinstance(data, str):
            data = json.loads(data)

        
        token = tokenBuilder(self.password, **data)

        if data["Token"] != token:
            raise ValueError("Token not valid")

        # Определяем модель на основе наличия уникальных полей
        model = None
        try:
            model = NotificationPayment(**data)
        except:
            pass
        try:
            model = NotificationAddCard(**data)
        except Exception as ex:
            print(ex)
            pass
        try:
            model = NotificationFiscalization(**data)
        except:
            pass
        try:
            model = NotificationQr(**data)
        except:
            pass

        if not model:
            raise ValueError("Неизвестный формат данных")

        return model