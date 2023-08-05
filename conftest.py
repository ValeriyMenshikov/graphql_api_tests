from pathlib import Path
import pytest
from datetime import datetime
from generic import LogicProvider
from collections import namedtuple
from modules.graphql.dm_api_account.ws_client import GraphQLWebSocketAccountApi
from vyper import v

options = (
    'service.dm_api_account_graphql',
    'service.dm_api_account_graphql_ws',
    'service.mailhog',
)


@pytest.fixture(autouse=True)
def set_config(request):
    config = Path(__file__).parent.joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(option, request.config.getoption(f'--{option}'))


def pytest_addoption(parser):
    parser.addoption('--env', action='store', default='stg')
    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)


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
def graphql_account_ws():
    client = GraphQLWebSocketAccountApi(
        service_name=v.get('service.dm_api_account_graphql_ws'),
        timeout=10,
    )
    return client


@pytest.fixture
def logic():
    client = LogicProvider()
    return client
