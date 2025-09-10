from flask import Flask
import requests
import socket
import os

BACKEND_HOST = os.environ.get("BACKEND_HOST", "backend:5000")
MESSAGE = os.environ.get("MESSAGE", "Olá do frontend!")

app = Flask(__name__)

@app.route("/")
def index():
    try:
        backend_response = requests.get(f"http://{BACKEND_HOST}").json()
    except Exception as e:
        backend_response = {"error": str(e)}
    return {
        "frontend_host": socket.gethostname(),
        "mensagem": MESSAGE,
        "backend_response": backend_response
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)