import asyncio
import threading
import time

import pytest


def timeout(sec):
    def _timeout(fn):
        def wrap(*args, **kwargs):
            time.sleep(sec)
            result = fn(*args, **kwargs)
            return result

        return wrap

    return _timeout


def test_subscription(logic, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    graphql_account_ws = logic.provider.graphql.dm_api_account_ws
    thread = threading.Thread(target=graphql_account_ws.user_login_subscription)
    thread.start()
    logic.account_helper.register_account(login=login, email=email, password=password)
    logic.provider.graphql.dm_api_account.login_account(login=login, password=password, remember_me=True)
    thread.join()
    assert graphql_account_ws.messages[0].login == login, 'Сообщение не соответствует ожидаемому!'
    graphql_account_ws.messages.clear()


@pytest.mark.asyncio
async def test_subscription_thread_gather(logic, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    logic.provider.graphql.dm_api_account.login_account(login=login, password=password, remember_me=True)
    coroutines = [
        asyncio.to_thread(logic.provider.graphql.dm_api_account_ws.user_login_subscription, login),
        asyncio.to_thread(timeout(3)(logic.provider.graphql.dm_api_account.login_account), login, password, True)
    ]
    res = await asyncio.gather(*coroutines)


@pytest.mark.asyncio
async def test_subscription_run_in_executor_gather(logic, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    logic.provider.graphql.dm_api_account.login_account(login=login, password=password, remember_me=True)
    loop = asyncio.get_event_loop()
    coroutines = [
        loop.run_in_executor(None, logic.provider.graphql.dm_api_account_ws.user_login_subscription, login),
        loop.run_in_executor(None, timeout(3)(logic.provider.graphql.dm_api_account.login_account), login, password,
                             True)
    ]
    res = await asyncio.gather(*coroutines)


@pytest.mark.asyncio
async def test_subscription_thread_task(logic, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    logic.provider.graphql.dm_api_account.login_account(login=login, password=password, remember_me=True)
    listen = asyncio.create_task(
        asyncio.to_thread(logic.provider.graphql.dm_api_account_ws.user_login_subscription, login)
    )
    await asyncio.sleep(3)
    send = asyncio.create_task(
        asyncio.to_thread(logic.provider.graphql.dm_api_account.login_account, login, password, True)
    )

    listen_result = await listen
    send_result = await send
    print(send_result)
    print(listen_result)
