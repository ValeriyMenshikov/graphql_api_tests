from generic.checkers.checkers import message_checker


def test_login_account(prepare_user, logic):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    access_token = logic.account_graphql.login_account(login=login, password=password).token
    assert access_token, 'Пользователь смог авторизоваться'


def test_login_account_with_invalid_password(prepare_user, logic):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    with message_checker(error_message="The password is incorrect. Did you forget to switch the keyboard?"):
        access_token = logic.account_graphql.login_account(login=login, password=password + '1')

    with message_checker(error_message=None) as response:
        access_token = logic.account_graphql.login_account(login=login, password=password + '1')
        print(response)
