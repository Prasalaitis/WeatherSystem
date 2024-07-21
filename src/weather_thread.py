from config import APIConfig, db_config
from src import CityData, GeoCoder, WeatherData
from api import DataAPI
import threading
from queue import Queue
import logging

logging.basicConfig(level=logging.INFO)


class WeatherProcessorThread:
    """
    Manages the concurrent fetching and storing of weather data for multiple cities using threads.
    """

    def __init__(
        self,
        api_config: APIConfig,
        data_api: DataAPI,
        city_data: CityData,
        geo_coder: GeoCoder,
    ) -> None:
        """
        Initializes the WeatherProcessorThread with API and database configurations.

        Args:
            api_config (APIConfig): Configuration for accessing the weather API.
            data_api (DataAPI): Provides database operation functionalities.
            city_data (CityData): Provides access to city-related data.
            geo_coder (GeoCoder): Provides geocoding functionalities to convert city names to coordinates.
        """
        self.api = api_config
        self.data_api = data_api
        self.city_data = city_data
        self.geo_coder = geo_coder
        self.weather_data_queue = Queue()

    def fetch_and_store_weather_data(
        self, city_name: str, lat: float, lon: float
    ) -> None:
        """
        Fetches weather data from the API and stores it in the database.

        Args:
            city_name (str): The name of the city.
            lat (float): Latitude of the city.
            lon (float): Longitude of the city.
        """
        try:
            response = self.api.fetch_weather_data(lat, lon)
            with self.data_api.sqlalchemy_connection.connect() as session:
                WeatherData.create_from_api_response(
                    session, city_name, response
                )
            logging.info(f"Weather data stored for {city_name}")
        except Exception as e:
            logging.error(f"Failed to store weather data for {city_name}: {e}")

    def store_weather_data_thread(
        self, city_name: str, lat: float, lon: float
    ) -> threading.Thread:
        """
        Initiates a thread to fetch and store weather data for a specific city.

        Args:
            city_name (str): The name of the city.
            lat (float): Latitude of the city.
            lon (float): Longitude of the city.

        Returns:
            threading.Thread: The thread executing the fetch and store operation.
        """
        thread = threading.Thread(
            target=self.fetch_and_store_weather_data,
            args=(city_name, lat, lon),
        )
        thread.start()
        return thread

    def process_cities(self) -> None:
        """
        Processes all cities by initiating threads to fetch and store weather data concurrently.
        """
        threads = []
        cities = self.geo_coder.get_lat_lon()
        for city_name, (lat, lon) in cities.items():
            thread = self.store_weather_data_thread(city_name, lat, lon)
            threads.append(thread)
        for thread in threads:
            thread.join()

    def run(self) -> None:
        """
        Entry point to start processing cities for weather data concurrently.
        """
        logging.info("Processing cities for weather data using threads...")
        self.process_cities()


if __name__ == "__main__":
    api_config = APIConfig()
    data_api = DataAPI(db_config)
    city_data = CityData(data_api)
    geo_coder = GeoCoder(api_config, city_data)
    processor = WeatherProcessorThread(
        api_config, data_api, city_data, geo_coder
    )
    processor.run()
