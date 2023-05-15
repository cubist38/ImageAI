import streamlit as st
from remove import remove_on_clicked
from PIL import Image
from engine import (resize_with_aspect_ratio, upload_an_image, 
                    draw_point_on_image, create_center_button)
from streamlit_image_coordinates import streamlit_image_coordinates as st_image_coordinates


RADIUS = 5

def main():
    if st.button("Remove Anything"):
        st.write("Click on an object in the image, and Inpainting Anything will remove it instantly!")
        image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if image_file is not None:
            image = Image.open(image_file)
            image = resize_with_aspect_ratio(image, 700)
            coords = st_image_coordinates(image)
            if coords:
                st.write("Coordinates: ", coords)
                st.image(draw_point_on_image(image, (int(coords["x"]), int(coords["y"])), radius = RADIUS), use_column_width=True)  
                remove_button = create_center_button(name = "Remove")  
                if remove_button:
                    img_inpainted = remove_on_clicked(image, coords)
                    st.image(img_inpainted, use_column_width=True)

if __name__ == "__main__":
    main()