import streamlit as st
from PIL import Image


# Display a file uploader to upload an image
uploaded_file = st.file_uploader("Upload an image here", type=["jpg", "jpeg", "png"])


# If an image is uploaded
if uploaded_file is not None:
    # Load the image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Get user click position
    click_pos = st.session_state.get('click_pos')
    if click_pos is not None:
        st.write("You clicked at:", click_pos)

    # Add click handler to image
    if st.button("Click on the image"):
        click_pos = st.mouse_clicks.add(click_data=image)
        st.session_state['click_pos'] = click_pos