class AccountHelper:
    def __init__(self, logic_provider):
        from generic import LogicProvider
        self.logic_provider: LogicProvider = logic_provider
        self.graphql_account = self.logic_provider.provider.graphql.dm_api_account
        self.mailhog_api = self.logic_provider.provider.http.mailhog

    def register_account(self, login, email, password):
        self.graphql_account.register_account(
            login=login,
            email=email,
            password=password
        )
        activation_token = self.mailhog_api.get_token_from_last_email()
        response = self.graphql_account.activate_account(
            activation_token=activation_token)
        return response
