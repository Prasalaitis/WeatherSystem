from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import logging


class SQLAlchemyConnection:
    """
    Manages the database connections using SQLAlchemy. It ensures that connections are properly opened and
    closed, and transactions are correctly managed with commits or rollbacks as needed.
    """

    def __init__(self, db_config):
        """
        Initializes the SQLAlchemyConnection with the provided database configuration.
        :param db_config: A dictionary containing the database configuration.
        """
        db_url = (
            f"postgresql+psycopg2://"
            f"{db_config['user']}:"
            f"{db_config['password']}"
            f"@{db_config['host']}"
            f"/{db_config['database']}"
        )
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def connect(self):
        """
        A context manager that manages a database session. It automatically commits
        the transaction on successful block execution or rolls back if an exception occurs.
        """
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Database error: {e}")
            raise
        finally:
            session.close()
