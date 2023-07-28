def test_accounts(logic):
    users_fields = ('user_id', 'email')
    paging_fields = ('total_pages_count', 'page_size')
    result = logic.account_graphql.accounts(
        users_fields=users_fields,
        paging_fields=paging_fields
    )
