import streamlit as st
from omegaconf import OmegaConf
import torch
import os
import yaml
import numpy as np
import sys
from pathlib import Path
from functools import lru_cache

sys.path.insert(0, str(Path(__file__).resolve().parent / "lama"))
from lama.saicinpainting.evaluation.utils import move_to_device
from lama.saicinpainting.training.trainers import load_checkpoint
from lama.saicinpainting.evaluation.data import pad_tensor_to_modulo

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

@torch.no_grad()
def inpaint_img_with_built_lama(
        model,
        img: np.ndarray,
        mask: np.ndarray,
        config_p=None,
        mod=8,
        device="cuda"
):
    assert len(mask.shape) == 2
    if np.max(mask) == 1:
        mask = mask * 255
    img = torch.from_numpy(img).float().div(255.)
    mask = torch.from_numpy(mask).float()

    batch = {}
    batch['image'] = img.permute(2, 0, 1).unsqueeze(0)
    batch['mask'] = mask[None, None]
    unpad_to_size = [batch['image'].shape[2], batch['image'].shape[3]]
    batch['image'] = pad_tensor_to_modulo(batch['image'], mod)
    batch['mask'] = pad_tensor_to_modulo(batch['mask'], mod)
    batch = move_to_device(batch, device)
    batch['mask'] = (batch['mask'] > 0) * 1

    batch = model(batch)
    cur_res = batch["inpainted"][0].permute(1, 2, 0)
    cur_res = cur_res.detach().cpu().numpy()

    if unpad_to_size is not None:
        orig_height, orig_width = unpad_to_size
        cur_res = cur_res[:orig_height, :orig_width]

    cur_res = np.clip(cur_res * 255, 0, 255).astype('uint8')
    return cur_res