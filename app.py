import streamlit as st
from remove import remove_on_clicked

def upload_an_image():
    return st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

def main():
    if st.button("Remove Anything"):
        st.write("Click on an object in the image, and Inpainting Anything will remove it instantly!")
        image_file = upload_an_image()
        if image_file is not None:
            remove_on_clicked(image_file)
    if st.button("Fill Anything"):
        st.write("Click on an object, type in what you want to fill, and Inpaint Anything will fill it!")

if __name__ == "__main__":
    main()