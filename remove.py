from lama_model import load_lama_model, inpaint_img_with_builded_lama
from sam_model import load_sam_model, predict_masks_with_sam
from engine import dilate_mask
from remove_anything_video import load_remove_anything_video
import numpy as np
import torch
import imageio as iio

def remove_selected_object_on_image(image, coords):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")    
    if image.mode == "RGBA":
        image = image.convert("RGB")
    image =  np.array(image)
    predictor = load_sam_model("vit_h", 
                                "/content/drive/MyDrive/InpaintAnything/Weights/sam_vit_h_4b8939.pth", 
                                device)
    masks, scores, logits = predict_masks_with_sam(image,
        [[int(coords["x"]), int(coords["y"])]],
        [1],
        predictor)
    masks = masks.astype(np.uint8) * 255
    mask = masks[np.argmax(scores)]
    mask = dilate_mask(mask, 15)
    lama_model = load_lama_model(
                    config_p = "lama/configs/prediction/default.yaml", 
                    ckpt_p = "/content/drive/MyDrive/InpaintAnything/Weights/big-lama", 
                    device = device
                )
    img_inpainted = inpaint_img_with_builded_lama(lama_model, image, mask, config_p = "lama/configs/prediction/default.yaml")
    return img_inpainted

def remove_selected_object_on_video(frames_p, coords, fps = 30):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  
    model = load_remove_anything_video()
    model.to(device)
    with torch.no_grad():
        all_frame_rm_w_mask, all_mask, all_box = model(
            frames_p, 0, np.array([[int(coords["x"]), int(coords["y"])]]), np.array([1]), 2,
            15
        )
    output_file = 'output.mp4'
    iio.mimwrite(output_file, all_frame_rm_w_mask, fps=fps)
    return output_file