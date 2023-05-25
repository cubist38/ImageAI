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