import streamlit as st
from PIL import Image
import requests

# streamlit run app.py --server.port 80

## Use the full page instead of a narrow central column
st.set_page_config(layout="wide")
st.title('ImageAI')


## Session state
if 'image' not in st.session_state:
	st.session_state.image = None

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )

tab1, tab2, tab3 = st.tabs(["Cat", "Dog", "Owl"])

with tab1:
   st.header("A cat")
   st.image("https://static.streamlit.io/examples/cat.jpg", width=200)

with tab2:
   st.header("A dog")
   st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

with tab3:
   st.header("An owl")
   st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

## Form uploading image
with st.form("my-form", clear_on_submit=True):
    uploaded_file = st.file_uploader("Choose an image...", type="jpg", key='btn-upload-image')
    submitted = st.form_submit_button("Upload")
    if submitted and uploaded_file is not None:
        st.write("UPLOADED!")
        st.session_state.image = Image.open(uploaded_file)
        # do stuff with your uploaded file

# Display image
if st.session_state.image is not None:
    image = st.session_state.image
    #image = image.resize((600, 400))
    st.image(image)

st.title("Image gallery")
n = st.number_input("Select Grid Width", 1, 5, 3)

image_paths = [
  'https://images.unsplash.com/photo-1575936123452-b67c3203c357?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aW1hZ2V8ZW58MHx8MHx8fDA%3D&w=1000&q=80',
  'https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg',
  'https://imglarger.com/Images/before-after/ai-image-enlarger-1-after-2.jpg',
  'https://imgv3.fotor.com/images/blog-cover-image/part-blurry-image.jpg'
]

images = [ Image.open(requests.get(path, stream=True).raw) for path in image_paths ]

def choose_image_event(image):
    st.session_state.image = image
    #st.write('Clicked on ', image_paths[grIdx * n + i])
    #st.experimental_rerun()

groups = []
for i in range(0, len(images), n):
    groups.append(images[i:i+n])

for grIdx, group in enumerate(groups):
    cols = st.columns(n)
    for i, image_file in enumerate(group):
      with cols[i]:
        st.button('Choose this image', key = grIdx * n + i, on_click=choose_image_event, args=(images[grIdx * n + i], ))
        st.image(image_file)
        
