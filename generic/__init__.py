from modules import _Provider
from generic.helpers.account import AccountHelper


class LogicProvider:
    def __init__(self):
        self.provider = _Provider()
        self.account_helper = AccountHelper(self)
