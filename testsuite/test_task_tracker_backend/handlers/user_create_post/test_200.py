import requests
import datetime as dt
import pytz

HANDLER = 'http://localhost:6432/api/user/create'


def test_200(sql):
    username = 'some_username'
    name = 'Name Surname'

    response = requests.post(
        HANDLER,
        json={
            'username': username,
            'hashed_password': '12345',
            'name': name,
        },
        timeout=5,
    )

    assert response.status_code == 201
    assert response.json() == {'username': username}

    token = response.headers['x-user-token']
    assert token is not None

    db_users = sql("select username, name from task_tracker.users")
    assert len(db_users) == 1
    db_user = db_users[0]
    assert db_user[0] == username
    assert db_user[1] == name

    db_tokens = sql("select uuid, expires_at from task_tracker.tokens")
    assert len(db_tokens) == 1
    db_token = db_tokens[0]
    assert db_token[0] == token
    assert db_token[1] > dt.datetime.utcnow()
