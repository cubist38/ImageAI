from flask import Flask
from pyngrok import ngrok
import json

with open('/content/drive/MyDrive/config.json', 'r') as f:
    config = json.load(f)
ngrok.set_auth_token(config['ngrok_token'])

if __name__ == '__main__':
    # Start ngrok and create a tunnel for the Flask app
    public_url = ngrok.connect(5002).public_url
    print(public_url)