import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    App: str = "Magic Photoshop"
    

def get_settings():
    return Settings()