from pydantic import BaseModel, Field, constr, conlist, conint, root_validator
from typing import List, Optional, Union

from tbank_kassa_api.enums import *
from tbank_kassa_api.enums import PaymentObject

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
    PaymentObject: str = PaymentObject.COMMODITY
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
    


class ReceiptFFD105(ReceiptBase):
    FfdVersion: str = "1.05"
    Items: List[ItemFFD105]
    Payments: Optional[Payments] = None


class ReceiptFFD105_2(ReceiptBase):
    FfdVersion: str = "1.05"
    Items: List[ItemFFD105]
    Payments: Optional[List[Payments]]


class ReceiptFFD12(ReceiptBase):
    FfdVersion: str = "1.2"
    Items: List[ItemFFD12]
    ClientInfo: Optional[ClientInfo] = None
    Customer: Optional[str] = None
    CustomerINN: Optional[constr(max_length=12)] = None
    Payments: Optional[Payments] = None


class ReceiptFFD12_2(ReceiptBase):
    FfdVersion: str = "1.2"
    Items: List[ItemFFD12]
    ClientInfo: Optional[ClientInfo]
    Customer: Optional[str] = None
    CustomerINN: Optional[constr(max_length=12)] = None
    Payments: Optional[List[Payments]]


class NotificationBase(BaseModel):
    TerminalKey: constr(max_length=20) = Field(..., description="Идентификатор терминала. Выдается Мерчанту Т‑Кассой при заведении терминала")
    Success: bool = Field(..., description="Успешность прохождения запроса (true/false)")
    ErrorCode: constr(max_length=20) = Field(..., description="Код ошибки. '0' в случае успеха")
    Message: Optional[str] = Field(None, description="Краткое описание ошибки")
    Token: str = Field(..., description="Токен")
    Status: PaymentStatus
    

class NotificationPayment(NotificationBase):
    Amount: conint(le=10**10) = Field(..., description="Сумма в копейках")
    OrderId: constr(max_length=36) = Field(..., description="Идентификатор заказа в системе Мерчанта")
    PaymentId: conint(le=10**20) = Field(..., description="Уникальный идентификатор транзакции в системе Т‑Кассы")
    Details: Optional[str] = Field(None, description="Подробное описание ошибки")
    RebillId: Optional[conint(le=10**20)] = Field(None, description="Идентификатор автоплатежа")
    CardId: Optional[int] = Field(None, description="Идентификатор карты в системе Т‑Кассы")
    Pan: Optional[str] = Field(None, description="Замаскированный номер карты/Замаскированный номер телефона")
    ExpDate: Optional[constr(pattern=r"^\d{4}$")] = Field(None, description="Срок действия карты в формате MMYY")
    

    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        use_enum_values = True


class NotificationAddCard(NotificationBase):
    CustomerKey: constr(max_length=36) = Field(..., description="Идентификатор клиента в системе Мерчанта")
    RequestKey: constr(pattern=r'^[a-f0-9\-]{36}$') = Field(..., description="Идентификатор запроса на привязку карты")
    Status: AddCardStatus = Field(..., description="Статус привязки карты")
    PaymentId: constr(max_length=20) = Field(..., description="Идентификатор платежа в системе Т‑Кассы")
    RebillId: constr(max_length=20) = Field(..., description="Идентификатор автоплатежа")
    CardId: constr(max_length=20) = Field(..., description="Идентификатор карты в системе Т‑Кассы")
    Pan: str = Field(..., description="Замаскированный номер карты")
    ExpDate: str = Field(..., description="Срок действия карты В формате MMYY")


class NotificationFiscalization(NotificationBase):
    OrderId: constr(max_length=36) = Field(..., description="Идентификатор заказа в системе Мерчанта")
    Status: str = Field("RECEIPT", description="Статус фискализации")
    PaymentId: constr(max_length=20) = Field(..., description="Идентификатор платежа в системе Т‑Кассы")
    ErrorMessage: Optional[str] = Field(None, description="Описание ошибки")
    Amount: int = Field(..., description="Сумма в копейках")
    FiscalNumber: int = Field(..., description="Номер чека в смене")
    ShiftNumber: int = Field(..., description="Номер смены")
    ReceiptDatetime: str = Field(..., description="Дата и время документа из ФН")
    FnNumber: str = Field(..., description="Номер ФН")
    EcrRegNumber: str = Field(..., description="Регистрационный номер ККТ")
    FiscalDocumentNumber: int = Field(..., description="Фискальный номер документа")
    FiscalDocumentAttribute: int = Field(..., description="Фискальный признак документа")
    Type: str = Field(..., description="Признак расчета")
    Ofd: Optional[str] = Field(None, description="Наименование оператора фискальных данных")
    Url: Optional[str] = Field(None, description="URL адрес с копией чека")
    QrCodeUrl: Optional[str] = Field(None, description="URL адрес с QR кодом для проверки чека в ФНС")
    CalculationPlace: Optional[str] = Field(None, description="Место осуществления расчетов")
    CashierName: Optional[str] = Field(None, description="Имя кассира")
    SettlePlace: Optional[str] = Field(None, description="Место нахождения (установки) ККМ")



    @root_validator(pre=True)
    def check_fields(cls, values):
        receipt = values.get("Receipt")

        ffd_version = receipt.get("FfdVersion")

        if "ClientInfo" in receipt or ffd_version == "1.2":
            values["Receipt"] = ReceiptFFD12_2(**receipt)
        
        else:
            values["Receipt"] = ReceiptFFD105_2(**receipt)


        return values


class NotificationQr(NotificationBase):
    RequestKey: constr(pattern=r'^[a-f0-9\-]{36}$') = Field(..., description="Идентификатор запроса на привязку счета")
    AccountToken: str = Field(..., description="Идентификатор привязки счета")
    BankMemberId: Optional[str] = Field(None, description="Идентификатор банка-эмитента клиента")
    BankMemberName: Optional[str] = Field(None, description="Наименование банка-эмитента")
    NotificationType: str = Field("LINKACCOUNT", description="Тип нотификации")
    Status: str = Field(..., description="Статус привязки")


if __name__ == "__main__":
    item = ItemFFD105(
                Name = "Услуга химчистки",
                Price = 1000,
                Quantity = 1,
                PaymentMethod = PaymentMethods.FULL_PAYMENT,
                PaymentObject = PaymentObject.SERVICE,
                Tax = Tax.NONE
            )
        
    print(item)