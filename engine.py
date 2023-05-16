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
        aspect_ratio = width / height
        new_width = max_size
        new_height = int(new_width / aspect_ratio)
    else:
        aspect_ratio = height / width
        new_height = max_size
        new_width = int(new_height / aspect_ratio)
    return image.resize((new_width, new_height))

def dilate_mask(mask, dilate_factor=15):
    mask = mask.astype(np.uint8)
    mask = cv2.dilate(
        mask,
        np.ones((dilate_factor, dilate_factor), np.uint8),
        iterations=1
    )
    return mask

def resize_rgb_keep_aspect_ratio(image, max_size = 512):
    width, height, _ = image.shape
    if width > height:
        aspect_ratio = width / height
        new_width = max_size
        new_height = int(new_width / aspect_ratio)
    else:
        aspect_ratio = height / width
        new_height = max_size
        new_width = int(new_height / aspect_ratio)
    return cv2.resize(image, (new_width, new_height))


def create_center_button(name: str):
    # Apply CSS to center the button
    col1, col2, col3 = st.columns(3)
    with col1:
        pass
    with col3:
        pass
    with col2 :
        button = st.button(name)
    return button