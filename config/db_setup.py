import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db_config = {
    "host": os.getenv("WEATHER_DB_HOST"),
    "port": os.getenv("WEATHER_DB_PORT"),
    "database": os.getenv("WEATHER_DB_NAME"),
    "user": os.getenv("WEATHER_DB_USER"),
    "password": os.getenv("WEATHER_DB_PASSWORD"),
}
