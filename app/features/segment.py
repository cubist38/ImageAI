from app.helpers.load_sam import load_sam_model, predict_masks_with_sam
from app.features.config import get_settings
from app.helpers.engine import dilate_mask
import numpy as np

config = get_settings()

def segment_selected_object_on_image(image, x, y):
    if image.mode == "RGBA":
        image = image.convert("RGB")   
    predictor = load_sam_model(config.sam_model_type, 
                                config.sam_model_ckpt_p,
                                config.device)
    image =  np.array(image)
    masks, scores, logits = predict_masks_with_sam(image,
                                                [[int(x), int(y)]],
                                                [1],
                                                predictor)
    masks = masks.astype(np.uint8) * 255
    mask = masks[np.argmax(scores)]
    mask = dilate_mask(mask, 15)
    return image, mask