import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    # Load the image and create a canvas
    image = Image.open(uploaded_file)
    # Create a canvas element
    st.image(image)

canvas = st.empty()
def on_click(event):
    x = event.x
    y = event.y
    # Draw a point at the coordinates of the click
    print(x, y)
    canvas.fill_rect((x - 5, y - 5, 10, 10), "red")

canvas.on_event("click", on_click)