from PIL import ImageDraw
import numpy as np
import cv2
import streamlit as st

def upload_an_image():
    return st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

def draw_point_on_image(image, coords, radius = 10):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    x, y = coords
    draw.ellipse((x, y, x + radius, y + radius), fill='red')
    return img

def resize_with_aspect_ratio(image, max_width = 512):
    width, height = image.size
    aspect_ratio = height / width
    new_width = max_width
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))

def dilate_mask(mask, dilate_factor=15):
    mask = mask.astype(np.uint8)
    mask = cv2.dilate(
        mask,
        np.ones((dilate_factor, dilate_factor), np.uint8),
        iterations=1
    )
    return mask

def create_center_button(name: str):
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
        button = st.button(name)
    return button