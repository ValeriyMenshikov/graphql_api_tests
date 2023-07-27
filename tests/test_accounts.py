def test_accounts(graphql_account_api):
    users_fields = ('user_id', 'email')
    paging_fields = ('total_pages_count', 'page_size')
    accounts_fields = ('users',)
    graphql_account_api.accounts(
        accounts_fields=accounts_fields,
        users_fields=users_fields,
        paging_fields=paging_fields
    )
