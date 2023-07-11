from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.features.gen_des import generate_description
from app.features.segment import segment_selected_object_on_image
from app.features.remove import remove_selected_object_on_image
from app.features.blur import blur_image 
from app.features.gen_image import gen_image_from_prompt
from app.helpers.engine import numpy_to_base64, base64_to_numpy, pil_to_base64, base64_to_pil
from app.models.request import (SegmentationRequest, HighlightRequest, 
                                InpaintRequest, GenerateDescriptionRequest, GenerateImageRequest)
from PIL import Image
import numpy as np
from app.config import get_settings


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
async def generate_description_from_image(request: GenerateDescriptionRequest):
    image = request.image
    image = base64_to_numpy(image)
    des = generate_description(image)
    return {"Description": des}

@app.post("/segment_selected_object")
async def segment_selected_object(request: SegmentationRequest):
    image = request.image
    x = request.x
    y = request.y
    image = base64_to_numpy(image)
    image, mask, img_with_mask = segment_selected_object_on_image(image, x, y)
    img_b64 = numpy_to_base64(image)
    img_with_mask_b64 = numpy_to_base64(img_with_mask)
    return {"Image": img_b64, "Mask": mask.tolist(), "maskedImage": img_with_mask_b64}

@app.post("/inpaint_selected_object")
async def inpaint_selected_object(request: InpaintRequest):
    image = request.image
    mask = request.mask
    mask = np.array(mask, dtype = np.uint8)
    image = base64_to_numpy(image)
    img_inpainted = remove_selected_object_on_image(image, mask)
    img_inpainted_b64 = numpy_to_base64(img_inpainted)
    return {"Image": img_inpainted_b64}

@app.post("/generate_image")
async def generate_image_from_prompt(request: GenerateImageRequest):
    prompt = request.prompt
    image = gen_image_from_prompt(prompt)
    image_b64 = pil_to_base64(image)
    return {"Image": image_b64}

@app.post("/highlight_object") 
async def highlight_object(request: HighlightRequest):
    image = request.image
    mask = request.mask
    mask = np.array(mask, dtype = np.uint8)
    image = base64_to_numpy(image)
    blurred_img = blur_image(image, mask) 
    img_b64 = numpy_to_base64(blurred_img)
    return {"Image": img_b64}
