from pydantic import BaseModel, Field, constr, conlist, conint, root_validator
from typing import List, Optional, Union

from tbank_kassa_api.tbank_models import Shop, ReceiptFFD105, ReceiptFFD12
from tbank_kassa_api.enums import PayType

class Init(BaseModel):
    OrderId: constr(max_length=36)
    Amount: int
    Description: Optional[constr(max_length=250)] = None
    CustomerKey: Optional[constr(max_length=36)] = None
    Recurrent: Optional[constr(max_length=1)] = None
    PayType: Optional[PayType] = None
    Language: Optional[constr(max_length=2)] = None
    NotificationURL: Optional[str] = None
    SuccessURL: Optional[str] = None
    FailURL: Optional[str] = None
    RedirectDueDate: Optional[str] = None
    DATA: Optional[dict] = None
    Receipt: Union[ReceiptFFD105, ReceiptFFD12] = None
    Shops: Optional[List[Shop]] = None

    @root_validator(pre=True)
    def check_fields(cls, values):
        customer_key = values.get("CustomerKey")
        recurrent = values.get("Recurrent")

        if recurrent and not customer_key:
            raise ValueError("CustomerKey is required with Recurrent")

        amount = values.get("Amount")
        receipt = values.get("Receipt")
        
        if receipt:
            true_amount: int = 0
            for item in receipt.Items:
                true_amount += item.Amount

            if true_amount != amount:
                raise ValueError("Amount does not equal the sum of the Amount of items")

        return values


