import streamlit as st
from lama_model import load_lama_model, inpaint_img_with_builded_lama
from sam_model import load_sam_model, predict_masks_with_sam
from engine import create_center_button, dilate_mask
import numpy as np
import torch

def remove_on_clicked(image, coords):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")    
    if image.mode == "RGBA":
        image = image.convert("RGB")
    image =  np.array(image)
    predictor = load_sam_model("vit_h", 
                                "/content/drive/MyDrive/InpaintAnything/Weights/sam_vit_h_4b8939.pth", 
                                device)
    masks, scores, logits = predict_masks_with_sam(image,
        [[int(coords["x"]), int(coords["y"])]],
        [1],
        predictor)
    masks = masks.astype(np.uint8) * 255
    mask = masks[np.argmax(scores)]
    mask = dilate_mask(mask, 15)
    lama_model = load_lama_model(
                    config_p = "lama/configs/prediction/default.yaml", 
                    ckpt_p = "/content/drive/MyDrive/InpaintAnything/Weights/big-lama", 
                    device = device
                )
    img_inpainted = inpaint_img_with_builded_lama(lama_model, image, mask, config_p = "lama/configs/prediction/default.yaml")
    return img_inpainted