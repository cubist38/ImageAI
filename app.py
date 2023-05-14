import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw
import numpy as np
import torch
from InpaintAnything.utils import dilate_mask, show_mask
from InpaintAnything.sam_segment import predict_masks_with_sam


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

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    st.title("Image Cropper Demo")
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        image = Image.open(image_file)
        image = resize_with_aspect_ratio(image)
        coords = streamlit_image_coordinates(image)
        if coords:
            if image.mode == "RGBA":
                image = image.convert("RGB")
            image =  np.array(image)
            masks, scores, logits = predict_masks_with_sam(
                image,
                [(int(coords["x"]), int(coords["y"]))],
                1,
                model_type= "vit_h",
                ckpt_p = "/content/drive/MyDrive/InpaintAnything/Weights/sam_vit_h_4b8939.pth",
                device = device,
            )
            masks = masks.astype(np.uint8) * 255
            masks = [dilate_mask(mask, 15) for mask in masks]
            # find mask with highest score
            mask = masks[np.argmax(scores)]
            st.image(mask)

if __name__ == "__main__":
    main()