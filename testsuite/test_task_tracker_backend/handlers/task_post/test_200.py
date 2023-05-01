import pytest
import requests

HANDLER = 'http://localhost:6432/api/task'


@pytest.mark.parametrize(
    'title, content',
    [
        pytest.param('title_1', None, id='task-without-content'),
        pytest.param('title_2', 'task content', id='task-with-content'),
    ]
)
def test_200(sql, title, content, get_auth_token):
    token = get_auth_token()
    body = {'title': title}
    if content is not None:
        body['content'] = content

    response = requests.post(
        HANDLER, json=body, headers={'X-User-Token': token}, timeout=5,
    )
    assert response.status_code == 201

    db_tasks = _get_tasks(sql)
    assert len(db_tasks) == 1
    assert db_tasks[0] == (response.json()['id'], title, content)


def _get_tasks(sql):
    return sql("""
        select public_id, title, content
        from task_tracker.tasks
    """)
