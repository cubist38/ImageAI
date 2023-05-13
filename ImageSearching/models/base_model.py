import torch
from abc import ABC, abstractmethod

class BaseModel():
    """Base class for models"""
    def __init__(self, device) -> None:
        self.device = device
        if not self.device: 
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        pass

    def execute(self, task: str = None, **kwargs):
        pass

class ImageTextEncoder(BaseModel, ABC):
    """Base class for image and text encode model"""
    def __init__(self, device = None) -> None:
        super().__init__(device)

    @abstractmethod
    def encode_image(self, images, **kwargs):
        pass
    
    @abstractmethod
    def encode_text(self, text, **kwargs):
        pass

    @abstractmethod
    def get_image_preprocess():
        pass

    