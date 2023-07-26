def test_account_current(prepare_user, graphql_account_api, mailhog_api):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    graphql_account_api.register_user(login=login, email=email, password=password)
    activation_token = mailhog_api.get_token_from_last_email()
    graphql_account_api.activate_account(activation_token=activation_token)
    access_token = graphql_account_api.login_account(login=login, password=password, remember_me=True).token
    graphql_account_api.account_current(access_token=access_token)
