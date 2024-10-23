# Spoonacular API Key
from dotenv import load_dotenv
import os
import requests

load_dotenv()
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