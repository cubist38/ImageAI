import streamlit as st
from remove import remove_on_clicked
from PIL import Image
from engine import (resize_with_aspect_ratio, 
                    draw_point_on_image, create_center_button)
from streamlit_image_coordinates import streamlit_image_coordinates as st_image_coordinates

features = ['Remove Anything Image', 'Remove Anything Video', 'Replace Anything']
RADIUS = 5

def main():
    st.markdown("<h1 style='text-align: center; color: red;'>Final Project</h1>", unsafe_allow_html=True)
    feature = st.selectbox('Choose a feature to use', features)
    if feature == 'Remove Anything Image':
        st.markdown("# Click on an object in the image, and Inpainting Anything will remove it instantly!")
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
    elif feature == 'Remove Anything Video':
        st.write("With a single click on an object in the first video frame, Remove Anything Video can remove the object from the whole video!")
if __name__ == "__main__":
    main()