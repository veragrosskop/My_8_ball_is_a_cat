from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os
from cat import Cat

# INITIALIZE APP
# ------------------
load_dotenv()  # loads .env into environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("No API key found. Set OPENAI_API_KEY in .env")

client = OpenAI(api_key=OPENAI_API_KEY)

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
    response = client.responses.create(
        model="gpt-5.4",
        instructions=f"Talk like a cat. {mood_prompt}",
        input=question
    )
    return response.output_text


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