from flask import Flask, jsonify, request
from openai import OpenAI
# from secret_key import secret_key
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openaiClient = OpenAI(api_key=OPENAI_API_KEY)

history = {}


@app.route("/", methods=["POST"])
def integration_gpt():
    body = request.json
    prompt = body["prompt"]
    if not prompt:
        return (
            jsonify({"msg": "Missing prompt"}),
            400,
            {"Content-Type": "application/json"},
        )
    auth = request.headers.get("authorization")
    if not auth or auth.find(" ") == -1:
        return (
            jsonify({"msg": "unauthorized"}),
            401,
            {"Content-Type": "application/json"},
        )
    userId = auth.split(" ")[1]
    if not userId:
        return (
            jsonify({"msg": "unauthorized"}),
            401,
            {"Content-Type": "application/json"},
        )
    messages = history.setdefault(userId, [])
    messages.append({"role": "user", "content": prompt})
    try:
        res = openaiClient.chat.completions.create(
            model="chatgpt-4o-latest",
            messages=[{"role": "system", "content": "give 3 examples for each answer"}]
            + messages,
        )
        answer = res.choices[0].message.content
        messages.append({"role": "assistant", "content": answer})
        return jsonify({"msg": answer}), 200, {"Content-Type": "application/json"}
    except Exception as e:
        print(e)
        return jsonify({"msg": "error"}), 500, {"Content-Type": "application/json"}


app.run(port=8080)
