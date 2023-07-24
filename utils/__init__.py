import structlog
# from utils.utils import log_graphql_request, create_graphql_log

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)
