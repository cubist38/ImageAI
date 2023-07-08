from app.features.segment import segment_selected_object_on_image
import cv2

def blur_image(img, x, y, sigma = (3, 3)): 
    img, mask = segment_selected_object_on_image(img, x, y)
    binary_mask = mask == 0
    blurred_img = cv2.GaussianBlur(img, (0, 0), sigmaX=sigma[0], sigmaY=sigma[1], borderType=cv2.BORDER_DEFAULT)
    blurred_img[binary_mask] = img[binary_mask]

    return blurred_img
    

