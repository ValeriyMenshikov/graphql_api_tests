def test_register_user(prepare_user, logic):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    response = logic.account_graphql.reset_account_password(login=login, email=email)
