from abc import abstractmethod
import clip
import torch


class BaseModel():
    @abstractmethod
    def encode_text(self):
        raise NotImplementedError

    @abstractmethod
    def encode_image(self):
        raise NotImplementedError