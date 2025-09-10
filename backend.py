from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def index():
    return {
        "backend_host": socket.gethostname()  # Container ID/hostname
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)