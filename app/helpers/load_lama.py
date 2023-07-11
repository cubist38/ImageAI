from omegaconf import OmegaConf
import torch
import os
import yaml
from functools import lru_cache
from models.lama.saicinpainting.training.trainers import load_checkpoint

def build_lama_model(        
        config_p: str,
        ckpt_p: str,
        device="cuda"
):
    predict_config = OmegaConf.load(config_p)
    predict_config.model.path = ckpt_p
    device = torch.device(device)

    train_config_path = os.path.join(
        predict_config.model.path, 'config.yaml')

    with open(train_config_path, 'r') as f:
        train_config = OmegaConf.create(yaml.safe_load(f))

    train_config.training_model.predict_only = True
    train_config.visualizer.kind = 'noop'

    checkpoint_path = os.path.join(
        predict_config.model.path, 'models',
        predict_config.model.checkpoint
    )
    model = load_checkpoint(train_config, checkpoint_path, strict=False)
    model.to(device)
    model.freeze()
    return model

@lru_cache
def load_lama_model(
        config_p: str, 
        ckpt_p: str,
        device = "cuda"):
    return build_lama_model(config_p, ckpt_p, device)