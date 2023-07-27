def test_accounts(graphql_account_api):
    users_fields = ('user_id', 'email')
    paging_fields = ('total_pages_count', 'page_size')
    result = graphql_account_api.accounts(
        users_fields=users_fields,
        paging_fields=paging_fields
    )
