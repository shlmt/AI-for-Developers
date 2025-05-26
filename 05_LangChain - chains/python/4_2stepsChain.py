import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableMap
from secret_key import open_api_key

os.environ["OPENAI_API_KEY"] = open_api_key

llm = ChatOpenAI(temperature=0.6)


def generate_code_and_tests(lang, gole):
    code_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert {lang} developer who writes exceptionally clean and smart code, using the specific and characteristic capabilities of the language."
                "Give me only the code. don't include comments or explanations.",
            ),
            ("human", "Write me a code please."),
            ("ai", "With pleasure! Tell me what code you need. What should it do?"),
            ("human", "{input}"),
        ]
    )

    test_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "Write unit test for the following code. Give me only the test code, don't include comments or explanations.",
            ),
            ("human", "{input}"),
        ]
    )

    code_chain = code_template | llm | StrOutputParser()

    test_chain = test_template | llm | StrOutputParser()

    full_chain = RunnableMap({"code": code_chain, "test": test_chain})

    response = full_chain.invoke({"lang": lang, "input": gole})

    return response


response = generate_code_and_tests(lang="python", gole="find a fibonacci number for a given position")
print(response["code"])
print(response["test"])
