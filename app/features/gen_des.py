from app.features.config import get_settings
from app.helpers.load_gen import load_clip_interrogator

config = get_settings()

def generate_description(image):
    model = load_clip_interrogator(
        caption_model_name=config.caption_model_name,
        clip_model_name=config.clip_model_name,
        device=config.device,
    )
    model.config.chunk_size = 2048 if model.config.clip_model_name == "ViT-L-14/openai" else 1024
    model.config.flavor_intermediate_count = 2048 if model.config.clip_model_name == "ViT-L-14/openai" else 1024
    return model.interrogate_fast(image)