from PIL import ImageDraw
import numpy as np
import cv2
import streamlit as st
import tempfile
import imageio.v2 as iio
import imageio
import os
from pathlib import Path
from skimage.transform import resize

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

def resize_imageio_keep_aspect_ratio(image, max_size = 512):
    height, width, _ = image.shape
    if width > height:
        new_height = int(height * max_size / width)
        new_width = max_size
    else:
        new_width = int(width * max_size / height)
        new_height = max_size
    return resize(image, (new_height, new_width))


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

# func to save BytesIO on a drive
def write_bytesio_to_file(filename, bytesio):
    """
    Write the contents of the given BytesIO to a file.
    Creates the file or overwrites the file if it does
    not exist yet. 
    """
    with open(filename, "wb") as outfile:
        # Copy the BytesIO stream to the output file
        outfile.write(bytesio.getbuffer())

def mkstemp(suffix, dir=None):
    fd, path = tempfile.mkstemp(suffix=f"{suffix}", dir=dir)
    os.close(fd)
    return Path(path)

def load_raw_video(video_raw_p):
    all_frame = iio.mimread(video_raw_p, memtest=False)
    fps = cv2.VideoCapture(video_raw_p).get(cv2.CAP_PROP_FPS)
    # tmp frames
    frame_ps = []
    for i in range(len(all_frame)):
        frame_p = str(mkstemp(suffix=f"{i:0>6}.png"))
        frame_ps.append(frame_p)
        all_frame[i] = resize_imageio_keep_aspect_ratio(all_frame[i], 384)
        iio.imwrite(frame_ps[i], all_frame[i])
    return frame_ps, fps
        
    