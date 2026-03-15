import sys
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from config import Config

@tool
def get_weather(location: str) -> str:
    """Get weather"""
    return f"Weather in {location} is sunny."

llm = ChatOpenAI(model=Config.MODEL, api_key=Config.API_KEY, base_url=Config.BASE_URL)
agent = create_react_agent(llm, tools=[get_weather], prompt="You are an assistant.")

result = agent.invoke({"messages": [("user", "What is the weather in NYC?")]})
msgs = result["messages"]

steps = []
for msg in msgs:
    if msg.type == "ai" and hasattr(msg, "tool_calls"):
        for tc in msg.tool_calls:
            # find the corresponding tool message
            tool_msg = next((m for m in msgs if m.type == "tool" and m.tool_call_id == tc["id"]), None)
            if tool_msg:
                steps.append({"tool": tc["name"], "input": tc["args"], "output": tool_msg.content})
print("FINAL:", result["messages"][-1].content)
print("STEPS:", steps)
