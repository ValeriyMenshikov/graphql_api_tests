import queue
import threading


def test_subscription(logic, prepare_user, graphql_account_ws):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    thread = threading.Thread(target=graphql_account_ws.user_login_subscription)
    thread.start()
    logic.account_helper.register_account(login=login, email=email, password=password)
    logic.account_graphql.login_account(login=login, password=password, remember_me=True)
    thread.join()
    assert graphql_account_ws.messages[0].login == login, 'Сообщение не соответствует ожидаемому!'
