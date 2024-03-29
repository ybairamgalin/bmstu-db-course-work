import requests

from testsuite.test_task_tracker_backend import utils

HANDLER = 'http://localhost:6432/api/task'


def test_404():
    response = requests.get(
        utils.gen_query(HANDLER, {'task_id': 1}),
        timeout=5,
    )
    assert response.status_code == 404
    assert response.json() == {
        'message': 'No task with id 1',
    }


def test_no_task_id():
    response = requests.get(HANDLER, timeout=5)
    assert response.status_code == 422
