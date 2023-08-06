from functools import cached_property


class LogicProvider:

    @cached_property
    def provider(self):
        from modules import modules_provider
        return modules_provider()

    @cached_property
    def account_helper(self):
        from generic.helpers.account import AccountHelper
        return AccountHelper(self)
