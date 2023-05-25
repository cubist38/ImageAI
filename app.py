import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates as st_image_coordinates

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "remove_anything"))
from remove import remove_selected_object_on_image, segment_selected_object_on_image
from engine import (draw_point_on_image, resize_pil_keep_aspect_ratio, 
                    create_center_button)

RADIUS = 10
def main():
    st.markdown("<h1 style='text-align: center; color: red;'>Our Magic Eraser</h1>", unsafe_allow_html=True)
    st.markdown("## Click on an object in the image, and our technique will remove it instantly!")
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        image = Image.open(image_file)
        image = resize_pil_keep_aspect_ratio(image, 640)
        coords = st_image_coordinates(image)
        if coords:
            image, mask, image_with_mask = segment_selected_object_on_image(image, coords)
            st.image(image_with_mask, use_column_width=True)
            dic = {"download": "Donwload this image with mask", "highlight": "Highlight this mask", "remove": "Remove selected object"}
            download, remove, highlight = create_center_button(name = dic, image_data = Image.fromarray(image_with_mask))  
            if remove:
                img_inpainted = remove_selected_object_on_image(image, mask)
                st.image(img_inpainted, use_column_width=True)
            elif highlight:
                pass
            else:
                pass
if __name__ == "__main__":
    main()