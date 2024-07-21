import requests
import os
import logging
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()


class TestWeatherAPI:
    """
    APIConfig is a configuration manager for handling requests to a weather API.
    This class is designed to demonstrate the process of making API requests and retrieving weather data.
    """

    def __init__(self):
        """
        Initializes the APIConfig class by loading the API key from environment variables.
        This API key is used for authenticating requests to the weather API.
        """
        self.api_key = os.getenv("WEATHER_API_KEY")
        logging.debug(f"API Key loaded: {self.api_key}")

    def fetch_coordinates(self, city, country):
        """
        Fetches geographical coordinates (latitude and longitude) for a given city and country.
        This method is a test to demonstrate making a request to the weather API for location data.

        Parameters:
            city (str): The city name.
            country (str): The country code.

        Returns:
            tuple: A tuple containing the latitude and longitude of the given location.
        """
        url = "http://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": f"{city},{country}",
            "limit": 1,
            "appid": self.api_key,
        }
        logging.info(f"Fetching coordinates for {city}, {country}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logging.debug(
            f'Coordinates fetched: {data[0]["lat"]}, {data[0]["lon"]}'
        )
        return data[0]["lat"], data[0]["lon"]

    def fetch_weather_data(self, lat, lon):
        """
        Fetches weather data for a given set of geographical coordinates.
        This method tests the retrieval of weather information from the weather API.

        Parameters:
            lat (float): Latitude of the location.
            lon (float): Longitude of the location.

        Returns:
            dict: A dictionary containing the weather data.
        """
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
        }
        logging.info(
            f"Fetching weather data for latitude: {lat}, longitude: {lon}"
        )
        response = requests.get(url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        logging.debug(f"Weather data fetched: {weather_data}")
        return weather_data


api_config = TestWeatherAPI()
lat, lon = api_config.fetch_coordinates("London", "GB")
weather_data = api_config.fetch_weather_data(lat, lon)
logging.info(f"Weather data: {weather_data}")
