from database import SQLAlchemyConnection
import pandas as pd
import logging
from typing import Dict


class DataAPI:
    """
    This class provides an API for performing pandas operations using SQL Alchemy.
    """

    def __init__(self, db_config: Dict[str, str]) -> None:
        """
        Initializes the DataAPI with database configuration settings.
        Args:
            db_config (Dict[str, str]): The database configuration settings.
        """
        self.sqlalchemy_connection = SQLAlchemyConnection(db_config)

    def sql_dataframes(self, query: str) -> pd.DataFrame:
        """
        Executes a SQL query using SQLAlchemy and returns the result as a DataFrame.
        Args:
            query (str): The SQL query to execute.
        Returns:
            pd.DataFrame: The result of the query.
        Raises:
            Exception: If there is an error executing the query.
        """
        try:
            with self.sqlalchemy_connection.engine.connect() as connection:
                df = pd.read_sql(query, connection)
            return df
        except Exception as e:
            logging.error(f"Error fetching data: {e}")
            raise
