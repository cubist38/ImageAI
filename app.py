import streamlit as st
from remove import remove_selected_object_on_image, remove_selected_object_on_video
from PIL import Image
from engine import (resize_pil_keep_aspect_ratio, 
                    load_raw_video, draw_point_on_image, create_center_button, write_bytesio_to_file)
from streamlit_image_coordinates import streamlit_image_coordinates as st_image_coordinates
from image_caption import ImageCaptioner
import os

features = ['Remove Anything Image', 'Remove Anything Video', 'Replace Anything', 'Write image caption']
RADIUS = 5

imageCaptioner = None

def main():
    global imageCaptioner
    st.markdown("<h1 style='text-align: center; color: red;'>Our Magic Eraser</h1>", unsafe_allow_html=True)
    feature = st.selectbox('Choose a feature to use', features)
    st.write('feature: ' + feature)
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
            write_bytesio_to_file("video.mp4", video_file)
            frames_p, fps = load_raw_video("video.mp4")  
            os.remove("video.mp4") 
            first_frame = Image.open(frames_p[0])
            first_frame = first_frame.convert("RGB")
            coords = st_image_coordinates(first_frame)
            if coords:
                st.write("Coordinates: ", coords)
                st.image(draw_point_on_image(first_frame, (int(coords["x"]), int(coords["y"])), radius = RADIUS), use_column_width=True)  
                remove_button = create_center_button(name = "Remove selected object")  
                if remove_button:
                    output_file = remove_selected_object_on_video(frames_p, coords, fps)
                    st.video(output_file)
    elif feature == 'Write image caption':
        st.markdown("## With a single click on an object in the first video frame, our technique can remove the object from the whole video!")
        uploaded_file = st.file_uploader("Choose an image...", type="jpg")
        if uploaded_file is not None:
            raw_img = Image.open(uploaded_file)
            st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)

            if imageCaptioner is None:
                imageCaptioner = ImageCaptioner()
            result_caption = imageCaptioner.generate_caption(raw_img)
            st.subheader("Results")
            st.write(result_caption)
        
if __name__ == "__main__":
    main()