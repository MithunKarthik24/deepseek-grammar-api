
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Load your OpenRouter API key from environment variable
API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return "✅ DeepSeek Grammar API is running!"

@app.route("/fix", methods=["GET"])
def fix_grammar():
    sentence = request.args.get("text", "")

    if not sentence.strip():
        return jsonify({"error": "No input text provided"}), 400

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-ai/deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that fixes grammar in English sentences."},
            {"role": "user", "content": f"Fix this sentence: {sentence}"}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
        print("DEBUG:", data)  # Logs response for debugging
        output = data["choices"][0]["message"]["content"]
        return jsonify({"output": output.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
