from typing import *
from pydantic import BaseModel
import numpy

class SegmentationRequest(BaseModel):
    image: str
    x: str
    y: str

class HighlightRequest(BaseModel):
    image: str
    mask: list[str, numpy.ndarray]

class InpaintRequest(BaseModel):
    image: str
    mask: list[str, numpy.ndarray]

class GenerateDescriptionRequest(BaseModel):
    image: str

class GenerateImageRequest(BaseModel):
    prompt: str