from PIL import Image
from Base import BaseModel
import clip
import torch


class VIT(BaseModel):
    def __init__(self):
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.model, self.preprocess =  clip.load("ViT-B/32", device=self.device)

        self.model.eval()
        # self.input_resolution = self.model.visual.input_resolution
        # self.context_length = self.model.context_length
        # self.vocab_size = self.model.vocab_size

    def encode_text(self, text):
        text_tokens = clip.tokenize([text]).to(self.device)

        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens).float()

        return text_features

    def encode_image(self, img_path):

        image = self.preprocess(Image.open(img_path)).unsqueeze(0).to(self.device)

        image_features = None
        with torch.no_grad():
            image_features = self.model.encode_image(image)
        return image_features

model = VIT()
encoded_text = model.encode_text('There are some tomatoes')
print(encoded_text.shape)