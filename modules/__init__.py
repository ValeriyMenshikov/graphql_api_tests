from modules.http import HTTPConnector
from modules.graphql import GraphQLConnector


class _Provider:
    http = HTTPConnector()
    graphql = GraphQLConnector()


modules_provider = _Provider