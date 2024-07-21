from src import (
    WeatherProcessorThread,
    WeatherProcessorSequential,
    GeoCoder,
    CityData,
)
from config import APIConfig, db_config
from api import DataAPI
from typing import Any
import time
import logging

logging.basicConfig(level=logging.INFO)


class WeatherBenchmark:
    def __init__(self) -> None:
        """Initialize API and data access configurations."""
        self.api_config = APIConfig()
        self.data_api = DataAPI(db_config)
        self.city_data = CityData(self.data_api)
        self.geo_coder = GeoCoder(self.api_config, self.city_data)

        self.thread_processor = WeatherProcessorThread(
            self.api_config, self.data_api, self.city_data, self.geo_coder
        )
        self.sequential_processor = WeatherProcessorSequential(
            self.api_config, self.data_api, self.city_data, self.geo_coder
        )

    @staticmethod
    def measure_execution_time(processor: Any) -> float:
        """Measures and logs the execution time of a given processing method."""
        start_time = time.time()
        processor.run()
        end_time = time.time()
        execution_time = end_time - start_time
        logging.info(
            f"Execution time for {processor.__class__.__name__}: {execution_time:.2f} seconds"
        )
        return execution_time

    def execute_benchmark(self) -> None:
        """Executes the benchmarking for both threaded and sequential processing methods."""
        logging.info("Starting benchmarking for threaded execution...")
        self.measure_execution_time(self.thread_processor)

        logging.info("Starting benchmarking for sequential execution...")
        self.measure_execution_time(self.sequential_processor)


if __name__ == "__main__":
    benchmark = WeatherBenchmark()
    benchmark.execute_benchmark()
