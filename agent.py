# @Author: Bertan Berker
# @Language: Python
#

# Import relevant functionality
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import openai
from langchain_core.tools import Tool
from langchain.prompts import PromptTemplate

from recipe import get_dish

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create the agent
memory = MemorySaver()
model = ChatOpenAI(model_name="gpt-3.5-turbo")

# Create a prompt template for extracting ingredients
prompt_template = PromptTemplate(
    input_variables=["message"],
    template="Extract only the ingredients from the following text:\n\n{message}\n\nIngredients:"
)


tools = [
    Tool(
        func=get_dish,
        name="Dish_Recommendation",
        description="Gives a dish recommendation based on the given ingredients."
    )
]


agent_executor = create_react_agent(model, tools, checkpointer=memory)

print("Agent created")

user_message = "Hi, my name is Bob and in my fridge I have apples, flour and sugar. I believe life's meaning is 42"

formatted_prompt = prompt_template.format(message=user_message)

ingredient_response = ""
# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content=formatted_prompt)]}, config
):
    print(chunk)
    print("----")
