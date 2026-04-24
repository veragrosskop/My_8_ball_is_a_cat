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
        response = f"{e}"
    print(response)
    return response

#
# def background_loop(flask_app):
#     with flask_app.app_context():
#         while True:
#             CAT.update()  # your global pet
#             time.sleep(5)
#
# def start_background_thread(flask_app):
#     thread = threading.Thread(target=background_loop, args=(flask_app,), daemon=True)
#     thread.start()

# Routes
# ------------------
@app.route("/", methods=['GET'])
def oracle_homepage():
    return render_template('index.html', message="Ask me anything...")

@app.route("/", methods=['POST'])
def oracle_action():
    answer = ""
    action = request.form.get("action")
    print("Form data:", request.form)  # what does this show?
    #TODO! fix stats view
    if action == "ask":
        question = request.form.get("question")
        print(question)
        answer = ask_oracle(question)
        return jsonify({"message": answer, "state": CAT.get_dict_state()})
    elif action == "feed":
        CAT.handle_feed()
        answer = "🐟 The cat has been fed!"
        return jsonify({"message": answer, "state": CAT.get_dict_state()})
    elif action == "pet":
        CAT.handle_pet()
        answer = "😸 Purr... the cat is happy!"
        return jsonify({"message": answer, "state": CAT.get_dict_state()})

    return jsonify({"message": answer, "state": CAT.get_dict_state()})

@app.route("/status")
def status():
    return jsonify(CAT.get_dict_state())

if __name__ == '__main__':
    # if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    #     start_background_thread(app)

    app.run(host="0.0.0.0", port=5002, debug=False)