import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    BASE_URL: str = "http://localhost:800" 
    USE_NGROK: bool = (os.environ.get("USE_NGROK", "False") == "True")
    

def get_settings():
    return Settings()