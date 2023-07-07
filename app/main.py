from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.features.gen_des import generate_description
from app.features.segment import segment_selected_object_on_image
from app.features.remove import remove_selected_object_on_image
from app.features.gen_image import gen_image_from_prompt
from app.helpers.engine import numpy_to_base64, base64_to_numpy, pil_to_base64
from PIL import Image
import io
from app.config import get_settings


app = FastAPI()
config_settings = get_settings()

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Add more allowed origins as needed
]
allowed_methods = ['GET', 'POST']
allowed_headers = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers,
)


@app.get("/")
async def root():
    return config_settings

@app.post("/generate_description")
async def generate_description_from_image(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    des = generate_description(img)
    return {"Description": des}

@app.post("/segment_selected_object")
async def segment_selected_object(file: UploadFile = File(...), 
                                  x: str = "0",
                                  y: str = "0"):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img, mask, img_with_mask = segment_selected_object_on_image(img, x, y)
    img_b64 = numpy_to_base64(img)
    mask_b64 = numpy_to_base64(mask)
    img_with_mask_b64 = numpy_to_base64(img_with_mask)
    return {"Image": img_b64, "Mask": mask_b64, "Masked image": img_with_mask_b64}

@app.post("/remove_selected_object")
async def remove_selected_object(image, mask):
    image = base64_to_numpy(image)
    mask = base64_to_numpy(mask)
    img_inpainted = remove_selected_object_on_image(image, mask)
    img_inpainted_b64 = numpy_to_base64(img_inpainted)
    return {"Image": img_inpainted_b64}

@app.post("/generate_image")
async def generate_image_from_prompt(prompt: str):
    image = gen_image_from_prompt(prompt)
    image_b64 = pil_to_base64(image)
    return {"Image": image_b64}