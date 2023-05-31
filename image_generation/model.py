from diffusers import StableDiffusionPipeline
import torch
import json
import streamlit as st

@st.cache_resource()
def load_imagine_model(config_p, device: str):
    with open(config_p, "r") as f:
        model_config = json.load(f)
    model_name = model_config["model_name"]
    pipe = StableDiffusionPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
    pipe = pipe.to(device)
    return pipe