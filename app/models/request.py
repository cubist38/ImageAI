from typing import *
from pydantic import BaseModel
import numpy

class Mask(BaseModel):
    mask_b64: str
    shape: list[int, int]

class SegmentationRequest(BaseModel):
    image: str
    x: str
    y: str

class HighlightRequest(BaseModel):
    image: str
    mask: Mask

class InpaintRequest(BaseModel):
    image: str
    mask: Mask

class GenerateDescriptionRequest(BaseModel):
    image: str

class GenerateImageRequest(BaseModel):
    prompt: str