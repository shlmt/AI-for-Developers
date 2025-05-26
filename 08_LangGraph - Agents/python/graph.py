from secret_keys import OPEN_API_KEY, SERPAPI_KEY
import os, requests
from langchain_core.messages import HumanMessage, AnyMessage
from langgraph.graph import StateGraph, START, END, add_messages
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
from langchain.agents import tool, Tool
from langchain_community.utilities import SerpAPIWrapper
from langgraph.prebuilt import ToolNode, tools_condition

os.environ["OPENAI_API_KEY"] = OPEN_API_KEY
os.environ["SERPAPI_API_KEY"] = SERPAPI_KEY


# tools
@tool()
def fetch_from_api(url: str):
    """
    get data from specific api
    """
    print("fetch", url)
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.text
    except:
        print("error:", res)
        return "Error in fetch"


@tool
def duckduckgo_search(query):
    """Search using DuckDuckGo."""
    print("duckducl search", query)
    url = "https://api.duckduckgo.com/" + query
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print("Error during fetch:", e)
        return "Error in fetch"


search = SerpAPIWrapper()

tools = [
    fetch_from_api,
    duckduckgo_search,
    # Tool(
    #     name="GoogleSearch",
    #     description="use for simple search in Google",
    #     func=search.run,
    # ), # its not work with netfree
]

# llm
llm = ChatOpenAI(model="gpt-3.5-turbo").bind_tools(tools)


# the state
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# the nodes
def run_llm(state: State):
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": response}


def format_response(state: State):
    last_message = state["messages"][-1]
    return {
        "messages": [HumanMessage(content=f"Agent response: {last_message.content}")]
    }


tool_node = ToolNode(tools)

# the graph
graph_builder = StateGraph(State)

graph_builder.add_node("llm", run_llm)
graph_builder.add_node("tools", tool_node)
graph_builder.add_node("llm explain", run_llm)
graph_builder.add_node("format", format_response)

graph_builder.add_edge(START, "llm")
graph_builder.add_conditional_edges("llm", tools_condition)
graph_builder.add_edge("tools", "llm explain")
graph_builder.add_edge("llm explain", "format")
graph_builder.add_edge("format", END)


graph = graph_builder.compile()

while True:
    question = input("Query: ")
    result = graph.invoke({"messages": [HumanMessage(content=question)]})
    print(result["messages"][-1].content)
