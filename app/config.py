import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    App: str = "Software Design Final Project"

    

def get_settings():
    return Settings()