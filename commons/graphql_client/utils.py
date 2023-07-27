import pprint
import uuid
from datetime import datetime
from typing import Any, Dict, Optional, Union
import structlog
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation
from functools import wraps

__logger__ = structlog.get_logger(__name__).bind(service="GraphQL")


def log_graphql_request(func):
    """Decorator to log a graphql request"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        client_instance = args[0]

        if client_instance.disable_log:
            return func(*args, **kwargs)

        start_time = datetime.now()
        response = func(*args, **kwargs)
        end_time = datetime.now()
        elapsed_time = str(end_time - start_time)
        query = kwargs.get("query")
        if query:
            print('\ngraphQL QUERY:')
            pprint.pp(query)
        create_graphql_log(
            log_bind=__logger__.bind(request_id=str(uuid.uuid4())),
            endpoint=client_instance._endpoint,
            host=client_instance.service_name,
            query=query or args[1],
            response=response,
            elapsed_time=elapsed_time,
        )
        return response

    return wrapper


def create_graphql_log(
        log_bind,
        endpoint: HTTPEndpoint,
        host: str,
        query: Operation,
        response: Union[Dict[str, Any]],
        elapsed_time: str,
):
    """Create log"""
    log_bind.msg(
        "request",
        url=endpoint.url,
        host=host,
        headers=endpoint.base_headers,
        operation_kind=query._Operation__kind,
        operation_name=query._Operation__name,
        request=query,
    )
    log_bind.msg("response", response_data=response, elapsed_time=elapsed_time)
