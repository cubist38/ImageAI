from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.features.gen_des import generate_description
from PIL import Image
import io
from app.config import get_settings
from fastapi.logger import logger
from pyngrok import ngrok
import sys


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

# @app.post("/generate_image")
# async def generate_image(file: bytes = File(...)):
#     # image = Image.open(io.BytesIO(file)).convert("RGB")
#     # results = generate_description(image)
#     return {"name": "test"}

# @app.post("/generate_image")
# async def generate_image(name: str = "test"):
#     # Your image generation logic here
#     # This could involve processing data, generating an image, and returning it
#     # You can use libraries like PIL, OpenCV, or any other image processing library
#     return {"name": name}

@app.post("/generate_image")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    # Perform operations with the image using Pillow
    # For example, you can resize the image
    des = generate_description(img)
    return {"Description": des}


if config_settings.USE_NGROK:
    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
    public_url = ngrok.connect(port).public_url
    logger.info("ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))
    config_settings.BASE_URL = public_url
