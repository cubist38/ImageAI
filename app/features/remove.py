from app.features.config import get_settings
from app.helpers.load_lama import load_lama_model, inpaint_img_with_built_lama

config = get_settings()

def remove_selected_object_on_image(image, mask):
    lama_model = load_lama_model(
                    config_p = config.lama_model_config_p, 
                    ckpt_p = config.lama_model_ckpt_p, 
                    device = config.device
                )
    img_inpainted = inpaint_img_with_built_lama(lama_model, 
                                                image, 
                                                mask,
                                            )      
    return img_inpainted