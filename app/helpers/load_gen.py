from clip_interrogator import Config, Interrogator
from functools import lru_cache

@lru_cache
def load_clip_interrogator(caption_model_name: str = "blip-large", 
                           clip_model_name: str =  "ViT-L-14/openai",
                           device: str = "cpu"):
    model_config = {
        "caption_model_name": caption_model_name,
        "clip_model_name": clip_model_name,
    }
    config = Config(**model_config)
    config.device = device
    model = Interrogator(config)
    return model