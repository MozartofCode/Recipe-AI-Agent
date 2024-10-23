
# Spoonacular API Key
from dotenv import load_dotenv
import os
import requests
import openai

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
spoonacular_api_key = os.getenv('SPOONACULAR_API_KEY')


# Function (Tool) for getting a recipe based on an ingredient
def get_dish(ingredients):

    # Format of the ingredients = apple, sugar, flour etc
    
    url = f"https://api.spoonacular.com/recipes/findByIngredients?apiKey={spoonacular_api_key}&ingredients={ingredients}&number=2"

    # Make the GET request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Print the retrieved recipes
        for i, recipe in enumerate(response.json(), start=1):
            return (f"Recipe {i}: {recipe['title']}")    
    else:
        print(f"Error: {response.status_code}")
        return None


# Tool for extracting ingredients from a text
def extract_ingredients(text):
    # Define the prompt for ingredient extraction
    prompt = f"Extract the ingredients from the following text:\n{text}\nIngredients:"
   
      # Make the request to OpenAI's GPT-3.5 API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Using GPT-3.5-turbo
        messages=[
            {"role": "system", "content": "You are an assistant that extracts ingredients from text."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the response and return the ingredients
    return response["choices"][0]["message"]["content"]
