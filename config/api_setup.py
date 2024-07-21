import requests
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()


class APIConfig:
    """Handles the configuration and API calls to the OpenWeatherMap API."""

    def __init__(self):
        """Initializes the API configuration using environment variables."""
        self.api_key: str = os.getenv("WEATHER_API_KEY", "")
        self.geo_url: str = "http://api.openweathermap.org/geo/1.0/direct"
        self.weather_url: str = (
            "https://api.openweathermap.org/data/2.5/weather"
        )

    def fetch_coordinates(self, city: str, country: str) -> Dict[str, Any]:
        """
        Fetches geographical coordinates for a given city and country.

        Args:
            city (str): The name of the city.
            country (str): The country the city is located in.

        Returns:
            Dict[str, Any]: A dictionary containing the coordinates of the city.

        Raises:
            HTTPError: If the API call fails.
        """
        params = {
            "q": f"{city},{country}",
            "limit": 1,
            "appid": self.api_key,
        }
        response = requests.get(self.geo_url, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_weather_data(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Fetches weather data for the specified latitude and longitude.

        Args:
            lat (float): The latitude of the location.
            lon (float): The longitude of the location.

        Returns:
            Dict[str, Any]: A dictionary containing weather data.

        Raises:
            HTTPError: If the API call fails.
        """
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
        }
        response = requests.get(self.weather_url, params=params)
        response.raise_for_status()
        return response.json()
