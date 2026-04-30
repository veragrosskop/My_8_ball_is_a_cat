from flask import Flask, render_template, request, jsonify
from cat import Cat
from client import GenAIClient
import threading
import time
import os

# INITIALIZE APP
# ------------------
CLIENT = GenAIClient() #defaults to standard Gemini for development see client.py
app = Flask(__name__)
CAT = Cat()

# Helper Functions
#-------------------
def ask_oracle(question) -> str:
    """
    Passes a question to openai.com and returns the answer as if it is a cat.

    :param question: The question to ask
    :return: The answer as a string as answered by a cat.
    """

    instructions = CAT.get_mood_instructions()
    print(instructions)
    try:
        response = CLIENT.get_response(question, instructions)
    except Exception as e:

        error_msg = f"{e}"

        if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
            response = "⚠️ You've reached your oracle question limit. Try again later."

        else:
            response =  "⚠️ The oracle is confused... something went wrong."
    print(response)
    return response

# Routes
# ------------------
@app.route("/", methods=['GET'])
def oracle_homepage():
    return render_template('index.html', state=CAT.get_dict_state(), message="Ask me anything...")

@app.route("/", methods=['POST'])
def oracle_action():
    answer = ""
    action = request.form.get("action")

    if action == "ask":
        question = request.form.get("question")
        CAT.handle_ask()
        print(question)
        answer = ask_oracle(question)
        print(CAT.get_dict_state())
        return jsonify({"message": answer, "state": CAT.get_dict_state()})
    elif action == "feed":
        CAT.handle_feed()
        answer = "🐟 The cat has been fed!"
        print(CAT.get_dict_state())
        return jsonify({"message": answer, "state": CAT.get_dict_state()})
    elif action == "nap":
        CAT.handle_nap()
        answer = "ZZZZZzzzzz..."
        print(CAT.get_dict_state())
        return jsonify({"message": answer, "state": CAT.get_dict_state()})
    elif action == "pet":
        CAT.handle_pet()
        answer = "😸 Purr... the cat is happy!"
        print(CAT.get_dict_state())
        return jsonify({"message": answer, "state": CAT.get_dict_state()})

    return jsonify({"message": answer, "state": CAT.get_dict_state()})

@app.route("/status")
def status():
    return jsonify(CAT.get_dict_state())

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=False)