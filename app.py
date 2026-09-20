from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

from City_Research_agent import run_city_agent

app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()

    if not message:
        return jsonify({"error": "Please enter a question about a city."}), 400

    try:
        return jsonify({"response": run_city_agent(message)})
    except Exception:
        app.logger.exception("City agent request failed")
        return jsonify({"error": "The city assistant could not complete that request."}), 500


if __name__ == "__main__":
    app.run(debug=False, port=5000)
