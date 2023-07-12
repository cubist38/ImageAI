import gdown
from tqdm import tqdm
import faiss
import numpy as np
from PIL import Image
import os 
import numpy as np
import logging

from app.helpers.encoder import ImageNTextEncoder
from app.dal.supabase_dao import SupabaseDAO
from app.helpers.image_helper import base64_to_image
from app.helpers.redis_helper import RedisHelper

PUBLIC_BUCKET = 'https://kghukcserwconiuwgboq.supabase.co/storage/v1/object/public/images/'
NUM_IMAGE_EACH_PAGE = 30

def get_faiss_by_user(email):   
  cached_urls, cached_index = RedisHelper().load_faiss(email)
  if ((cached_index is not None) and (cached_urls is not None)):
    logging.info(f'Loading cached faiss index of {email}')
    return cached_urls, cached_index

  images_url = [] 
  faiss_index = faiss.IndexFlatL2(256)

  images = SupabaseDAO().get_image_by_email(email) 
  for image in images: 
    embedded = np.array([image.embedded], dtype=np.float64)  
    faiss_index.add(embedded)
    images_url.append(f'{PUBLIC_BUCKET}{image.id}.{image.image.split(".")[-1]}')

  RedisHelper().save_faiss(email, images_url, faiss_index)

  return images_url, faiss_index

def retrieve_image_by_text(email, query, page): 
  ids = RedisHelper().load_search_result(email, query)
  images_url, faiss_index = get_faiss_by_user(email) 

  if (ids is None): 
    text_embedded = ImageNTextEncoder().encode_text(query)
    dists, ids = faiss_index.search(text_embedded, faiss_index.ntotal) 
    ids = ids[0]

    RedisHelper().save_search_result(email, query, ids)
  else: 
    logging.info(f'Loading cache of text search {email}, {query}')

  result = [] 
  for i in range(page * NUM_IMAGE_EACH_PAGE, (page + 1) * NUM_IMAGE_EACH_PAGE):  
    if (i >= len(ids)): 
      break
    result.append(images_url[ids[i]])
  return result 

def retrieve_image_by_image(email, image_b64, page): 
  ids = RedisHelper().load_search_result(email, image_b64)
  images_url, faiss_index = get_faiss_by_user(email) 

  if (ids is None): 
    image = base64_to_image(image_b64)
    image_embedded = np.array([ImageNTextEncoder().encode_image(image)], dtype=np.float64)
    dists, ids = faiss_index.search(image_embedded, faiss_index.ntotal) 
    ids = ids[0]

    RedisHelper().save_search_result(email, image_b64, ids)
  else: 
    logging.info(f'Loading cache of visual search {email}, {image_b64[:12]}')

  result = [] 
  for i in range(page * NUM_IMAGE_EACH_PAGE, (page + 1) * NUM_IMAGE_EACH_PAGE):  
    if (i >= len(ids)): 
      break
    result.append(images_url[ids[i]])
  return result 
