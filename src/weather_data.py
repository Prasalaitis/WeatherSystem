from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from typing import Dict, Any

Base = declarative_base()


class WeatherData(Base):
    """
    Defines the structure of the table 'weather_data' within the database.
    """

    __tablename__ = "weather_data"
    weather_id = Column(Integer, primary_key=True)
    country_name = Column(String)
    city_name = Column(String)
    temperature = Column(Float, default=0.0)
    humidity = Column(Float, default=0.0)
    pressure = Column(Float, default=0.0)
    rain = Column(Float, default=0.0)
    description = Column(String)

    @classmethod
    def create_from_api_response(
        cls, session: Session, city_name: str, response: Dict[str, Any]
    ) -> None:
        """
        Create and commit a new WeatherData record to the database based on the response from a weather API.

        Args:
            session (Session): The database session to use for committing this record.
            city_name (str): The name of the city to which this weather data pertains.
            response (Dict[str, Any]): The JSON dictionary response from the weather API containing weather metrics.
        """
        country = response['sys']['country']
        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        pressure = response["main"]["pressure"]
        description = response["weather"][0]["description"]
        rain = response.get("rain", {"1h": 0})["1h"]

        weather_data = cls(
            country_name=country,
            city_name=city_name,
            temperature=temp,
            humidity=humidity,
            pressure=pressure,
            rain=rain,
            description=description,
        )
        session.add(weather_data)
        session.commit()
