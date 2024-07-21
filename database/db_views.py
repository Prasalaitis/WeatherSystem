from connection_sqlalchemy import SQLAlchemyConnection
from config.db_setup import db_config
from sqlalchemy import text
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DatabaseViews:
    """
    Manages the creation of database views.
    """

    def __init__(self, db_connection: SQLAlchemyConnection):
        """
        Initializes the DatabaseViews with the provided SQLAlchemyConnection.
        """
        self.db_connection = db_connection
        logging.info("DatabaseViews initialized with SQLAlchemy connection.")

    def create_rainfall_counts_view(self):
        """
        Creates or replaces the 'rainfall_counts' view in the database.
        """
        view_name = "rainfall_counts"
        view_query = text(
            """
            CREATE OR REPLACE VIEW rainfall_counts AS
            SELECT
              city_name,
              TO_CHAR(CURRENT_DATE - INTERVAL '1 day', 'YYYY-MM-DD') AS time_frame,
              ROUND(SUM(rain)::numeric, 2) AS total_rain
            FROM weather_data
            WHERE record_time >= CURRENT_TIMESTAMP - INTERVAL '1 day'
              AND record_time < CURRENT_TIMESTAMP
            GROUP BY city_name

            UNION ALL

            SELECT
              city_name,
              TO_CHAR(CURRENT_DATE - INTERVAL '13 days', 'YYYY-MM-DD') || ' to ' || TO_CHAR(CURRENT_DATE - INTERVAL '7 days', 'YYYY-MM-DD') AS time_frame,
              ROUND(SUM(rain)::numeric, 2) AS total_rain
            FROM weather_data
            WHERE record_time >= CURRENT_TIMESTAMP - INTERVAL '14 days'
              AND record_time < CURRENT_TIMESTAMP - INTERVAL '7 days'
            GROUP BY city_name;
        """
        )
        self.execute_sql(view_name, view_query)

    def create_temperature_analytics_view(self):
        """
        Creates or replaces the 'temperature_analytics' view in the database.
        """
        view_name = "temperature_analytics"
        view_query = text(
            """
            CREATE OR REPLACE VIEW temperature_analytics AS
            SELECT
                DISTINCT
                city_name,
                'Today' AS time_frame,
                MAX(temperature) OVER (PARTITION BY city_name) AS max_temperature,
                MIN(temperature) OVER (PARTITION BY city_name) AS min_temperature,
                ROUND(STDDEV(temperature) OVER (PARTITION BY city_name)::numeric, 2) AS stddev_temperature
            FROM
                weather_data
            WHERE
                record_time >= CURRENT_DATE AND record_time < CURRENT_DATE + INTERVAL '1 day'

            UNION ALL

            SELECT
                DISTINCT
                city_name,
                'Yesterday' AS time_frame,
                MAX(temperature) OVER (PARTITION BY city_name) AS max_temperature,
                MIN(temperature) OVER (PARTITION BY city_name) AS min_temperature,
                ROUND(STDDEV(temperature) OVER (PARTITION BY city_name)::numeric, 2) AS stddev_temperature
            FROM
                weather_data
            WHERE
                record_time >= CURRENT_DATE - INTERVAL '1 day' AND record_time < CURRENT_DATE

            UNION ALL

            SELECT
                DISTINCT
                city_name,
                'Current Week' AS time_frame,
                MAX(temperature) OVER (PARTITION BY city_name) AS max_temperature,
                MIN(temperature) OVER (PARTITION BY city_name) AS min_temperature,
                ROUND(STDDEV(temperature) OVER (PARTITION BY city_name)::numeric, 2) AS stddev_temperature
            FROM
                weather_data
            WHERE
                record_time >= date_trunc('week', CURRENT_DATE) AND record_time < CURRENT_DATE + INTERVAL '1 day'

            UNION ALL

            SELECT
                DISTINCT
                city_name,
                'Last 7 Days' AS time_frame,
                MAX(temperature) OVER (PARTITION BY city_name) AS max_temperature,
                MIN(temperature) OVER (PARTITION BY city_name) AS min_temperature,
                ROUND(STDDEV(temperature) OVER (PARTITION BY city_name)::numeric, 2) AS stddev_temperature
            FROM
                weather_data
            WHERE
                record_time >= CURRENT_DATE - INTERVAL '7 days' AND record_time < CURRENT_DATE + INTERVAL '1 day';
        """
        )
        self.execute_sql(view_name, view_query)

    def create_temperature_extremes_view(self):
        """
        Creates or replaces the 'temperature_extremes' view in the database.
        """
        view_name = "temperature_extremes"
        view_query = text(
            """
            CREATE OR REPLACE VIEW temperature_extremes AS
            SELECT * FROM (
                SELECT
                    date_trunc('hour', record_time) AS time_frame,
                    'Hourly' AS interval,
                    FIRST_VALUE(city_name) OVER (PARTITION BY date_trunc('hour', record_time) ORDER BY temperature DESC) AS hottest_city,
                    FIRST_VALUE(temperature) OVER (PARTITION BY date_trunc('hour', record_time) ORDER BY temperature DESC) AS highest_temperature,
                    FIRST_VALUE(city_name) OVER (PARTITION BY date_trunc('hour', record_time) ORDER BY temperature ASC) AS coldest_city,
                    FIRST_VALUE(temperature) OVER (PARTITION BY date_trunc('hour', record_time) ORDER BY temperature ASC) AS lowest_temperature
                FROM
                    weather_data

                UNION ALL

                SELECT
                    DATE(record_time) AS time_frame,
                    'Daily' AS interval,
                    FIRST_VALUE(city_name) OVER (PARTITION BY DATE(record_time) ORDER BY temperature DESC) AS hottest_city,
                    FIRST_VALUE(temperature) OVER (PARTITION BY DATE(record_time) ORDER BY temperature DESC) AS highest_temperature,
                    FIRST_VALUE(city_name) OVER (PARTITION BY DATE(record_time) ORDER BY temperature ASC) AS coldest_city,
                    FIRST_VALUE(temperature) OVER (PARTITION BY DATE(record_time) ORDER BY temperature ASC) AS lowest_temperature
                FROM
                    weather_data

                UNION ALL

                SELECT
                    date_trunc('week', record_time) AS time_frame,
                    'Weekly' AS interval,
                    FIRST_VALUE(city_name) OVER (PARTITION BY date_trunc('week', record_time) ORDER BY temperature DESC) AS hottest_city,
                    FIRST_VALUE(temperature) OVER (PARTITION BY date_trunc('week', record_time) ORDER BY temperature DESC) AS highest_temperature,
                    FIRST_VALUE(city_name) OVER (PARTITION BY date_trunc('week', record_time) ORDER BY temperature ASC) AS coldest_city,
                    FIRST_VALUE(temperature) OVER (PARTITION BY date_trunc('week', record_time) ORDER BY temperature ASC) AS lowest_temperature
                FROM
                    weather_data
            ) AS combined_results
            ORDER BY
                CASE interval
                    WHEN 'Hourly' THEN 1
                    WHEN 'Daily' THEN 2
                    WHEN 'Weekly' THEN 3
                END;
        """
        )
        self.execute_sql(view_name, view_query)

    def execute_sql(self, view_name, sql_command):
        """
        Executes a SQL command using the connection.
        """
        try:
            with self.db_connection.connect() as session:
                session.execute(sql_command)
                logging.info(
                    f"SQL operation for '{view_name}' executed successfully."
                )
        except Exception as e:
            logging.error(
                f"Error executing SQL operation for '{view_name}': {str(e)}"
            )


if __name__ == "__main__":
    db_connection = SQLAlchemyConnection(db_config)
    db_views = DatabaseViews(db_connection)
    db_views.create_rainfall_counts_view()
    db_views.create_temperature_analytics_view()
    db_views.create_temperature_extremes_view()
