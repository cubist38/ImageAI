import torch
from lavis.models import load_model_and_preprocess
from app.helpers.image_helper import load_image_from_path
import numpy as np

device = torch.device('cuda') if torch.cuda.is_available() else 'cpu'

class ImageNTextEncoder():
  _instance = None

  def __new__(cls, model_name='blip_feature_extractor', model_type='base'):
    if cls._instance is None:
      cls._instance = super().__new__(cls)
      cls._instance.model, cls._instance.vis_processors, cls._instance.txt_processors = load_model_and_preprocess(name=model_name, model_type=model_type, is_eval=True, device=device)

    return cls._instance

  def encode_text(self, text): 
    text_input = self.txt_processors['eval'](text)
    sample = {'text_input': [text_input]}
    features_text = self.model.extract_features(sample, mode='text')
    if (device == 'cpu'): 
      return (features_text.text_embeds_proj[0, 0:1, :]).numpy()
    else:
      return (features_text.text_embeds_proj[0, 0:1, :]).cpu().numpy()
  
  def encode_image_by_path(self, image_path): 
    image = load_image_from_path(image_path)
    return self.encode_image(image)
  
  def encode_image(self, image): 
    image = self.vis_processors['eval'](image).unsqueeze(0).to(device)
    sample = {'image': image}
    features_image = self.model.extract_features(sample, mode='image')
    if (device == 'cpu'): 
      return (features_image.image_embeds_proj[0, 0:1, :]).numpy()[0]
    else: 
      return (features_image.image_embeds_proj[0, 0:1, :]).cpu().numpy()[0]

  @staticmethod
  def calc_similarity(features_image, features_text): 
    return features_image[:,0,:] @ features_text[:,0,:].t()