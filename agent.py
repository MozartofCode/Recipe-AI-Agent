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

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
serper_api_key = os.getenv('SERPER_API_KEY')
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'


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
        tools =[scrape_tool, search_tool]
    )

    #TODO add the agent that will find the matching drink for the dish

    # TASKS
    dish = Task(
        description=(
            "The task is to find the top 3 dishes that can be made with the given ingredients",
            " {ingredients}"
        ),
        expected_output=(
            "The top 3 dishes that can be made with the given ingredients are:"
            "1- Dish1"
            "2- Dish2"
            "3- Dish3",
        ),
        agent=dish
    )

    # Define the crew with agents and tasks
    poker_crew = Crew(
        agents=[find_dish],
        tasks=[dish],
        manager_llm=ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7),
        process=Process.sequential,
        verbose=True
    )


    result = poker_crew.kickoff(inputs=ingredients)
    return result