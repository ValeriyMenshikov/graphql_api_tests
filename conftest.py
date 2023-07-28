import pytest
from datetime import datetime

from generic.helpers import LogicProvider
from modules.graphql.dm_api_account.client import GraphQLAccountApi
from collections import namedtuple
from modules.http.mailhog_api.client import MailhogApi


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime("%Y_%m_%d_%H_%M_%S")
    login = f'login_{data}'
    email = f'login_{data}@mail.ru'
    password = '12345678'
    user = namedtuple('User', 'login, email, password')
    return user(login=login, email=email, password=password)


@pytest.fixture
def graphql_account_api():
    client = GraphQLAccountApi(service_name='http://5.63.153.31:5051')
    return client


@pytest.fixture
def mailhog_api():
    client = MailhogApi(host='http://5.63.153.31:5025')
    return client


@pytest.fixture
def logic(mailhog_api, graphql_account_api):
    client = LogicProvider(
        mailhog=mailhog_api,
        account_graphql=graphql_account_api
    )
    return client
