import streamlit as st
import numpy as np
from PIL import Image

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    # Load the image and create a canvas
    image = Image.open(uploaded_file)
    # Create a canvas element
    st.image(image)

# Create a canvas element
canvas = st.empty()

# Add an event listener to the canvas element to detect when the user clicks on it
def on_click(event):
  x = event.x
  y = event.y

  # Draw a point at the coordinates of the click
  canvas.fill_rect((x - 5, y - 5, 10, 10), "red")

canvas.on_change(on_click)

# # Display the image with the clickable images component
# clicked_image = clickable_images([image], canvas=canvas)