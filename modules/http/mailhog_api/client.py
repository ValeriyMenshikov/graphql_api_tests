import json

import allure
import requests
from time import sleep


class MailhogApi:
    def __init__(self, host: str, disable_log=False) -> None:
        self.host = host
        self.disable_log = disable_log
        self.client = requests.session()

    @allure.step("Получить список писем")
    def get_api_v2_messages(self, limit: int = 50) -> requests.Response:
        """
        Get messages by limit
        :param limit:
        :return:
        """
        response = self.client.get(
            url=f"{self.host}/api/v2/messages",
            params={
                'limit': limit
            }
        )

        return response

    @allure.step("Получить токен из последнего письма")
    def get_token_from_last_email(self) -> str:
        """
        Get user activation token from last email
        :return:
        """
        sleep(2)
        emails = self.get_api_v2_messages(limit=1).json()
        data = json.loads(emails["items"][0]["Content"]["Body"])
        token_url = data.get("ConfirmationLinkUrl") or data.get("ConfirmationLinkUri")
        token = token_url.split("/")[-1]
        return token

    @allure.step("Удалить все письма")
    def delete_all_messages(self) -> requests.Response:
        response = self.client.delete(url=f"{self.host}/api/v1/messages")
        return response
