import sys
import os

from db_models import Base, OrderRecord
from sqlalchemy.orm import Session

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from testcontainers.postgres import PostgresContainer
import sqlalchemy


def test_postgres_container_starts_and_connects():
    """Sanity check: a real Postgres container can start and accept a connection."""
    with PostgresContainer("postgres:16") as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        with engine.begin() as connection:
            result = connection.execute(sqlalchemy.text("select version()"))
            version = result.fetchone()[0]
            assert "PostgreSQL" in version

def test_insert_and_query_order():
    """Test that an order can be inserted into a real Postgres database and queried back."""
    with PostgresContainer("postgres:16") as postgres:
        engine = sqlalchemy.create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)  # create the orders table

        with Session(engine) as session:
            new_order = OrderRecord(customer_name="Alice", status="created")
            session.add(new_order)
            session.commit()

            result = session.query(OrderRecord).filter_by(customer_name="Alice").first()
            assert result is not None
            assert result.status == "created"
