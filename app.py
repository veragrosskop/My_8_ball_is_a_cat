from flask import Flask, render_template, request
from cat import Cat
from client import GenAIClient

# INITIALIZE APP
# ------------------
CLIENT = GenAIClient()

app = Flask(__name__)

CAT = Cat()

# Helper Functions
#-------------------

def ask_oracle(question, mood_prompt) -> str:
    """
    Passes a question to openai.com and returns the answer as if it is a cat.

    :param question: The question to ask
    :param mood_prompt: The mood prompt for the cat. For example answer as if you're a hungry cat.
    :return: The answer as a string as answered by a cat.
    """

    response = CLIENT.get_response(question, mood_prompt)
    return response


# Routes
# ------------------

@app.route("/", methods=['GET', 'POST'])
def oracle_homepage():
    question = request.form.get("question")
    print(question)
    answer = ask_oracle(question, Cat.mood_prompt())
    return render_template('index.html', answer=answer)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)