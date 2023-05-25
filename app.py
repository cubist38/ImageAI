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
            image, mask = segment_selected_object_on_image(image, coords)
            st.write(mask)
            remove_button = create_center_button(name = "Remove selected object")  
            st.image(mask, use_column_width=True)
            if remove_button:
                img_inpainted = remove_selected_object_on_image(image, mask)
                st.image(img_inpainted, use_column_width=True)
if __name__ == "__main__":
    main()