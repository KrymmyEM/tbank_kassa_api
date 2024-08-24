try:
    import pytest
except Exception:
    pass
import hashlib

from tbank_client import TClient

from tbank_kassa_api.tbank_models import *
from tbank_kassa_api.enums import *

tc = TClient("TinkoffBankTest", "TinkoffBankTest", False)