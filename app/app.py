from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from DevOps Compose Demo!"


@app.route("/health")
def health():
    return {
        "status": "healthy",
        "application": "devops-compose-demo"
    }


@app.route("/message")
def message():
    return {
        "message": "Flask application is running successfully!"
    }


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)