import allure
import sgqlc
from sgqlc.types import ContainerTypeMeta, non_null

from modules.graphql.dm_api_account.errors import GraphQLClientError
from modules.graphql.dm_api_account.schema import (
    schema,
    Mutation,
    Query,
    RegistrationInput,
    AccountRegisterResponse,
    EnvelopeOfUserDetails,
    EnvelopeOfUser,
    LoginCredentialsInput,
    AccountLoginResponse,
    PagingQueryInput,
    AccountsResponse,
    GeneralUser,
    PagingResult,
    ChangeEmailInput,
    ResetPasswordInput,
    ChangePasswordInput,
    UpdateUserInput,
    MutationResult,
)
from commons.graphql_client.client import GraphQLClient
from modules.graphql.dm_api_account.utils import allure_attach as attach


class GraphQLAccountApi:
    def __init__(
            self,
            service_name: str = '',
            endpoint: str = "/graphql/",
            disable_log: bool = False,
            base_headers: dict = None,
            allure_attach: bool = True
    ):
        self.client = GraphQLClient(
            service_name=service_name,
            endpoint=endpoint,
            disable_log=disable_log,
            base_headers=base_headers,
            schema=schema
        )
        self.allure_attach = allure_attach

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
        raise GraphQLClientError(response)

    @allure.step('Зарегистрировать пользователя.')
    def register_account(self, login: str, email: str, password: str) -> AccountRegisterResponse:
        """
        Регистрация пользователя.
        :param login:
        :param email:
        :param password:
        :return:
        """
        query_name = 'registerAccount'
        mutation_request = self.client.mutation(name=query_name)
        registration_input = RegistrationInput(
            login=login,
            email=email,
            password=password,
        )
        mutation_request.register_account(registration=registration_input)
        response = self.client.request(query=mutation_request)

        if self.allure_attach:
            attach(request=mutation_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=AccountRegisterResponse
        )

        return response

    @allure.step('Получить информацию о текущем пользователе.')
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

        if self.allure_attach:
            attach(request=query_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUserDetails
        )
        return response

    @allure.step('Получить список всех активированных пользователей с пагинацией.')
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

        if self.allure_attach:
            attach(request=query_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=AccountsResponse
        )
        return response

    @allure.step('Активировать пользователя.')
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

        if self.allure_attach:
            attach(request=mutation_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUser
        )
        return response

    @allure.step('Авторизовать пользователя.')
    def login_account(self, login: str, password: str, remember_me: bool = True) -> AccountLoginResponse | dict:
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

        if self.allure_attach:
            attach(request=mutation_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=AccountLoginResponse
        )
        return response

    @allure.step('Сменить почту пользователя.')
    def change_account_email(self, login: str, password: str, email: str) -> EnvelopeOfUser | dict:
        """
        Сменить почту пользователя.
        :param login:
        :param password:
        :param email:
        :return:
        """
        query_name = 'changeAccountEmail'
        mutation_request = self.client.mutation(name=query_name)
        change_email_input = ChangeEmailInput(
            login=login,
            password=password,
            email=email
        )
        mutation_request.change_account_email(change_email=change_email_input)
        response = self.client.request(query=mutation_request)

        if self.allure_attach:
            attach(request=mutation_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUser
        )
        return response

    @allure.step('Сбросить пароль пользователя')
    def reset_account_password(self, login: str, email: str) -> EnvelopeOfUser | dict:
        """
        Сбросить пароль пользователя
        :param login:
        :param email:
        :return:
        """
        query_name = 'resetAccountPassword'
        mutation_request = self.client.mutation(name=query_name)
        reset_password_input = ResetPasswordInput(
            login=login,
            email=email
        )
        mutation_request.reset_account_password(reset_password=reset_password_input)
        response = self.client.request(query=mutation_request)

        if self.allure_attach:
            attach(request=mutation_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUser
        )
        return response

    @allure.step('Завершить смену пароля пользователя.')
    def change_account_password(self, login: str, token: str, old_password, new_password) -> EnvelopeOfUser | dict:
        """
        Завершить смену пароля пользователя.
        :param login:
        :param token: Токен сброса пароля пользователя
        :param old_password:
        :param new_password:
        :return:
        """
        query_name = 'changeAccountPassword'
        mutation_request = self.client.mutation(name=query_name)
        reset_password_input = ChangePasswordInput(
            login=login,
            token=token,
            old_password=old_password,
            new_password=new_password
        )
        mutation_request.change_account_password(change_password=reset_password_input)
        response = self.client.request(query=mutation_request)

        if self.allure_attach:
            attach(request=mutation_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUser
        )
        return response

    @allure.step('Обновить данные профиля текущего пользователя.')
    def update_account(
            self,
            access_token: str,
            **kwargs: dict[UpdateUserInput.__field_names__]
    ) -> EnvelopeOfUserDetails | dict:
        """
        Обновить данные профиля текущего пользователя.
        :param access_token:
        :param kwargs:
        :return:
        """
        query_name = 'updateAccount'
        mutation_request = self.client.mutation(name=query_name)

        update_user_input = UpdateUserInput()
        for k, v in kwargs.items():
            update_user_input.__setattr__(name=k, value=v)
        mutation_request.update_account(access_token=access_token, user_data=update_user_input)
        response = self.client.request(query=mutation_request)

        if self.allure_attach:
            attach(request=mutation_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=EnvelopeOfUserDetails
        )
        return response

    @allure.step('Закрыть текущую сессию пользователя.')
    def logout_account(self, access_token: str) -> non_null(MutationResult) | dict:
        """
        Закрытие текущей сессии пользователя.
        :param access_token:
        :return:
        """
        query_name = 'logoutAccount'
        mutation_request = self.client.mutation(name=query_name)
        mutation_request.logout_account(access_token=access_token)
        response = self.client.request(query=mutation_request)

        if self.allure_attach:
            attach(request=mutation_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=non_null(MutationResult)
        )
        return response

    @allure.step('Закрыть все сессии пользователя (кроме текущей).')
    def logout_all_account(self, access_token: str) -> non_null(MutationResult) | dict:
        """
        Закрытие всех сессий пользователя (кроме текущей).
        :param access_token:
        :return:
        """
        query_name = 'logoutAllAccount'
        mutation_request = self.client.mutation(name=query_name)
        mutation_request.logout_all_account(access_token=access_token)
        response = self.client.request(query=mutation_request)

        if self.allure_attach:
            attach(request=mutation_request, response=response)

        response = self._convert_to_model(
            response=response,
            query_name=query_name,
            model=non_null(MutationResult)
        )
        return response
