from config import APIConfig, LoggerSetup, db_config
from api import DataAPI
from src import (
    CityData,
    GeoCoder,
    WeatherProcessorThread,
    WeatherProcessorSequential,
)
import os
import time
import logging


class WeatherRunner:
    def __init__(self) -> None:
        """
        Initializes the WeatherRunner with configurations and sets up the processing method.
        Uses a named logger to log the application's operations.
        """
        self.data_api = DataAPI(db_config)
        self.city_data = CityData(self.data_api)
        self.geo_coder = GeoCoder(APIConfig(), self.city_data)
        self.method = os.getenv(
            "METHOD", "thread"
        )  # Default to 'thread' if no env var is set
        self.logger = LoggerSetup(
            "WeatherRunner", "logging", "weather_processing.log"
        ).logger

    def run(self) -> None:
        """
        Executes the weather data processing based on the configured method. It logs the
        execution time and method.

        Raises:
            ValueError: If an invalid execution method is specified.
        """
        method_env = os.getenv("METHOD")
        logging.info("Current METHOD setting: %s", method_env)
        if self.method == "thread":
            processor = WeatherProcessorThread(
                APIConfig(), self.data_api, self.city_data, self.geo_coder
            )
        elif self.method == "sequential":
            processor = WeatherProcessorSequential(
                APIConfig(), self.data_api, self.city_data, self.geo_coder
            )
        else:
            self.logger.error("Invalid execution method specified.")
            raise ValueError("Invalid execution method specified")

        self.logger.info(f"Starting execution with method: {self.method}")
        start_time = time.time()
        processor.run()
        end_time = time.time()
        self.logger.info(
            f"Execution time for {self.method}: {end_time - start_time:.2f} seconds"
        )


if __name__ == "__main__":
    runner = WeatherRunner()
    runner.run()
