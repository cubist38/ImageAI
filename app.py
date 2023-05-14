import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

def draw_point_on_image(image, coords):
    img = image.copy()
    print(coords)
    draw = ImageDraw.Draw(img)
    draw.point(coords, fill="red")
    return img

def main():
    st.title("Image Cropper Demo")
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        image = Image.open(image_file)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        coords = streamlit_image_coordinates(image)
        st.write("Coordinates: ", coords)
        cropped_image = draw_point_on_image(image, coords)
        st.image(cropped_image, caption="Cropped Image")
        st.write(f"Clicked at: {coords}")

if __name__ == "__main__":
    main()