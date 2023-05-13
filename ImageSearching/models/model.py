import clip
from models.base_model import ImageTextEncoder
import torch

class CLIPModel(ImageTextEncoder):
    def __init__(self, model_name = 'ViT-L/14@336px', device: str = None) -> None:
        super().__init__(device)
        self.model, self.preprocess = clip.load(model_name, device = self.device)
        print('CLIP loaded model', model_name, 'successfully')

    def encode_image(self, images):
        if isinstance(images, list):
            images = torch.stack([
                self.preprocess(image) for image in images
            ]).to(self.device)
        
        with torch.no_grad():
            image_features = self.model.encode_image(images)
            image_features /= image_features.norm(dim = -1, keepdim = True)
        return image_features.detach().cpu()
    
    def encode_text(self, text):
        tokenized_text = clip.tokenize(text).to(self.device)
        with torch.no_grad():
            text_feature = self.model.encode_text(tokenized_text)
            text_feature /= text_feature.norm(dim = -1, keepdim = True)
        return text_feature.detach().cpu()
    
    def get_image_preprocess(self):
        return self.preprocess