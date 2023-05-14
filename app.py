import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image, ImageDraw

def draw_point_on_image(image, coords):
    img = Image.fromarray(image)
    draw = ImageDraw.Draw(img)
    draw.point((coords[0], coords[1]), fill="red")
    return img

def main():
    st.title("Image Cropper Demo")
    image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if image:
        cropped_image, coords = st_cropper(image=image, realtime_update=True, return_coords=True)
        st.image(draw_point_on_image(cropped_image, coords), caption="Cropped Image")
        st.write(f"Clicked at: {coords}")

if __name__ == "__main__":
    main()