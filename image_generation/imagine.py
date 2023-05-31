import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "image_generation"))
from model import load_imagine_model

def text_to_image(prompt, device="cuda"):
    model = load_imagine_model("image_generation/config.json", device)
    image = model(prompt).images[0]
    return image