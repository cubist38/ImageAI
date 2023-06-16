from pydantic import BaseSettings


class Settings(BaseSettings):
    device: str = "cpu"
    sam_model_type: str = "vit_h"
    sam_model_ckpt_p: str = "/content/drive/MyDrive/InpaintAnything/Weights/sam_vit_h_4b8939.pth"
    lama_model_config_p: str = "./models/lama/configs/prediction/default.yaml"
    lama_model_ckpt_p: str = "/content/drive/MyDrive/InpaintAnything/Weights/big-lama"
    caption_model_name: str = "blip-large"
    clip_model_name: str = "ViT-L-14/openai"

def get_settings():
    return Settings()