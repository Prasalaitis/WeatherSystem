from sqlalchemy import text
from connection_sqlalchemy import SQLAlchemyConnection
from config.db_setup import db_config
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DatabaseTables:
    """
    Manages the creation of database tables.
    """

    def __init__(self, db_connection: SQLAlchemyConnection):
        """
        Initializes the DatabaseTables with the provided SQLAlchemyConnection.

        :param db_connection: An SQLAlchemyConnection object.
        """
        self.db_connection = db_connection
        logging.info("DatabaseTables initialized with SQLAlchemy connection.")

    @staticmethod
    def create_weather_data_table():
        """
        Creates the 'weather_data' table in the database.
        """
        create_weather_query = text(
            """
        CREATE TABLE IF NOT EXISTS weather_data (
            weather_id SERIAL PRIMARY KEY,
            country_name VARCHAR(50) NOT NULL,
            city_name VARCHAR(50) NOT NULL,
            temperature FLOAT,
            humidity INT,
            pressure INT,
            rain FLOAT,
            description VARCHAR(255),
            record_time TIMESTAMP(0) WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_country_city FOREIGN KEY (country_name, city_name)
                REFERENCES cities (country_name, city_name)
        );
        """
        )
        logging.info("Weather data table creation SQL prepared.")
        return create_weather_query

    @staticmethod
    def create_cities_data_table():
        """
        Creates the 'cities_data' table in the database.
        """
        create_cities_query = text(
            """
        CREATE TABLE IF NOT EXISTS cities (
            city_id SERIAL PRIMARY KEY,
            city_name VARCHAR(50) UNIQUE NOT NULL,
            country_name VARCHAR(50) UNIQUE NOT NULL
        );
        """
        )
        logging.info("Cities data table creation SQL prepared.")
        return create_cities_query

    @staticmethod
    def create_simulations_table():
        """
        Creates the 'simulations' table in the database.
        """
        create_simulations_query = text(
            """
            CREATE TABLE IF NOT EXISTS simulations (
                simulation_id SERIAL PRIMARY KEY,
                city_id INT NOT NULL,
                daytime TIMESTAMP,
                predicted_temperature FLOAT,
                prediction VARCHAR(255),
                CONSTRAINT fk_city_simulations FOREIGN KEY (city_id) REFERENCES cities(city_id)
            );
        """
        )
        logging.info("Simulations data table creation SQL prepared.")
        return create_simulations_query

    def table_execution(self):
        """
        Executes the SQL commands to create the tables in the database.
        """
        try:
            with self.db_connection.connect() as session:
                session.execute(self.create_cities_data_table())
                session.commit()
                logging.info("Cities data table created successfully.")

                session.execute(self.create_weather_data_table())
                session.commit()
                logging.info("Weather data table created successfully.")

                session.execute(self.create_simulations_table())
                session.commit()
                logging.info("Simulations data table created successfully.")
        except Exception as e:
            logging.error(f"An error occurred while creating tables: {e}")
            raise


if __name__ == "__main__":
    db_conn = SQLAlchemyConnection(db_config)
    db_tables = DatabaseTables(db_conn)
    db_tables.table_execution()
