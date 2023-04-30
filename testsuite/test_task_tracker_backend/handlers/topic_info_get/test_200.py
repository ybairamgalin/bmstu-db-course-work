import requests

HANDLER = 'http://localhost:6432/api/topic/info'
TOPIC_NAME = 'topic_name'


def test_200(sql):
    _insert_topic(sql)

    response = requests.get(HANDLER, timeout=5)
    assert response.status_code == 200
    assert response.json() == {
        'topics': [{'id': 1, 'name': TOPIC_NAME}]
    }


def _insert_topic(sql):
    sql("""
        insert into task_tracker.topics (id, name)
        values 
            (1, 'topic_name')
    """)