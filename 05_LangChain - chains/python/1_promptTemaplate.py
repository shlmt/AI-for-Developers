from secret_key import open_api_key

import os

os.environ["OPENAI_API_KEY"] = open_api_key

from langchain_openai import ChatOpenAI

chat = ChatOpenAI(temperature=0.5)

from langchain.prompts import PromptTemplate

code_template = PromptTemplate(
    input_variables=["gole"], template="write a code that {gole}"
)

code_prompt = code_template.format(gole="calculates the average of a list of numbers")

response = chat.invoke(code_prompt)

print(response.content)
