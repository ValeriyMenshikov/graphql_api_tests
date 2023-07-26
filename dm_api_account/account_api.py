from typing import Union, Tuple

from sgqlc.types import ContainerTypeMeta
from schema.dm_api_schema import (
    dm_api_schema,
    RegistrationInput,
    AccountRegisterResponse,
    Mutation,
    Query,
    EnvelopeOfUserDetails,
    EnvelopeOfUser,
    LoginCredentialsInput,
    AccountLoginResponse,
    PagingQueryInput,
    AccountsResponse
)
from graphql_client.client import GraphQLClient


class GraphQLAccountApi:
    def __init__(
            self,
            service_name: str = '',
            endpoint: str = "/graphql/",
            disable_log: bool = False,
            base_headers: dict = None
    ):
        self.client = GraphQLClient(
            service_name=service_name,
            endpoint=endpoint,
            disable_log=disable_log,
            base_headers=base_headers,
            schema=dm_api_schema
        )

    def register_user(self, login=None, email=None, password=None) -> AccountRegisterResponse:
        mutation_request = self.client.mutation(name='registerAccount')
        registration_input = RegistrationInput(
            login=login,
            email=email,
            password=password,
        )
        mutation_request.register_account(registration=registration_input)
        json_data = self.client.request(query=mutation_request)["data"]["registerAccount"]
        result = AccountRegisterResponse(json_data)
        return result

    @staticmethod
    def _convert_to_model(response: dict, query_name: str, model: ContainerTypeMeta):
        """

        :param response: GraphQL response
        :param query_name: mutation or query name
        :param model: GraphQL response model from schema
        :return:
        """
        json_data = response.get('data', {}).get(query_name)
        if json_data:
            return model(json_data)
        return response

    def account_current(self, access_token) -> EnvelopeOfUserDetails | dict:
        query_name = 'accountCurrent'
        query_request = self.client.query(name=query_name)
        query_request.account_current(access_token=access_token)
        response = self.client.request(query=query_request)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUserDetails
        )
        return response

    def accounts(
            self,
            accounts_fields: AccountsResponse.__field_names__ = AccountsResponse.__field_names__,
            with_inactive=True,

    ) -> AccountsResponse | dict:
        query_name = 'accounts'
        query_request = self.client.query(name=query_name)
        query = PagingQueryInput(
            skip=0,
            number=0,
            size=10
        )
        query_request.accounts(paging=query, with_inactive=with_inactive)
        # TODO разобраться с полями и перенести в класс АПИ

        query_request.accounts.__fields__('users')
        query_request.accounts.users.__fields__('user_id')
        response = self.client.request(query=query_request)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUserDetails
        )
        return response

    def activate_account(self, activation_token) -> EnvelopeOfUser | dict:
        query_name = 'activateAccount'
        mutation_request = self.client.mutation(name=query_name)
        mutation_request.activate_account(activation_token=activation_token)
        response = self.client.request(query=mutation_request)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUser
        )
        return response

    def login_account(self, login, password, remember_me) -> AccountLoginResponse | dict:
        query_name = 'loginAccount'
        mutation_request = self.client.mutation(name=query_name)
        login_credentials_input = LoginCredentialsInput(
            login=login,
            password=password,
            remember_me=remember_me
        )
        mutation_request.login_account(login=login_credentials_input)
        response = self.client.request(query=mutation_request)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=AccountLoginResponse
        )
        return response
