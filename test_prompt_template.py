import sys
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import Config

@tool
def get_weather(location: str) -> str:
    """Get weather"""
    return f"Weather in {location} is sunny."

llm = ChatOpenAI(model=Config.MODEL, api_key=Config.API_KEY, base_url=Config.BASE_URL)

history_str = "User likes NYC."
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant. (STATIC PROMPT)"),
    ("system", f"History: {history_str}"),
    MessagesPlaceholder(variable_name="messages")
])

agent = create_react_agent(llm, tools=[get_weather], prompt=prompt_template)

result = agent.invoke({"messages": [("user", "What is the weather like? Where do I like?")]})
msgs = result["messages"]

print("FINAL:", result["messages"][-1].content)
