from typing import List
import numpy as np
import streamlit as st
from segment_anything import SamPredictor, sam_model_registry

@st.cache_resource()
def load_sam_model(sam_model_type, sam_model_path, device):
    sam = sam_model_registry[sam_model_type](checkpoint=sam_model_path)
    sam.to(device=device)
    predictor = SamPredictor(sam)
    return predictor

def build_sam_model(model_type: str, ckpt_p: str, device="cuda"):
    sam = sam_model_registry[model_type](checkpoint=ckpt_p)
    sam.to(device=device)
    predictor = SamPredictor(sam)
    return predictor

def predict_masks_with_sam(
        img: np.ndarray,
        point_coords: List[List[float]],
        point_labels: List[int],
        predictor: SamPredictor):
    point_coords = np.array(point_coords)
    point_labels = np.array(point_labels)
    predictor.set_image(img)
    masks, scores, logits = predictor.predict(
        point_coords=point_coords,
        point_labels=point_labels,
        multimask_output=True,
    )
    return masks, scores, logits