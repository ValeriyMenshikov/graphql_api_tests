from functools import cached_property
from modules.http.mailhog_api.client import MailhogApi
from config.config import Config


class HTTPConnector:

    @cached_property
    def mailhog(self) -> MailhogApi:
        return MailhogApi(host=Config.mailhog)
