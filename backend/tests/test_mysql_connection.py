import os

import pytest
from sqlalchemy import create_engine, text


@pytest.mark.mysql

def test_mysql_connection():
    url = os.getenv("MYSQL_TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set MYSQL_TEST_DATABASE_URL to run the real MySQL smoke test")
    engine = create_engine(url, pool_pre_ping=True)
    with engine.connect() as connection:
        assert connection.execute(text("SELECT 1")).scalar_one() == 1
