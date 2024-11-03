# @Author: Bertan Berker
# @Language: Python
# This is the code for the finance agent that uses OpenAI's GPT-3.5-turbo model to provide financial advice to users

# Import relevant functionality
from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import make_a_dish

app = Flask(__name__)
CORS(app)


@app.route('/get_response', methods=['POST'])
def get_response():
    user_ingredients = request.json.get('question', '')
    
    # Get the response from the agent
    recommendation = make_a_dish(user_ingredients)
    
    # Process the output
    result = "1- " + recommendation['dish1'] + " with " + recommendation['drink1'] + "\n" + \
    "2- " + recommendation['dish2'] + " with " + recommendation['drink2']+ "\n" + "3- " + \
    recommendation['dish3'] + " with " + recommendation['drink3']+ "\n"

    # Return the response
    return jsonify({"answer": result})


if __name__ == '__main__':
    app.run(debug=True)