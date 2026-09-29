from flask import Flask, jsonify, render_template, request

from chatbot import FAQBot

app = Flask(__name__)
bot = FAQBot("faqs.json")


@app.route("/")
def index():
    samples = [f["question"] for f in bot.faqs[:5]]
    return render_template("index.html", samples=samples)


@app.route("/ask", methods=["POST"])
def ask():
    question = (request.get_json(silent=True) or {}).get("question", "").strip()
    if not question:
        return jsonify({"answer": "Please type a question.", "matched": None, "score": 0}), 400
    return jsonify(bot.ask(question))


if __name__ == "__main__":
    app.run(debug=True)
