from enum import StrEnum, Enum


class PayType(StrEnum):
    O = "O"  # Означает оплату одним платежом
    T = "T"  # Означает оплату частями


class Tax(StrEnum):
    NONE = "none"
    VAT0 = "vat0"
    VAT10 = "vat10"
    VAT20 = "vat20"
    VAT110 = "vat110"
    VAT120 = "vat120"


class Taxation(StrEnum):
    OSN = "osn"  # Общая система налогообложения
    USN_INCOME = "usn_income"  # Упрощенная система (доходы)
    USN_INCOME_OUTCOME = "usn_income_outcome"  # Упрощенная система (доходы минус расходы)
    ENVD = "envd"  # Единый налог на вменённый доход
    ESN = "esn"  # Единый сельскохозяйственный налог
    PATENT = "patent"  # Патентная система налогообложения


class AgentSign(StrEnum):
    BANK_PAYING_AGENT = "bank_paying_agent"  # Банковский платежный агент
    BANK_PAYING_SUBAGENT = "bank_paying_subagent"  # Банковский платежный субагент
    PAYING_AGENT = "paying_agent"  # Платежный агент
    PAYING_SUBAGENT = "paying_subagent"  # Платежный субагент
    ATTORNEY = "attorney"  # Поверенный
    COMMISSION_AGENT = "commission_agent"  # Комиссионер
    ANOTHER = "another"  # Другой тип агента


class PaymentMethods(StrEnum):
    FULL_PREPAYMENT = "full_prepayment"
    PREPAYMENT = "prepayment"
    ADVANCE = "advance"
    FULL_PAYMENT = "full_payment"
    PARTIAL_PAYMENT = "partial_payment"
    CREDIT = "credit"
    CREDIT_PAYMENT = "credit_payment"


class PaymentObject(str, Enum):
    COMMODITY = "commodity"
    EXCISE = "excise"
    JOB = "job"
    SERVICE = "service"
    GAMBLING_BET = "gambling_bet"
    GAMBLING_PRIZE = "gambling_prize"
    LOTTERY = "lottery"
    LOTTERY_PRIZE = "lottery_prize"
    INTELLECTUAL_ACTIVITY = "intellectual_activity"
    PAYMENT = "payment"
    AGENT_COMMISSION = "agent_commission"
    COMPOSITE = "composite"
    ANOTHER = "another"
    CONTRIBUTION = "contribution"
    PROPERTY_RIGHTS = "property_rights"
    UNREALIZATION = "unrealization"
    TAX_REDUCTION = "tax_reduction"
    TRADE_FEE = "trade_fee"
    RESORT_TAX = "resort_tax"
    PLEDGE = "pledge"
    INCOME_DECREASE = "income_decrease"
    IE_PENSION_INSURANCE_WITHOUT_PAYMENTS = "ie_pension_insurance_without_payments"
    IE_PENSION_INSURANCE_WITH_PAYMENTS = "ie_pension_insurance_with_payments"
    IE_MEDICAL_INSURANCE_WITHOUT_PAYMENTS = "ie_medical_insurance_without_payments"
    IE_MEDICAL_INSURANCE_WITH_PAYMENTS = "ie_medical_insurance_with_payments"
    SOCIAL_INSURANCE = "social_insurance"
    CASINO_CHIPS = "casino_chips"
    AGENT_PAYMENT = "agent_payment"
    EXCISABLE_GOODS_WITHOUT_MARKING_CODE = "excisable_goods_without_marking_code"
    EXCISABLE_GOODS_WITH_MARKING_CODE = "excisable_goods_with_marking_code"
    GOODS_WITHOUT_MARKING_CODE = "goods_without_marking_code"
    GOODS_WITH_MARKING_CODE = "goods_with_marking_code"


class MarkCodeType(StrEnum):
    UNKNOWN = "UNKNOWN"
    EAN8 = "EAN8"
    EAN13 = "EAN13"
    ITF14 = "ITF14"
    GS10 = "GS10"
    GS1M = "GS1M"
    SHORT = "SHORT"
    FUR = "FUR"
    EGAIS20 = "EGAIS20"
    EGAIS30 = "EGAIS30"
    RAWCODE = "RAWCODE"


class PaymentStatus(StrEnum):
    AUTHORIZED = "AUTHORIZED"
    CONFIRMED = "CONFIRMED"
    PARTIAL_REVERSED = "PARTIAL_REVERSED"
    REVERSED = "REVERSED"
    PARTIAL_REFUNDED = "PARTIAL_REFUNDED"
    REFUNDED = "REFUNDED"
    REJECTED = "REJECTED"
    DEADLINE_EXPIRED = "DEADLINE_EXPIRED"


class AddCardStatus(StrEnum):
    COMPLETED = "COMPLETED"
    REJECTED = "REJECTED"