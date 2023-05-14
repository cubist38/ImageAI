import streamlit as st
from PIL import Image
from st_clickable_images import clickable_images
import io
import base64

# Define a function to convert the uploaded image to a byte stream
def image_to_byte_array(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

def bytestream_to_base64(bytestream):
    return base64.b64encode(img_byte_arr).decode()

# Define the on_click callback function
def on_click(x, y):
    st.write("Clicked at", x, y)

# Display a file uploader to upload an image
uploaded_file = st.file_uploader("Upload an image here", type=["jpg", "jpeg", "png"])


# If an image is uploaded
if uploaded_file is not None:
    # Load the image
    image = Image.open(uploaded_file)
    
    # Convert the image to a byte stream
    img_byte_arr = image_to_byte_array(image)
    img_base64 = bytestream_to_base64(img_byte_arr)

    # Display the clickable image
    st.image(img_base64, use_column_width=True, caption="Click me!")
    if st.button("Click me!"):
        on_click(0, 0)
