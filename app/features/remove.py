import torch
import numpy as np
from app.features.config import get_settings
from app.helpers.load_lama import load_lama_model
from models.lama.saicinpainting.evaluation.data import pad_tensor_to_modulo
from models.lama.saicinpainting.evaluation.utils import move_to_device


config = get_settings()

@torch.no_grad()
def inpaint_img_with_built_lama(
        model,
        img: np.ndarray,
        mask: np.ndarray,
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

def remove_selected_object_on_image(image, mask):
    lama_model = load_lama_model(
                    config_p = config.lama_model_config_p, 
                    ckpt_p = config.lama_model_ckpt_p, 
                    device = config.device
                )
    img_inpainted = inpaint_img_with_built_lama(lama_model, 
                                                image, 
                                                mask
                                            )      
    return img_inpainted