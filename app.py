from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY", "sk-or-your-api-key-here")  # Replace with your key or set env var

@app.route("/fix", methods=["POST"])
def fix_grammar():
    sentence = request.get_json().get("text", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": f"Correct this sentence: {sentence}"}]
    }

    r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

    try:
        output = r.json()["choices"][0]["message"]["content"]
        return jsonify({"output": output.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
