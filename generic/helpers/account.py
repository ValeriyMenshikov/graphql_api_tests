class AccountHelper:
    def __init__(self, logic_provider):
        from generic.helpers import LogicProvider
        self.logic_provider: LogicProvider = logic_provider

    def register_user(self, login, email, password):
        self.logic_provider.account_graphql.register_user(
            login=login,
            email=email,
            password=password
        )
        activation_token = self.logic_provider.mailhog.get_token_from_last_email()
        response = self.logic_provider.account_graphql.activate_account(activation_token=activation_token)
        return response
