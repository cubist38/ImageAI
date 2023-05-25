import streamlit as st
import torch
from lavis.models import load_model_and_preprocess


class ImageCaptioner():
    def __init__(self, model_name='blip_caption', model_type='base_coco', device = None):
        if not device:
            device = torch.device('cuda') if torch.cuda.is_available() else 'cpu'
        self.device = device
        self.model, self.vis_processors, _ = load_model_and_preprocess(name=model_name, model_type=model_type, is_eval=True, device=device)

    def generate_caption(self, image):
        processed_image = self.vis_processors["eval"](image).unsqueeze(0).to(self.device)
        out = self.model.generate({"image": processed_image})
        return out[0]
    
@st.cache_resource()
def load_image_captioner():
    return ImageCaptioner()