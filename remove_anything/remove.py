import numpy as np
import torch
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).resolve().parent / "remove_anything"))
from lama_model import load_lama_model, inpaint_img_with_builded_lama
from sam_model import load_sam_model, predict_masks_with_sam
from engine import dilate_mask

def segment_selected_object_on_image(image, coords):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu") 
    if image.mode == "RGBA":
        image = image.convert("RGB")   
    with open('./remove_anything/config.json', 'r') as f:
        config = json.load(f)
    predictor = load_sam_model(config["sam_model"]["model_type"], 
                                config["sam_model"]["ckpt_p"], 
                                device)
    image =  np.array(image)
    masks, scores, logits = predict_masks_with_sam(image,
        [[int(coords["x"]), int(coords["y"])]],
        [1],
        predictor)
    masks = masks.astype(np.uint8) * 255
    mask = masks[np.argmax(scores)]
    mask = dilate_mask(mask, 15)
    image_with_mask = image.copy()
    color = np.array([0, 0, 255])
    image_with_mask[mask == 255] = color

    return image, mask, image_with_mask

def remove_selected_object_on_image(image, mask):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")    
    with open('./remove_anything/config.json', 'r') as f:
        config = json.load(f)
    lama_model = load_lama_model(
                    config_p = config["lama_model"]["config_p"], 
                    ckpt_p = config["lama_model"]["ckpt_p"], 
                    device = device
                )
    img_inpainted = inpaint_img_with_builded_lama(lama_model, image, mask, config_p = "lama/configs/prediction/default.yaml")
    return img_inpainted