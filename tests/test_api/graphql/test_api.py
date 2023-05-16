from unittest.mock import Mock

import pytest

from api.graphql.base import schema


@pytest.mark.asyncio
async def test_create_user(fake):
    mutation = '''
        mutation TestCreateUserMutation($username: String!, $password: String!) {
            createUser (user: {
                username: $username,
                password: $password
            }) {
                username
            }
        }
    '''

    username = fake.user_name()

    # NOTE: `context_value` is required, without it sqlalchemy ext fails
    result = await schema.execute(
        mutation,
        variable_values={
            'username': username,
            'password': fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)
        },
        context_value={}
    )

    assert result.errors is None
    assert result.data['createUser']['username'] == username


@pytest.fixture
async def create_user(fake):
    username = fake.user_name()
    password = fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)

    mutation = '''
        mutation TestCreateUserMutation($username: String!, $password: String!) {
            createUser (user: {
                username: $username,
                password: $password
            }) {
                username
            }
        }
    '''

    await schema.execute(
        mutation,
        variable_values={
            'username': username,
            'password': password
        },
        context_value={}
    )

    return username, password


@pytest.mark.asyncio
async def test_login(create_user):
    username, password = create_user

    mutation = '''
    mutation TestLoginMutation($username: String!, $password: String!) {
        login (
            username: $username,
            password: $password
        ) {
            ... on LoginSuccess {
                token
            }
            ... on LoginError {
                message
            }
        }
    }
    '''

    result = await schema.execute(
        mutation,
        variable_values={
            'username': username,
            'password': password
        },
        context_value={}
    )

    assert result.errors is None
    assert result.data.get('login', None) is not None
    assert result.data.get('message', None) is None
    assert result.data['login'].get('token', None) is not None


@pytest.fixture
async def auth_token(create_user):
    username, password = create_user

    mutation = '''
    mutation TestLoginMutation($username: String!, $password: String!) {
        login (
            username: $username,
            password: $password
        ) {
            ... on LoginSuccess {
                token
            }
            ... on LoginError {
                message
            }
        }
    }
    '''

    result = await schema.execute(
        mutation,
        variable_values={
            'username': username,
            'password': password
        },
        context_value={}
    )

    return result.data['login']['token']


@pytest.mark.asyncio
async def test_get_plan(auth_token):
    query = '''
    query TestPlan {
        plan (dateFrom: "2022-11-20", dateTo: "2022-12-20", userCode: "290b5177-5f78-40cc-9bf7-888416fed988") {
            day,
            userCode,
            dishId,
            dish {
                name,
                description,
                url,
                ingredients {
                    name,
                    amount
                }
            }
        }
    }
    '''

    request_mock = Mock()
    request_mock.headers = {'authorization': auth_token}

    resp = await schema.execute(
        query,
        context_value={'request': request_mock}
    )

    assert resp.errors is None
