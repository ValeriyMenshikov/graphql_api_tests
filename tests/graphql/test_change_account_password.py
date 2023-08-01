def test_change_account_password(logic, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    logic.account_graphql.reset_account_password(login=login, email=email)
    token = logic.mailhog.get_token_from_last_email()
    new_password = 'new_' + password
    logic.account_graphql.change_account_password(
        login=login,
        token=token,
        old_password=password,
        new_password=new_password
    )
    logic.account_graphql.login_account(login=login, password=new_password)
