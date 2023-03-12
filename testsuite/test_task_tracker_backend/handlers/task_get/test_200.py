import requests

from testsuite.test_task_tracker_backend import utils

HANDLER = 'http://localhost:6432/task'


def test_200(sql):
    _insert_user(sql)
    _insert_task(sql)
    response = requests.get(utils.gen_query(HANDLER, {'task_id': 1}))
    assert response.status_code == 200
    assert response.json() == {
        'task': {
            'content': 'task_content',
            'created_at': '2020-10-10 00:00:00',
            'updated_at': '2021-11-11 00:00:00',
            'executor_id': 1,
            'creator_id': 1,
            'id': 1,
            'title': 'task_name',
        }
    }


def _insert_user(sql):
    sql("""
        INSERT INTO task_tracker.users (id, username, name, salt, password)
        VALUES
            (1, 'username', 'name', 'salt', 'password')
    """)


def _insert_task(sql):
    sql("""
        INSERT INTO task_tracker.tasks (
            id,
            title,
            content,
            creator,
            executor,
            created_at,
            updated_at
        )
        VALUES
            (1, 'task_name', 'task_content', 1, 1, '2020-10-10', '2021-11-11')
    """)
