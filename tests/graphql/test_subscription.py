import asyncio

import pytest
from sgqlc.endpoint.websocket import WebSocketEndpoint
from sgqlc.operation import Operation
from websocket import WebSocketTimeoutException

import threading

from modules.graphql.dm_api_account.schema import Subscription


def test_1(logic, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    thread = threading.Thread(target=logic.account_graphql.user_login_subscription)
    thread.start()
    logic.account_helper.register_account(login=login, email=email, password=password)
    logic.account_graphql.login_account(login=login, password=password, remember_me=True)
    thread.join(timeout=10)
