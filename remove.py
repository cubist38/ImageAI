import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from utils import dilate_mask
from lama_model import load_lama_model, inpaint_img_with_builded_lama
from PIL import Image
from sam_model import load_sam_model, predict_masks_with_sam
from utils import draw_point_on_image, create_center_button
import numpy as np
import torch

RADIUS = 5

def resize_with_aspect_ratio(image, max_width = 512):
    width, height = image.size
    aspect_ratio = height / width
    new_width = max_width
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))

def remove_on_clicked(image_file):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    image = Image.open(image_file)
    image = resize_with_aspect_ratio(image, 700)
    coords = streamlit_image_coordinates(image)
    if coords:
        st.write("Coordinates: ", coords)
        st.image(draw_point_on_image(image, (int(coords["x"]), int(coords["y"])), radius = RADIUS), use_column_width=True)        
        remove_button = create_center_button(name = "Remove")
        if remove_button:
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
            st.image(img_inpainted, use_column_width=True)
    