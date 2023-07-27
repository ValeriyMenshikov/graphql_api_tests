from sgqlc.types import ContainerTypeMeta
from apis.dm_api_account.graphql.schema.schema import (
    schema,
    RegistrationInput,
    AccountRegisterResponse,
    EnvelopeOfUserDetails,
    EnvelopeOfUser,
    LoginCredentialsInput,
    AccountLoginResponse,
    PagingQueryInput,
    AccountsResponse,
    GeneralUser,
    PagingResult
)
from commons.graphql_client.client import GraphQLClient


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
            schema=schema
        )

    def register_user(self, login: str, email: str, password: str) -> AccountRegisterResponse:
        """
        Регистрация пользователя.
        :param login:
        :param email:
        :param password:
        :return:
        """
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
        Метод преобразует json dict ответ в соответсвующую ResponseModel, в противном случае отдает
        полный json dict
        :param response: GraphQL response
        :param query_name: mutation or query name
        :param model: GraphQL response model from schema
        :return:
        """
        json_data = response.get('data', {}).get(query_name)
        if json_data:
            return model(json_data)
        return response

    def account_current(self, access_token: str) -> EnvelopeOfUserDetails | dict:
        """
        Получение текущего пользователя.
        :param access_token:
        :return:
        """
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
            accounts_fields: tuple[AccountsResponse.__field_names__] = (),
            users_fields: tuple[GeneralUser.__field_names__] = (),
            paging_fields: tuple[PagingResult.__field_names__] = (),
            skip: int = 0,
            number: int = 0,
            size: int = 10,
            with_inactive: bool = True,
    ) -> AccountsResponse | dict:
        """
        Метод получения списка всех активированных пользователей с пагинацией.
        Метод принимает значения указанные в полях accounts_fields, users_fields, paging_fields.
        Так как accounts_fields являются более верхне уровневыми полями, то если мы указываем эти значения, значения
        из users_fields, paging_fields игнорируются. Если хотим получить значения из users_fields, paging_fields,
        то accounts_fields можно не указывать.

        :param accounts_fields: Кортеж с одним и более значений из AccountsResponse.__fields__
        :param users_fields: Кортеж с одним и более значений из GeneralUser.__fields__
        :param paging_fields: Кортеж с одним и более значений из PagingResult.__fields__
        :param skip:
        :param number:
        :param size:
        :param with_inactive:
        :return:
        """
        query_name = 'accounts'
        query_request = self.client.query(name=query_name)
        query = PagingQueryInput(
            skip=skip,
            number=number,
            size=size
        )
        query_request.accounts(paging=query, with_inactive=with_inactive)

        if accounts_fields:
            query_request.accounts.__fields__(*accounts_fields)
        else:
            query_request.accounts.users.__fields__(*users_fields)
            query_request.accounts.paging.__fields__(*paging_fields)

        response = self.client.request(query=query_request)
        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=AccountsResponse
        )
        return response

    def activate_account(self, activation_token: str) -> EnvelopeOfUser | dict:
        """
        Активация пользователя.
        :param activation_token:
        :return:
        """
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

    def login_account(self, login: str, password: str, remember_me: bool) -> AccountLoginResponse | dict:
        """
        Авторизация пользователя.
        :param login:
        :param password:
        :param remember_me:
        :return:
        """
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
