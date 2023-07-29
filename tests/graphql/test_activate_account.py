def test_activate_account(logic, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    logic.account_graphql.register_account(
        login=login,
        email=email,
        password=password
    )
    activation_token = logic.mailhog.get_token_from_last_email()
    logic.account_graphql.activate_account(activation_token=activation_token)
