from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'kruger',
            'email': 'ricardo@example.com',
            'password': 'pass1234',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'username': 'kruger',
        'email': 'ricardo@example.com',
    }


def test_create_user_with_existing_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': f'new{user.email}',
            'password': 'somepassword',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_with_existing_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': f'new{user.username}',
            'email': f'{user.email}',
            'password': 'somepassword',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_single_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_users_not_found(client):
    response = client.get('/users/9999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'NewUserName',
            'email': 'other@email.com',
            'password': 'newpass987',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'NewUserName',
        'email': 'other@email.com',
    }


def test_update_user_integrity_error(client, user, token):
    # Criando um registro para "fausto"
    client.post(
        '/users',
        json={
            'username': 'fausto',
            'email': 'fausto@example.com',
            'password': 'secret',
        },
    )

    # Alterando o user.username das fixture para fausto
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'fausto',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or Email already exists'
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
