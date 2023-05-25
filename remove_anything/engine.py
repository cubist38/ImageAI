from PIL import ImageDraw
import numpy as np
import cv2
import streamlit as st

def draw_point_on_image(image, coords, radius = 10):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    x, y = coords
    draw.ellipse((x, y, x + radius, y + radius), fill='red')
    return img

def resize_pil_keep_aspect_ratio(image, max_size = 512):
    width, height = image.size
    if width > height:
        new_height = int(height * max_size / width)
        new_width = max_size
    else:
        new_width = int(width * max_size / height)
        new_height = max_size
    return image.resize((new_width, new_height))

def dilate_mask(mask, dilate_factor=15):
    mask = mask.astype(np.uint8)
    mask = cv2.dilate(
        mask,
        np.ones((dilate_factor, dilate_factor), np.uint8),
        iterations=1
    )
    return mask

def create_center_button(name: dict, image_data = None):
    # Apply CSS to center the button
    col1, col2, col3 = st.columns(3)
    with col1:
        download = st.download_button(name["download"], data=image_data, file_name='image_with_mask.png', mime='image/png')
    with col2 :
        remove = st.button(name["remove"])
    with col3:
        highlight = st.button(name["highlight"])
    return download, remove, highlight