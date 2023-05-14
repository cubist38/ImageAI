import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    # Load the image and create a canvas
    image = Image.open(uploaded_file)
    canvas = st_canvas(
        width=image.width,
        height=image.height,
        image_mode='RGB'
    )

    # Display the image and wait for the user to click
    st.image(image)
    if canvas.clicked:
        x, y = canvas.coordinates
        st.write(f"You clicked at ({x}, {y})")