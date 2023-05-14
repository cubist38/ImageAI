import streamlit as st

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    # Do something with the image, e.g. display it
    st.image(uploaded_file)