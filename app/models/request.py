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