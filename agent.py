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

from recipe import get_dish

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Create the agent
memory = MemorySaver()
model = ChatOpenAI(model_name="gpt-3.5-turbo")

tools = [
    Tool(
        func=get_dish,
        name="Dish_Recommendation",
        description="Gives a dish recommendation based on the given prompt."
    )
]


agent_executor = create_react_agent(model, tools, checkpointer=memory)

print("Agent created")

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config
):
    print(chunk)
    print("----")

for chunk in agent_executor.stream(
    {"messages": [HumanMessage(content="What should I eat?")]}, config
):
    print(chunk)
    print("----")