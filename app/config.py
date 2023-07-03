import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    App: str = "Magic Image Toolkit"

    

def get_settings():
    return Settings()