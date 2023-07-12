from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware

from app.helpers.encoder import ImageNTextEncoder
from app.helpers.engine import (numpy_to_base64, base64_to_numpy, 
                                pil_to_base64, base64_to_pil, expand_dim_mask)
from app.helpers.google_helper import GoogleHelper

from app.features.gen_des import generate_description
from app.features.segment import segment_selected_object_on_image
from app.features.remove import remove_selected_object_on_image
from app.features.blur import blur_image
from app.features.gen_image import gen_image_from_prompt
from app.features.image_retrieval import retrieve_image_by_image, retrieve_image_by_text

from app.dal.supabase_dao import SupabaseDAO
from app.models.request import (SegmentationRequest, HighlightRequest,
                                InpaintRequest, GenerateDescriptionRequest, GenerateImageRequest,
                                StorageRequest, ImportStorageRequest, ImageStorageRequest, 
                                TextSearchRequest, VisualSearchRequest)

from app.config import get_settings

# Initialize for singleton instance 
GoogleHelper()
ImageNTextEncoder()

PUBLIC_BUCKET = 'https://kghukcserwconiuwgboq.supabase.co/storage/v1/object/public/images/'

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
    image = base64_to_pil(image)
    if image.mode == "RGBA":
        image = image.convert("RGB") 
    des = generate_description(image)
    return {"Description": des}


@app.post("/segment_selected_object")
async def segment_selected_object(request: SegmentationRequest):
    image = request.image
    x = request.x
    y = request.y
    image = base64_to_numpy(image)
    image, mask, img_with_mask = segment_selected_object_on_image(image, x, y)
    mask = expand_dim_mask(mask)
    img_b64 = numpy_to_base64(image)
    mask_b64 = numpy_to_base64(mask)
    img_with_mask_b64 = numpy_to_base64(img_with_mask)
    return {"Image": img_b64, "Mask": mask_b64, "maskedImage": img_with_mask_b64}


@app.post("/inpaint_selected_object")
async def inpaint_selected_object(request: InpaintRequest):
    image = request.image
    mask = request.mask
    image = base64_to_numpy(image)
    mask = base64_to_numpy(mask)
    mask = mask[:, :, 0]
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
    image = base64_to_numpy(image)
    mask = base64_to_numpy(mask)
    mask = mask[:, :, 0]
    blurred_img = blur_image(image, mask) 
    img_b64 = numpy_to_base64(blurred_img)
    return {"Image": img_b64}


@app.post("/storage")
async def storage(request: StorageRequest):
    # TODO: Check authorization
    storages_url = SupabaseDAO().get_storage_by_email('temp_email')
    return {"urls": [item.storage_url for item in storages_url]}


@app.post("/images")
async def process_images(request: ImageStorageRequest):
    # TODO: Check authorization
    images_url = SupabaseDAO().get_image_by_storage_url(request.storage_url)
    return {"urls": [f'{PUBLIC_BUCKET}{item.id}.{item.image.split(".")[-1]}' for item in images_url]}


@app.post("/import_storage")
async def import_storage(request: ImportStorageRequest, response: Response):
    # TODO: Check authorization
    result = GoogleHelper().import_storage('temp_email', request.storage_url)

    if (result):
        response.status_code = 200
        return {"message": "Import storage completed"}
    else:
        response.status_code = 400
        return {"message": "Fail to import storage"}

@app.post("/text_search")
async def text_search(request: TextSearchRequest, response: Response):
    result = retrieve_image_by_text('temp_email', request.query, request.page)
    return {'urls': result}

@app.post("/visual_search")
async def visual_search(request: VisualSearchRequest, response: Response):
    result = retrieve_image_by_image('temp_email', request.image, request.page)
    return {'urls': result}
    
# Initialization for singleton 
temp = GoogleHelper() 
temp = ImageNTextEncoder() 
temp = SupabaseDAO()