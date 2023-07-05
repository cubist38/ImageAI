from diffusers import DiffusionPipeline
from functools import lru_cache

@lru_cache
def load_diffusion(model_name: str = "runwayml/stable-diffusion-v1-5", 
                   device: str = None):
    pipeline = DiffusionPipeline.from_pretrained(model_name).to(device)
    return pipeline