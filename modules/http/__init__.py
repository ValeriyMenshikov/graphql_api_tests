from functools import cached_property
from modules.http.mailhog_api.client import MailhogApi
from vyper import v


class HTTPConnector:

    @cached_property
    def mailhog(self) -> MailhogApi:
        return MailhogApi(host=v.get('service.mailhog'))
