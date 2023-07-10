import gdown
from tqdm import tqdm
import faiss
import numpy as np
from PIL import Image
import os 
import pickle

from app.helpers.encoder import ImageNTextEncoder
from app.dal.supabase_dao import SupabaseDAO
from app.helpers.image_helper import base64_to_image

PUBLIC_BUCKET = 'https://kghukcserwconiuwgboq.supabase.co/storage/v1/object/public/images/'
NUM_IMAGE_EACH_PAGE = 30

def get_faiss_by_user(email):   
  images_url = [] 
  faiss_index = faiss.IndexFlatL2(256)

  images = SupabaseDAO().get_image_by_email(email) 
  for image in images: 
    embedded = pickle.loads(image.encode)  
    faiss_index.add(embedded)
    images_url.append(f'{PUBLIC_BUCKET}{image.id}.{image.image.split(".")[-1]}')

  return images_url, faiss_index

def retrieve_image_by_text(email, query, page): 
  text_embedded = ImageNTextEncoder().encode_text(query) 
  images_url, faiss_index = get_faiss_by_user(email) 
  dists, ids = faiss_index.search(text_embedded) 
  result = [] 
  for i in range(page * NUM_IMAGE_EACH_PAGE, (page + 1) * NUM_IMAGE_EACH_PAGE):  
    if (i >= len(ids)): 
      break
    result.append(images_url[ids[i]])
  return result 

def retrieve_image_by_image(email, image_b64, page): 
  image = base64_to_image(image_b64)
  image_embedded = ImageNTextEncoder().encode_image(image) 
  images_url, faiss_index = get_faiss_by_user(email) 
  dists, ids = faiss_index.search(image_embedded) 
  result = [] 
  for i in range(page * NUM_IMAGE_EACH_PAGE, (page + 1) * NUM_IMAGE_EACH_PAGE):  
    if (i >= len(ids)): 
      break
    result.append(images_url[ids[i]])
  return result 
    