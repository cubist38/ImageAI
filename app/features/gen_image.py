from app.features.config import get_settings
from app.helpers.load_diffusion import load_diffusion

config = get_settings()

def gen_image_from_prompt(prompt: str, num_inference_step = 30):
    pipeline = load_diffusion(config.gen_image_model_name, config.device)
    image = pipeline(prompt, num_inference_step = num_inference_step)
    return image