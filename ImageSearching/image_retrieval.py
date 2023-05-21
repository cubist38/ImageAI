import gdown
from tqdm import tqdm
from encoder import ImageNTextEncoder
import faiss
import numpy as np
from PIL import Image
import os 

class ImageHelper(): 
  def __init__(self) -> None:
    pass

  @staticmethod
  def download_folder_drive(url): 
    gdown.download_folder(url, output='temp', quiet=True, use_cookies=False)

  @staticmethod 
  def load_image_from_path(path): 
    try: 
      image = Image.open(path).convert('RGB')
      return image
    except IOError: 
      return None 
  
  @staticmethod
  def load_image_from_folder(path): 
    if (not os.path.isdir(path)): 
      return []
    
    images = []
    images_path = []
    for image_path in os.listdir(path):
      image = ImageHelper.load_image_from_path(os.path.join(path, image_path)) 
      if (image == None): 
        continue 
      images.append(image)
      images_path.append(image_path)

    return images, images_path

class ImageRetrieval(): 
  def __init__(self, model_name = 'blip_feature_extractor', model_type='base') -> None:
    self.encoder = ImageNTextEncoder(model_name=model_name, model_type=model_type) 
    self.index = faiss.IndexFlatL2(256)
    self.images_path = []

  def insert_images(self, images, images_path): 
    for id, image in tqdm(enumerate(images)): 
      embedded = self.encoder.encode_image(image)
      self.index.add(embedded) 
      self.images_path.append(images_path[id]) 

  def search_images(self, text, limit = 10): 
    text_feature = self.encoder.encode_text(text) 
    dists, ids = self.index.search(text_feature, k = limit) 
    return [self.images_path[id] if id != -1 else '' for id in ids[0]] 
  
if __name__ == '__main__': 
  temp = ImageRetrieval() 
  images, images_path = ImageHelper.load_image_from_folder('./images')
  temp.insert_images(images, images_path)
  result = temp.search_images('a star')
  print(result)
