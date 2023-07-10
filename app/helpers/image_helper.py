from PIL import Image

def resize_image(image_path, max_width = 400, max_height = 400):
    image = Image.open(image_path)

    width, height = image.size

    aspect_ratio = width / height
    new_width = min(width, max_width)
    new_height = int(new_width / aspect_ratio)

    if new_height > max_height:
        new_height = min(height, max_height)
        new_width = int(new_height * aspect_ratio)

    resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)

    resized_image.save(image_path)