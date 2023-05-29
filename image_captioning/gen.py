import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "image_captioning"))
from model import load_clip_interrogator

def generate_description(image, device="cuda"):
    if image.mode == "RGBA":
        image = image.convert("RGB")  
        
    model = load_clip_interrogator("clip_interrogator/config.json", device)
    model.config.chunk_size = 2048 if model.config.clip_model_name == "ViT-L-14/openai" else 1024
    model.config.flavor_intermediate_count = 2048 if model.config.clip_model_name == "ViT-L-14/openai" else 1024
    return model.interrogate_fast(image)