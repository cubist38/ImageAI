import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image

def dilate_mask(mask, dilate_factor=15):
    mask = mask.astype(np.uint8)
    mask = cv2.dilate(
        mask,
        np.ones((dilate_factor, dilate_factor), np.uint8),
        iterations=1
    )
    return mask

def numpy_to_base64(img):
    _, im_arr = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64

def pil_to_base64(img):
    im_file = BytesIO()
    img.save(im_file, format="JPEG")
    im_bytes = im_file.getvalue()
    im_b64 = base64.b64encode(im_bytes)
    return im_b64

def base64_to_pil(img):
    im_bytes = base64.b64decode(img) 
    im_file = BytesIO(im_bytes)
    img = Image.open(im_file)   
    return img

def base64_to_numpy(img):
    im_bytes = base64.b64decode(img)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  # im_arr is one-dim Numpy array
    img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
    return img

def expand_dim_mask(mask):
    mask = np.expand_dims(mask, axis=-1)
    mask = np.tile(mask, (1, 1, 3))
    return mask