import gdown
from tqdm import tqdm
from app.helpers.encoder import ImageNTextEncoder
import faiss
import numpy as np
from PIL import Image
import os 

class ImageRetrieval(): 
  _instance = None

  def __new__(cls, model_name = 'blip_feature_extractor', model_type='base'):
    if cls._instance is None:
      cls._instance = super().__new__(cls)

      cls._instance.encoder = ImageNTextEncoder(model_name=model_name, model_type=model_type) 

    return cls._instance

  def insert_images(self, images, images_path): 
    for id, image in tqdm(enumerate(images)): 
      embedded = self.encoder.encode_image(image)
      self.index.add(embedded) 
      self.images_path.append(images_path[id]) 

  def search_images(self, text, limit = 10): 
    text_feature = self.encoder.encode_text(text) 
    dists, ids = self.index.search(text_feature, k = limit) 
    return [self.images_path[id] if id != -1 else '' for id in ids[0]] 