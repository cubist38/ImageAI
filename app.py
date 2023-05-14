import streamlit as st
from PIL import Image
from st_clickable_images import clickable_images


uploaded_file = st.file_uploader("Choose an image...", type= ["jpg", "png", "jpeg"])

def on_image_click(x, y):
    st.write("You clicked on the image at coordinates:", x, y)

if uploaded_file is not None:
    # Load the image and create a canvas
    image = Image.open(uploaded_file)
    # Create a canvas element
    st.image(image)
    st_clickable_image = clickable_images(image, on_image_click)

    # Display the clickable image
    if st_clickable_image is not None:
        st.write(st_clickable_image)

