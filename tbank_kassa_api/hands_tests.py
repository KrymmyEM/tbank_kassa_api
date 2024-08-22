import uuid

from enums import *
from tbank_models import *
from tbank_client import *


if __name__ == "__main__":
    import asyncio
    tc = TClient("TinkoffBankTest", "TinkoffBankTest", False)
    ui = uuid.uuid4()
    inut = Init(
        OrderId = 'test' + str(ui)[5:],
        Amount = 5000,
        Description = "hello",
        CustomerKey = str(ui),
        Recurrent = "Y",
        Receipt = ReceiptFFD105(
            Email = "momotov0292@gmail.com",
            Phone = "+79188814124",
            Taxation = Taxation.OSN,
            Items=[
            ItemFFD105(
                Name = "Test",
                Price = 2500,
                Quantity = 2,
                Tax = Tax.VAT10
            )
        ])
    )

    asyncio.run(tc.send_model(inut))