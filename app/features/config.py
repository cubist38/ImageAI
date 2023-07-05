from pydantic import BaseSettings
import torch


class Settings(BaseSettings):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    sam_model_type: str = "vit_h"
    sam_model_ckpt_p: str = "/content/drive/MyDrive/InpaintAnything/Weights/sam_vit_h_4b8939.pth"
    lama_model_config_p: str = "./models/lama/configs/prediction/default.yaml"
    lama_model_ckpt_p: str = "/content/drive/MyDrive/InpaintAnything/Weights/big-lama"
    caption_model_name: str = "blip-large"
    clip_model_name: str = "ViT-L-14/openai"
    gen_image_model_name: str = "runwayml/stable-diffusion-v1-5"

def get_settings():
    return Settings()