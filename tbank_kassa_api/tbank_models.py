from pydantic import BaseModel, Field, constr, conlist, conint, root_validator
from typing import List, Optional, Union

from enums import *

class AgentData(BaseModel):
    AgentSign: AgentSign
    OperationName: Optional[constr(max_length=64)] = None
    Phones: Optional[conlist(constr(min_length=1, max_length=19), min_length=1)] = None
    ReceiverPhones: Optional[conlist(constr(min_length=1, max_length=19), min_length=1)] = None
    TransferPhones: Optional[conlist(constr(min_length=1, max_length=19), min_length=1)] = None
    OperatorName: Optional[constr(max_length=64)] = None
    OperatorAddress: Optional[constr(max_length=243)] = None
    OperatorINN: Optional[constr(max_length=12)] = None

    @root_validator(pre=True)
    def check_required_fields(cls, values):
        agent_sign = values.get('AgentSign')
        if agent_sign in {AgentSign.BANK_PAYING_AGENT, AgentSign.BANK_PAYING_SUBAGENT}:
            if values.get('OperationName') is None:
                raise ValueError("OperationName is required when AgentSign is bank_paying_agent or bank_paying_subagent")
            if values.get('Phones') is None and values.get('TransferPhones') is None:
                raise ValueError("Phones or TransferPhones is required when AgentSign is bank_paying_agent or bank_paying_subagent")
        if agent_sign in {AgentSign.PAYING_AGENT, AgentSign.PAYING_SUBAGENT}:
            if values.get('Phones') is None or values.get('ReceiverPhones') is None:
                raise ValueError("Phones and ReceiverPhones are required when AgentSign is paying_agent or paying_subagent")
        if agent_sign in {AgentSign.BANK_PAYING_AGENT, AgentSign.BANK_PAYING_SUBAGENT}:
            if values.get('OperatorName') is None or values.get('OperatorAddress') is None:
                raise ValueError("OperatorName and OperatorAddress are required when AgentSign is bank_paying_agent or bank_paying_subagent")
        if agent_sign in {AgentSign.BANK_PAYING_AGENT, AgentSign.BANK_PAYING_SUBAGENT}:
            if values.get('OperatorName') is None or values.get('OperatorINN') is None:
                raise ValueError("OperatorName and OperatorINN are required when AgentSign is bank_paying_agent or bank_paying_subagent")
        return values


class SupplierInfo(BaseModel):
    Phones: conlist(constr(pattern=r'^\+\d{1,19}$'), min_length=1, max_length=19) 
    Name: constr(max_length=239)
    INN: constr(pattern=r'^\d{10,12}$')


class MarkCode(BaseModel):
    MarkCodeType: MarkCodeType
    Value: str


class MarkQuantity(BaseModel):
    Numerator: int
    Denominator: int


class SectoralItemProps(BaseModel):
    FederalID: str
    Date: str
    Number: str
    Value: str


class ItemBase(BaseModel):
    Name: constr(max_length=128)
    Price: int
    Quantity: int
    Amount: int
    PaymentMethod: PaymentMethods = PaymentMethods.FULL_PAYMENT
    PaymentObject: Optional[PaymentObject] = None
    Tax: Tax
    AgentData: Optional[AgentData] = None
    SupplierInfo: Optional[SupplierInfo] = None

    @root_validator(pre=True)
    def check_fields(cls, values):
        amount = values.get("Amount")
        quantity = values.get("Quantity")
        price = values.get("Price")

        if (quantity * price) != amount:
            values["Amount"] = quantity * price
        
        agent_data = values.get("AgentData")
        if agent_data and not values.get("SupplierInfo"):
            raise ValueError("SupplierInfo is required with AgentData")

        return values


class ItemFFD105(ItemBase):
    Ean13: Optional[constr(max_length=300)] = None
    ShopCode: Optional[str] = None


class ItemFFD12(ItemBase):
    MeasurementUnit: str
    UserData: Optional[str] = None
    Excise: Optional[str] = None
    CountryCode: Optional[constr(max_length=3)] = None
    DeclarationNumber: Optional[str] = None
    MarkProcessingMode: Optional[str] = None
    MarkCode: Optional[MarkCode] = None
    MarkQuantity: Optional[MarkQuantity] = None
    SectoralItemProps: Optional[SectoralItemProps] = None


class Payments(BaseModel):
    Cash: Optional[int] = None
    Electronic: int
    AdvancePayment: Optional[int] = None
    Credit: Optional[int] = None
    Provision: Optional[int] = None


class ClientInfo(BaseModel):
    Birthdate: Optional[str] = None
    Citizenship: Optional[str] = None
    DocumentCode: Optional[str] = None
    DocumentData: Optional[str] = None
    Address: Optional[str] = None


class Shop(BaseModel):
    ShopCode: str
    Amount: int
    Name: Optional[constr(max_length=128)]
    Fee: str


class ReceiptBase(BaseModel):
    Email: Optional[constr(max_length=128)] = None
    Phone: Optional[constr(max_length=64)] = None
    Taxation: Taxation
    Payments: Optional[Payments] = None


class ReceiptFFD105(ReceiptBase):
    FfdVersion: str = "1.05"
    Items: List[ItemFFD105]


class ReceiptFFD12(ReceiptBase):
    FfdVersion: str = "1.2"
    Items: List[ItemFFD12]
    Customer: Optional[str] = None
    CustomerINN: Optional[constr(max_length=12)] = None


class Init(BaseModel):
    OrderId: constr(max_length=36)
    Amount: int
    Description: Optional[constr(max_length=250)] = None
    CustomerKey: Optional[constr(max_length=36)] = None
    Ecurrent: Optional[constr(max_length=1)] = None
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
        recurrent = values.get("Ecurrent")

        if recurrent and not customer_key:
            raise ValueError("CustomerKey is required with Ecurrent")

        amount = values.get("Amount")
        receipt = values.get("Receipt")
        
        if receipt:
            true_amount: int = 0
            for item in receipt.Items:
                true_amount += item.Amount

            if true_amount != amount:
                raise ValueError("Amount does not equal the sum of the Amount of items")

        return values

    