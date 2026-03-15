import sys
import queue
import threading
from langchain_openai import ChatOpenAI
from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from config import Config

@tool
def dummy_tool(query: str) -> str:
    """A dummy tool"""
    return "Dummy result for " + query

class CB(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs):
        print("TOKEN:", token)
    def on_tool_start(self, serialized, input_str, **kwargs):
        print("TOOL START:", input_str)

llm = ChatOpenAI(model=Config.MODEL, api_key=Config.API_KEY, base_url=Config.BASE_URL, streaming=True)
agent = create_react_agent(llm, tools=[dummy_tool], prompt="You are a helpful assistant. Use dummy tool to answer.")

cb = CB()
result = agent.invoke({"messages": [("user", "Hello! Then use dummy tool to search for AI")]}, config={"callbacks": [cb]})
print("FINAL MSG:", result["messages"][-1].content)
