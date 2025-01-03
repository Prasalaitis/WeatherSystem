# Weather Data System

## Project Overview
This project is designed to fetch, process, and store weather data for multiple cities using different processing methods (sequential, threaded). It uses external APIs to gather current weather data and stores this information in a PostgreSQL database using SQLAlchemy for ORM operations. The system also includes views for performing various analytical operations on the stored data.

## Features
- Fetch weather data from OpenWeatherMap API.
- Process data using different methods: sequential, threaded.
- Store weather data in PostgreSQL database.
- Analyze data through SQL views such as rainfall counts, temperature analytics and temperature extremes.


## Prerequisites
Things you need to have:
```
Open Weather API (coordinates(lat,lon)): http://api.openweathermap.org/geo/1.0/direct
Open Weather API: https://api.openweathermap.org/data/2.5/weather
PostgreSQL==16.1
python==3.12.3
poetry==1.8.2
```

### Installation
A step-by-step series of examples that tell you how to get a development environment running.

#### Step 1: Clone the repository
```bash
git clone https://github.com/Prasalaitis/WeatherSystem/blob WeatherSystem
cd your-project-name
```

#### Step 2: Install dependencies
Using poetry, install all dependent libraries:
```bash
poetry install
```

#### Step 3: Set environment variables
Create a `.env` file in the root directory (or locally on your machine) and add the necessary environment variables:
```
WEATHER_DB_HOST = 'localhost'
WEATHER_DB_PORT = 'yourdbport'
WEATHER_DB_NAME = 'yourdbname'
WEATHER_DB_USER = 'yourdbuser'
WEATHER_DB_PASSWORD = 'yourdbpassword'

WEATHER_API_KEY = 'yourAPIkey'
```

#### Step 4: Running the tests
Run a test to check connection to Weather API:
```bash
poetry shell
poetry run python tests/test_weather_api.py
```

#### Step 5: Create database tables and views
Create database tables:
```bash
poetry shell
poetry run python -m database.db_tables
```
Create database views:
```bash
poetry run python -m database.db_views
```

#### Step 6: Set up cronjob
Runs Weather API every hour
```bash
1 * * * * /usr/bin/python3 your-project-name/main.py > /dev/null 2>&1
```
Runs Backups every day at 1:00 AM
```bash
0 1 * * * /usr/bin/python3 your-project-name/backup/full_backup.py > /dev/null 2>&1
```

### Running the application
How to run the application:
```bash
poetry shell
poetry run python -m main
```

## Project Structure
```
your-project-name/
│
├── api/
│   ├── __init__.py
│   └── db_api.py
│   
├── backups/
│
├── config/
│   ├── __init__.py
│   ├── api_setup.py
│   ├── db_setup.py
│   └── logging_setup.py
│
├── cron/
│   └── crontab.txt
│
├── database/
│   ├── __init__.py
│   ├── connection_sqlalchemy.py
│   ├── db_tables.py
│   ├── db_views.py
│   └── full_backup.py.py
│
├── docs/
│   └── weather_ERD.png
│
├── logging/
│   ├── backup.log
│   └── weather_processing.log
│
├── src/
│   ├── __init__.py
│   ├── benchmark.py
│   ├── weather_thread.py
│   ├── weather_sequential.py
│   ├── city_converter.py
│   └── weather_data.py
│   
├── tests/
│   ├── __init__.py
│   └── test_weather_api.py
│   
├── main.py
├── README.md
├── .env
├── pyproject.toml
├── poetry.lock
└── .gitignore
```
