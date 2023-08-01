import allure
import json


def allure_attach(request, response):
    allure.attach(body=str(request), attachment_type=allure.attachment_type.TEXT, name='GraphQL request')
    allure.attach(body=json.dumps(response, indent=2), attachment_type=allure.attachment_type.JSON, name='Response')
