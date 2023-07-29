def test_account_current(prepare_user, logic):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_helper.register_account(login=login, email=email, password=password)
    access_token = logic.account_graphql.login_account(login=login, password=password, remember_me=True).token
    logic.account_graphql.account_current(access_token=access_token)
