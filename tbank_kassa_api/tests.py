import pytest

from tbank_client import TClient

from tbank_models import *

tc = TClient("TinkoffBankTest", "TinkoffBankTest", False)

def test_notification_payment():
    data = {
        "TerminalKey": "TinkoffBankTest",
        "Amount": 100000,
        "OrderId": "21050",
        "Success": True,
        "Status": "CONFIRMED",
        "PaymentId": "13660",
        "ErrorCode": "0",
        "Message": "string",
        "Details": "string",
        "RebillId": 3207469334,
        "CardId": 10452089,
        "Pan": "string",
        "ExpDate": "0229",
        "Token": "6b4f3cc51f5ef0875cd8a1996e6b9a920d024e390f6a999af572d27a08c01b5e",
        "DATA": {
            "Route": "TCB",
            "Source": "Installment",
            "CreditAmount": 10000
        }
    }
    
    model = tc.pars_notification(data)
    assert isinstance(model, NotificationPaymentModel)


def test_notification_add_card():
    data = {
        "TerminalKey": "TinkoffBankTest",
        "CustomerKey": "testCustomer1234",
        "RequestKey": "13021e10-a3ed-4f14-bcd1-823b5ac37390",
        "Success": True,
        "Status": "COMPLETED",
        "PaymentId": "13660",
        "ErrorCode": "0",
        "RebillId": "3207469334",
        "CardId": "10452089",
        "Pan": "string",
        "ExpDate": "0229",
        "Token": "7241ac8307f349afb7bb9dda760717721bbb45950b97c67289f23d8c69cc7b96"
    }
    model = tc.pars_notification(data)
    assert isinstance(model, NotificationAddCardModel)


def test_notification_fiscalization():
    data = {
        "TerminalKey": "TinkoffBankTest",
        "OrderId": "21050",
        "Success": True,
        "Status": "RECEIPT",
        "PaymentId": "13660",
        "ErrorCode": "0",
        "ErrorMessage": "string",
        "Amount": 100000,
        "FiscalNumber": 0,
        "ShiftNumber": 0,
        "ReceiptDatetime": "string",
        "FnNumber": "string",
        "EcrRegNumber": "string",
        "FiscalDocumentNumber": 0,
        "FiscalDocumentAttribute": 0,
        "Receipt": {
        "FfdVersion": "string",
        "ClientInfo": {
        "Birthdate": "string",
        "Citizenship": "string",
        "DocumentСode": "21",
        "DocumentData": "string",
        "Address": "string"
        },
        "Taxation": "osn",
        "Email": "a@test.ru",
        "Phone": "+79031234567",
        "Customer": "string",
        "CustomerInn": "string",
        "Items": [],
        "Payments": [
        {
        "Cash": 90000,
        "Electronic": 50000,
        "AdvancePayment": 0,
        "Credit": 0,
        "Provision": 0
        }
        ]
        },
        "Type": "string",
        "Token": "1268613448ca58be8b19c68a0de4f7289f11f186e4920dfcaf085a5f9cdfd660",
        "Ofd": "string",
        "Url": "string",
        "QrCodeUrl": "string",
        "CalculationPlace": "string",
        "CashierName": "string",
        "SettlePlace": "string"
    }
    model = tc.pars_notification(data)
    assert isinstance(model, NotificationFiscalizationModel)


def test_notification_qr():
    data = {
        "TerminalKey": "TinkoffBankTest",
        "RequestKey": "13021e10-a3ed-4f14-bcd1-823b5ac37390",
        "AccountToken": "70LSS7DN18SJQRS10006DNPKLJL24B05",
        "BankMemberId": "5555",
        "BankMemberName": "string",
        "NotificationType": "LINKACCOUNT",
        "Success": True,
        "ErrorCode": "0",
        "Message": "string",
        "Token": "871199b37f207f0c4f721a37cdcc71dfcea880b4a4b85e3cf852c5dc1e99a8d6",
        "Status": "ACTIVE"
    }
    model = tc.pars_notification(data)
    assert isinstance(model, NotificationQrModel)


def test_invalid_notification():
    data = {
        "InvalidKey": "InvalidValue"
    }
    with pytest.raises(ValueError):
        tc.pars_notification(data)


if __name__ == "__main__":
    test_notification_payment()