import threading


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
