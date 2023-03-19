from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify
import base64
from src.retriever import *
from src.models.ViT import *


server = Flask(__name__)
VECTOR_DIM = 512
IMG_DIR = './Server/image'
encoder = VIT()
retriever = Retriever(IMG_DIR, VECTOR_DIM)
retriever.add_images_embedding(encoder)


def retrieve_image(text, top): 
    # TODO: retrieve image from text to list of image url 
    text_feature = encoder.encode_text(text).cpu().numpy()
    top_k_images = retriever.search_queries(text_feature.astype(np.float32), top)

    return top_k_images

if __name__ == '__main__':
    #server.run(host = '0.0.0.0', port=8000)
    print(retrieve_image('Carrot', 5))
