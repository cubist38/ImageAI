import faiss
import json
import numpy as np
import os
from tqdm.notebook import trange, tqdm
import pandas as pd
import glob


def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

class Retriever:
    def __init__(self, img_dir: str, vector_dim: int = 512):
        self.img_dir = img_dir
        self.img_index = {}
        # faiss
        self.index = faiss.IndexFlatIP(vector_dim)


    def add_images_embedding(self, encoder):

        # device = "cuda:0" if torch.cuda.is_available() else "cpu"
        # model, preprocess = clip.load("ViT-B/16", device=device)

        imgs_path = glob.glob(os.path.join(self.img_dir, '*.jpg'))

        for idx, img_path in enumerate(imgs_path):

            # image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
            # with torch.no_grad():
            #     image_features = model.encode_image(image)
            
            image_features = encoder.encode_image(img_path)
            feat_arr = image_features.cpu().detach().numpy()
            feat_arr = normalize(feat_arr)
            feat_arr = feat_arr.astype(np.float32)
            faiss.normalize_L2(feat_arr)
            self.index.add(feat_arr)
            self.img_index[str(idx)] = img_path

    def index_to_path(self, idx):
        return self.img_index[str(idx)]
        

    def search_queries(self, X, top_k: int):
        # convert to numpy array
        faiss.normalize_L2(X)
        distances, indices = self.index.search(X.astype(np.float32), top_k)

        ls = []

        for idx in indices[0]:
            
            ls.append(self.img_index[str(idx)])

        return ls
