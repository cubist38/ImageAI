from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.features.gen_des import generate_description
from app.features.segment import segment_selected_object_on_image
from PIL import Image
import io
from app.config import get_settings
import base64
import cv2


app = FastAPI()
config_settings = get_settings()

allowed_origins = ['*']
allowed_methods = ['GET', 'POST']
allowed_headers = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers,
)


@app.get("/")
async def root():
    return config_settings

@app.post("/generate_description")
async def generate_description(file: UploadFile = File(...)):
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
    _, img_with_mask = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = img_with_mask.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return {"Masked image": im_b64}

    