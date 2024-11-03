# @Author: Bertan Berker
# @Language: Python
# This is an multi-agent system that creates a recipe and finds a 
# matching drink for the food as well as the history of the food


from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from crewai import Agent, Task, Crew, Process
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
import warnings
warnings.filterwarnings('ignore')
import os
from pydantic import BaseModel

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# Defining the output model for having a structured output from the agents
class DishPair(BaseModel):
    dish1: str
    dish2: str
    dish3: str
    drink1: str
    drink2: str
    drink3: str


# Function to create a dish with the given ingredients
# :param ingredients: list of ingredients
# :return: the top 3 dishes that can be made with the given ingredients and the drinks that can be paired with them
def make_a_dish(ingredients):

    search_tool = SerperDevTool()
    scrape_tool = ScrapeWebsiteTool()

    # AGENTS
    find_dish = Agent(
        role="Dish Maker Agent",
        goal="Finds the top 3 dishes based on the ingredients that are present in the fridge",
        backstory="Specializing in making creative and amazing dishes and incredibly knowledgable"
                  " about the ingredients and the dishes that can be made with them. Given the ingredients: {ingredients}"
                  " the agent will find the top 3 dishes that can be made with them",
        verbose=True,
        allow_delegation=False,
        tools=[scrape_tool, search_tool]
    )

    find_drink = Agent(
        role="Food Pairing Agent",
        goal="Finds the right drinks for the food",
        backstory="Specializing in making creative and amazing drink pairing with given dishes. These drink could be like"
                  " specific types of wine, beer etc or it could just be cola, sprite, ice tea as well.",
        verbose=True,
        allow_delegation=False,
        tools=[scrape_tool, search_tool]
    )

    # TASKS
    dish = Task(
        description=
            "The task is to find the top 3 dishes that can be made with the given ingredients"
            " {ingredients}",
        expected_output=
            "The top 3 dishes that can be made with the given ingredients are:"
            "1- Dish1"
            "2- Dish2"
            "3- Dish3",
        agent=find_dish
    )

    drink = Task(
        description=
            "The task is to find the right drinks for the given dish",
        expected_output=
            "The right drinks for the given dish are:"
            "1- Drink1"
            "2- Drink2"
            "3- Drink3",
        output_json=DishPair,
        agent=find_drink
    )

    
    # Define the crew with agents and tasks
    meal_crew = Crew(
        agents=[find_dish, find_dish],
        tasks=[dish, drink],
        manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
        process=Process.sequential,
        verbose=True
    )
    inputs = {'ingredients': ingredients}
    result = meal_crew.kickoff(inputs=inputs)
    return result