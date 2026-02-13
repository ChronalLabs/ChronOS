import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")
    DEBUG = True

    # Future configs
    WEATHER_BASE_URL = "https://api.open-meteo.com/v1/forecast"
