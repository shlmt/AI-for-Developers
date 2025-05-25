from langchain.chat_models import init_chat_model
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_core.prompts import PromptTemplate

from current_weather_tool import get_current_weather
from langchain_community.utilities import WikipediaAPIWrapper

wikipedia = WikipediaAPIWrapper()

import os
from secret_keys import groq_key

if not os.environ.get("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = groq_key

llm = init_chat_model("llama3-8b-8192", model_provider="groq")

tools = [
    Tool(
        name="Wikipedia",
        func=wikipedia.run,
        description="useful for getting information about a place from Wikipedia",
    ),
    Tool(
        name="CurrentWeather",
        func=get_current_weather.run,
        description="Use this tool to get the current weather of a location. The input must be in the format 'City,CountryCode', e.g., 'Jerusalem,IL'.",
    ),
]

agent = initialize_agent(
    tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True,
)
prompt = PromptTemplate(
    input_variables=["country"],
    template="give me the current weather in the capital city of {country}. Also provide a short interesting fact about the city. when you have an answer return it."
)

res = agent.invoke(prompt.format(country="India"))
print(res["output"])
