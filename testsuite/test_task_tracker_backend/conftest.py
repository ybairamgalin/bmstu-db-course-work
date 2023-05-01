import datetime as dt

import pytest
import psycopg2

CREDENTIALS = {
    'database': 'task_tracker',
    'user': 'root',
    'password': 'root_password',
    'host': 'localhost',
    'port': 5432
}

CONNECTION = psycopg2.connect(
    database=CREDENTIALS['database'],
    user=CREDENTIALS['user'],
    password=CREDENTIALS['password'],
    host=CREDENTIALS['host'],
    port=CREDENTIALS['port'],
)


@pytest.fixture()
def sql():
    cursor = CONNECTION.cursor()

    def _sql(query, args=()):
        if not query:
            return None
        cursor.execute(query, args)
        CONNECTION.commit()
        try:
            return cursor.fetchall()
        except psycopg2.ProgrammingError:
            return None

    return _sql


@pytest.fixture()
def get_auth_token(sql):
    def _get_auth_token(user_id=1000):
        user_query = f"""
        insert into task_tracker.users(id, username, salt, password)
        values
            ({user_id}, 'username', 'salt', 'password')
        on conflict(id)
        do nothing
        """
        sql(user_query)
        token = 'auth_token'
        token_query = f"""
        insert into task_tracker.tokens(uuid, user_id, expires_at)
        values 
            ('{token}', {user_id}, '{dt.datetime.utcnow() + dt.timedelta(hours=1)}')
        """
        sql(token_query)
        return token

    return _get_auth_token


@pytest.fixture(autouse=True)
def database_cleanup(sql):
    all_tables_query = """
    select table_name from information_schema.tables
    where table_schema = 'task_tracker'"""

    all_tables = sql(all_tables_query)
    clear_all_rows_query = ''
    for table in all_tables:
        clear_all_rows_query += (
            f'truncate table task_tracker.{table[0]} cascade;\n'
        )

    sql(clear_all_rows_query)
    yield
