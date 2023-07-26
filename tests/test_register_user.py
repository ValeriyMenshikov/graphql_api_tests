def test_mutation(prepare_user, graphql_account_api):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    graphql_account_api.register_user(login=login, email=email, password=password)
