from lama_inpaint import build_lama_model
import streamlit as st

@st.cache_resource()
def load_lama_model(
        config_p: str, 
        ckpt_p: str,
        device = "cuda"):
    return build_lama_model(config_p, ckpt_p, device)