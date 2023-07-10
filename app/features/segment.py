from app.helpers.load_sam import load_sam_model, predict_masks_with_sam
from app.features.config import get_settings
from app.helpers.engine import dilate_mask
import numpy as np

config = get_settings()

def segment_selected_object_on_image(image, x, y):
    predictor = load_sam_model(config.sam_model_type, 
                                config.sam_model_ckpt_p,
                                config.device)
    # if image.mode == 'RGBA':
    #     image = image.convert('RGB')
    # image = np.array(image)
    masks, scores, logits = predict_masks_with_sam(image,
                                                [[int(float(x)), int(float(y))]],
                                                [1],
                                                predictor)
    masks = masks.astype(np.uint8) * 255
    mask = masks[np.argmax(scores)]
    mask = dilate_mask(mask, 15)
    image_with_mask = image.copy()
    color = np.array([ 40, 40, 255])
    image_with_mask[mask == 255] = color

    return image, mask, image_with_mask