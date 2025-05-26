from secret_key import open_api_key

import os

os.environ["OPENAI_API_KEY"] = open_api_key

from langchain_openai import ChatOpenAI

chat = ChatOpenAI(temperature=0.5)

from langchain.prompts import ChatPromptTemplate

code_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert {lang} developer who writes exceptionally clean and smart code, using the specific and characteristic capabilities of the language. Give me only the code. don't include comments or explanations.",
        ),
        ("human", "Write me a code please."),
        ("ai", "With pleasure! Tell me what code you need. What should it do?"),
        ("human", "{input}"),
    ]
)

code_prompt = code_template.format(
    lang="js", input="find a fibonacci number for a given position"
)

response = chat.invoke(code_prompt)

print(response.content)
