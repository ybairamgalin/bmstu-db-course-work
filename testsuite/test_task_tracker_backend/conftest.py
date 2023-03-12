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
        cursor.execute(query, args)
        CONNECTION.commit()
        try:
            return cursor.fetchall()
        except psycopg2.ProgrammingError:
            return None

    return _sql


@pytest.fixture(autouse=True)
def database_cleanup(sql):
    all_tables_query = """
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'task_tracker'"""

    all_tables = sql(all_tables_query)
    clear_all_rows_query = ''
    for table in all_tables:
        clear_all_rows_query += (
            f'TRUNCATE TABLE task_tracker.{table[0]} CASCADE;\n'
        )

    sql(clear_all_rows_query)
    yield
