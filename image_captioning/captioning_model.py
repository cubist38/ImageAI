from clip_interrogator import Config, Interrogator
import streamlit as st
import json

@st.cache_resource()
def load_clip_interrogator(config_p, device: str):
    with open(config_p, "r") as f:
        model_config = json.load(f)
    config = Config(**model_config)
    config.device = device
    model = Interrogator(config)
    return model