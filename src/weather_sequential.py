from config import APIConfig, db_config
from src import CityData, GeoCoder, WeatherData
from api import DataAPI
import logging

logging.basicConfig(level=logging.INFO)


class WeatherProcessorSequential:
    """
    Handles the sequential processing of weather data for multiple cities.
    """

    def __init__(
        self,
        api_config: APIConfig,
        data_api: DataAPI,
        city_data: CityData,
        geo_coder: GeoCoder,
    ) -> None:
        """
        Initializes the WeatherProcessorSequential with required configurations and data access objects.

        Args:
            api_config (APIConfig): Configuration settings for the weather API.
            data_api (DataAPI): Data access API for database operations.
            city_data (CityData): Access to city data for processing.
            geo_coder (GeoCoder): Geocoding utility to fetch geographic coordinates.
        """
        self.api = api_config
        self.data_api = data_api
        self.city_data = city_data
        self.geo_coder = geo_coder

    def store_weather_data(
        self, city_name: str, lat: float, lon: float
    ) -> None:
        """
        Fetches weather data for a specified city and stores it in the database.

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

    def process_cities(self) -> None:
        """
        Processes all cities to fetch and store weather data sequentially.
        """
        cities = self.geo_coder.get_lat_lon()
        for city_name, (lat, lon) in cities.items():
            self.store_weather_data(city_name, lat, lon)

    def run(self) -> None:
        """
        Entry point to start the sequential processing of cities for weather data.
        """
        logging.info("Processing cities for weather data...")
        self.process_cities()


if __name__ == "__main__":
    api_config = APIConfig()
    data_api = DataAPI(db_config)
    city_data = CityData(data_api)
    geo_coder = GeoCoder(api_config, city_data)
    processor = WeatherProcessorSequential(
        api_config, data_api, city_data, geo_coder
    )
    processor.run()
