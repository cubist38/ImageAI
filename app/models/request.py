from typing import *
from pydantic import BaseModel

class SegmentationRequest(BaseModel):
    image: str
    x: str
    y: str

class HighlightRequest(BaseModel):
    image: str
    mask: str

class InpaintRequest(BaseModel):
    image: str
    mask: str

class GenerateDescriptionRequest(BaseModel):
    image: str

class GenerateImageRequest(BaseModel):
    prompt: str

class StorageRequest(BaseModel): 
    access_token: str 

class ImageStorageRequest(BaseModel): 
    access_token: str 
    storage_url: str

class ImportStorageRequest(BaseModel): 
    access_token: str 
    storage_url: str
    
