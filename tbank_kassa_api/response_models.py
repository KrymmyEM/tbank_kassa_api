import json
from types import Optional, Any
from pydantic import BaseModel, constr


class TBankResponse():
    
    def __init__(self, data: Union[str, dict]):
        if isinstance(data, str):
            data = json.loads(data)

        if isinstance(data, dict):
            for key, value in data.items():
                attr_name: str = str(key)
                if attr_name[0].isdigit():
                    attr_name = "I_" + attr_name
                self.__setattr__(attr_name, value)



