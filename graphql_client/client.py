from abc import ABC, abstractmethod
from typing import Any, Dict
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation


class BaseGraphQLClient(ABC):
    @property
    @abstractmethod
    def service_name(self):
        pass

    @property
    @abstractmethod
    def endpoint(self):
        pass

    def __init__(self):
        api_url = self.service_name + self.endpoint
        self._endpoint = HTTPEndpoint(api_url, base_headers=self.authorize())

    @staticmethod
    def authorize() -> dict:
        """
        Authorization headers one wants to add.

        :return: Headers to add to every request
        """
        return {}

    def make_request(self, query: Operation) -> Dict[str, Any]:
        """
        Public method to make a request

        :param query: Operation
        :return: GraphQL Response
        """
        return self._endpoint(query)
