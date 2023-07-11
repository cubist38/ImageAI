from typing import *
from pydantic import BaseModel

class SegmentationRequest(BaseModel):
    image: str
    x: str
    y: str

class HighlightRequest(BaseModel):
    image: str
    mask: list

class InpaintRequest(BaseModel):
    image: str
    mask: list

class GenerateDescriptionRequest(BaseModel):
    image: str

class GenerateImageRequest(BaseModel):
    prompt: str