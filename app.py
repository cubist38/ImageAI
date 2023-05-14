import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

def draw_point_on_image(image, coords):
    img = image.copy()
    draw = ImageDraw.Draw(img)
    draw.point(coords, fill="red")
    return img

def resize_with_aspect_ratio(image, max_width = 640):
    width, height = image.size
    aspect_ratio = height / width
    new_width = max_width
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))

def main():
    st.title("Image Cropper Demo")
    image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image_file is not None:
        image = Image.open(image_file)
        image = resize_with_aspect_ratio(image)
        coords = streamlit_image_coordinates(image)
        if coords:
            st.write(coords)
            st.image(draw_point_on_image(image, (int(coords["x"]), int(coords["y"]))), caption="Selected point", use_column_width=True)

if __name__ == "__main__":
    main()