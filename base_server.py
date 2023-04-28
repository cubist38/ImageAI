from flask import Flask
from pyngrok import ngrok
import json

with open('./config.json', 'r') as f:
    config = json.load(f)
ngrok.set_auth_token(config['ngrok_token']'])

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    # Start ngrok and create a tunnel for the Flask app
    public_url = ngrok.connect(5002).public_url
    print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}/\"".format(public_url, 5002))
    app.run(port = 5002)