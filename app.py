import streamlit as st
from remove import remove_selected_object_on_image, remove_selected_object_on_video
from PIL import Image
from engine import (resize_pil_keep_aspect_ratio, 
                    load_raw_video, draw_point_on_image, create_center_button, write_bytesio_to_file)
from streamlit_image_coordinates import streamlit_image_coordinates as st_image_coordinates
import tempfile

features = ['Remove Anything Image', 'Remove Anything Video', 'Replace Anything']
RADIUS = 5

def main():
    st.markdown("<h1 style='text-align: center; color: red;'>Our Magic Eraser</h1>", unsafe_allow_html=True)
    feature = st.selectbox('Choose a feature to use', features)
    if feature == 'Remove Anything Image':
        st.markdown("## Click on an object in the image, and our technique will remove it instantly!")
        image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
        if image_file is not None:
            image = Image.open(image_file)
            image = resize_pil_keep_aspect_ratio(image, 640)
            coords = st_image_coordinates(image)
            if coords:
                st.write("Coordinates: ", coords)
                st.image(draw_point_on_image(image, (int(coords["x"]), int(coords["y"])), radius = RADIUS), use_column_width=True)  
                remove_button = create_center_button(name = "Remove selected object")  
                if remove_button:
                    img_inpainted = remove_selected_object_on_image(image, coords)
                    st.image(img_inpainted, use_column_width=True)
    elif feature == 'Remove Anything Video':
        st.markdown("## With a single click on an object in the first video frame, our technique can remove the object from the whole video!")
        video_file = st.file_uploader("Upload a video", type=["mp4", "mov", "gif"])
        if video_file is not None:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(video_file.read())
            frames_p, fps, first_frame = load_raw_video(tfile.name)
            first_frame = Image.fromarray(first_frame)
            coords = st_image_coordinates(first_frame)
            if coords:
                st.write("Coordinates: ", coords)
                st.image(draw_point_on_image(first_frame, (int(coords["x"]), int(coords["y"])), radius = RADIUS), use_column_width=True)  
                remove_button = create_center_button(name = "Remove selected object")  
                if remove_button:
                    output_file = remove_selected_object_on_video(frames_p, coords, fps)
                    st.video(output_file)
if __name__ == "__main__":
    main()