from generic.helpers.account import AccountHelper
from modules.graphql.dm_api_account.client import GraphQLAccountApi
from modules.http.mailhog_api.client import MailhogApi


class LogicProvider:
    def __init__(self, account_graphql, mailhog, ):
        self.account_graphql: GraphQLAccountApi = account_graphql
        self.mailhog: MailhogApi = mailhog
        self.account_helper = AccountHelper(self)
