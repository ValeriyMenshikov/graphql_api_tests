from graphql_client.client import GraphQLClient
from schema.dm_api_schema import dm_api_schema, Mutation, RegistrationInput
import datetime


def test_mutation_registration():
    client = GraphQLClient(service_name='http://5.63.153.31:5051/', schema=dm_api_schema)
    mutation: Mutation.register_account = client.mutation(name='register_user')
    now = datetime.datetime.now()
    data = now.strftime("%Y_%m_%d_%H_%M_%S")
    login = f'login_{data}'
    email = f'login_{data}@mail.ru'
    password = '12345678'
    request: RegistrationInput = RegistrationInput(
        login=login,
        email=email,
        password=password
    )
    client.request(query=request)
    print(mutation)
