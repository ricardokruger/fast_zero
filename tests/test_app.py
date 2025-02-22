from http import HTTPStatus


def test_root_deve_ser_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'kruger',
                'email': 'ricardo@example.com',
            }
        ]
    }


def test_read_users(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'kruger',
        'email': 'ricardo@example.com',
    }


def test_users_not_found(client):
    response = client.get('/users/9999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
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


def test_update_user_not_found(client):
    response = client.put(
        '/users/9999',
        json={
            'username': 'NewUserName',
            'email': 'other@email.com',
            'password': 'newpass987',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/9999')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}
