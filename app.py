import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from segment_anything import SamPredictor, sam_model_registry
from PIL import Image, ImageDraw
import numpy as np
import torch
import cv2
from sam_segment import predict_masks_with_sam
from utils import dilate_mask
from lama_inpaint import build_lama_model, inpaint_img_with_builded_lama

def create_center_button():
    # Apply CSS to center the button
    col1, col2, col3 , col4, col5 = st.columns(5)
    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        pass
    with col3 :
        remove_button = st.button('Remove', key='my_button')
    return remove_button

def dilate_mask(mask, dilate_factor=15):
    mask = mask.astype(np.uint8)
    mask = cv2.dilate(
        mask,
        np.ones((dilate_factor, dilate_factor), np.uint8),
        iterations=1
    )
    return mask

RADIUS = 5

def draw_point_on_image(image, coords, radius = 10):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    x, y = coords
    draw.ellipse((x, y, x + radius, y + radius), fill='red')
    return img

def resize_with_aspect_ratio(image, max_width = 640):
    width, height = image.size
    aspect_ratio = height / width
    new_width = max_width
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))

@st.cache_resource
def load_sam_model(sam_model_type, sam_model_path, device):
    sam = sam_model_registry[sam_model_type](checkpoint=sam_model_path)
    sam.to(device=device)
    predictor = SamPredictor(sam)
    return predictor

@st.cache_resource
def load_lama_model(
        config_p: str, 
        ckpt_p: str,
        device = "cuda"):
    return build_lama_model(config_p, ckpt_p, device)

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    st.title("Remove anything from an image")
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        image = Image.open(image_file)
        image = resize_with_aspect_ratio(image, 700)
        coords = streamlit_image_coordinates(image)
        if coords:
            st.write("Coordinates: ", coords)
            st.image(draw_point_on_image(image, (int(coords["x"]), int(coords["y"])), radius = RADIUS), use_column_width=True)        
            remove_button = create_center_button()
            if remove_button:
                if image.mode == "RGBA":
                    image = image.convert("RGB")
                image =  np.array(image)
                predictor = load_sam_model("vit_h", 
                                            "/content/drive/MyDrive/InpaintAnything/Weights/sam_vit_h_4b8939.pth", 
                                            device)
                st.write("SAM model loaded!")
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

if __name__ == "__main__":
    main()