def test_register_user(prepare_user, graphql_account_api):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    graphql_account_api.register_user(login=login, email=email, password=password)

    # TODO разобраться с полями и перенести в класс АПИ
    def accounts(
            self,
            accounts_fields: str | tuple = AccountsResponse.__field_names__,
            users_fields: str | tuple = GeneralUser.__field_names__,
            with_inactive=True,
    ) -> AccountsResponse | dict:

        print('!!!!', accounts_fields)
        print('!!!!', users_fields)
        query_name = 'accounts'
        query_request = self.client.query(name=query_name)
        query = PagingQueryInput(
            skip=0,
            number=0,
            size=10
        )
        query_request.accounts.__fields__('users')
        query_request.accounts.users.__fields__('user_id')
        query_request.accounts(paging=query, with_inactive=with_inactive)
        response = self.client.request(query=query_request)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUserDetails
        )
        return response