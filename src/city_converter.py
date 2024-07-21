from config import APIConfig, db_config
from api import DataAPI
import logging
from typing import Dict, Tuple

logging.basicConfig(level=logging.INFO)


class CityData:
    def __init__(self, data_api_instance: DataAPI) -> None:
        """
        Initializes the CityData with a given DataAPI instance.
        """
        self.data_api = data_api_instance

    def get_cities(self) -> dict:
        """
        Retrieves a dictionary of city names and their corresponding countries from the database.

        Returns:
            dict: A dictionary where keys are city names and values are the corresponding country names.
        """
        query = "SELECT city_name, country_name FROM cities;"
        try:
            result = self.data_api.sql_dataframes(query)
            if not result.empty:
                return result.set_index("city_name")["country_name"].to_dict()
            else:
                logging.info("No cities found in the database.")
                return {}
        except Exception as e:
            logging.error(f"Failed to fetch cities: {e}")
            return {}


class GeoCoder:
    def __init__(
        self, api_config_instance: APIConfig, city_data_instance: CityData
    ) -> None:
        """
        Initializes the GeoCoder with APIConfig and CityData instances.

        Args:
            api_config_instance (APIConfig): An instance of APIConfig for fetching coordinates.
            city_data_instance (CityData): An instance of CityData to retrieve city data.
        """
        self.api_config = api_config_instance
        self.city_data = city_data_instance

    def get_lat_lon(self) -> Dict[str, Tuple[float, float]]:
        """
        Retrieves latitude and longitude for cities retrieved from CityData.

        Returns:
            A dictionary with city names as keys and tuples of (latitude, longitude) as values.
        """
        cities = self.city_data.get_cities()
        lat_lon_dict = {}
        for city, country in cities.items():
            data = self.api_config.fetch_coordinates(str(city), country)
            if data and len(data) > 0:
                lat_lon_dict[str(city)] = (data[0]["lat"], data[0]["lon"])
            else:
                logging.warning(f"No data found for {city}, {country}")
        return lat_lon_dict


if __name__ == "__main__":
    api_config = APIConfig()
    data_api = DataAPI(db_config)
    city_data = CityData(data_api)
    geo_coder = GeoCoder(api_config, city_data)
    lat_lon = geo_coder.get_lat_lon()
    for city, coords in lat_lon.items():
        print(f"{city}: {coords}")
