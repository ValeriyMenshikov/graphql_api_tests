from generic.checkers.checkers import message_checker


def test_logout_all_account(prepare_user, logic):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    access_token = logic.account_graphql.login_account(login=login, password=password).token
    logic.account_graphql.logout_all_account(access_token=access_token)


def test_logout_all_account_with_invalid_token(prepare_user, logic):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    access_token = logic.account_graphql.login_account(login=login, password=password).token
    with message_checker(error_message="Not authorized: ForgedToken") as message:
        logic.account_graphql.logout_all_account(access_token=access_token + '1')
