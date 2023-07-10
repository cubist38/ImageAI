import torch
from lavis.models import load_model_and_preprocess

device = torch.device('cuda') if torch.cuda.is_available() else 'cpu'

class ImageNTextEncoder():
  def __init__(self, model_name='blip2_t5', model_type='pretrain_flant5xxl') -> None:
    self.model, self.vis_processors, self.txt_processors = load_model_and_preprocess(name=model_name, model_type=model_type, is_eval=True, device=device)

  def encode_text(self, text): 
    text_input = self.txt_processors['eval'](text)
    sample = {'text_input': [text_input]}
    features_text = self.model.extract_features(sample, mode='text')
    return features_text.text_embeds_proj[0, 0:1, :]
  
  def encode_image(self, image): 
    image = self.vis_processors['eval'](image).unsqueeze(0).to(device)
    sample = {'image': image}
    features_image = self.model.extract_features(sample, mode='image')
    return features_image.image_embeds_proj[0, 0:1, :]

  @staticmethod
  def calc_similarity(features_image, features_text): 
    return features_image[:,0,:] @ features_text[:,0,:].t()