from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
from crewai_tools import FileReadTool
from langchain_experimental.utilities import PythonREPL

import os
from secret_key import open_ai_key

os.environ["OPENAI_API_KEY"] = open_ai_key


# tools
@tool("repl")
def repl(code: str) -> str:
    """Useful for executing Python code"""
    return PythonREPL().run(command=code)


@tool("files_in_directory")
def get_files_in_direftory() -> str:
    """Returns the tree of files in the current directory"""
    return "\n".join(os.listdir("."))


file_read_tool = FileReadTool()

# agents

analistAgent = Agent(
    role="You are a data-analisist & python programmer.",
    goal="Write Python code that solves data analysis problems based on data from a relevant CSV file.",
    backstory="""You are a data-analyst & python programmer.""",
    tools=[get_files_in_direftory, file_read_tool],
)

runCodeAgent = Agent(
    role="Python code executor.",
    goal="Execute the Python code and explain its output clearly.",
    backstory="""
            You are a Python execution engine.
            You will be given a code to run and return the output with nice explain.
            """,
    tools=[repl],
)

# task
codeTask = Task(
    description="Write code for . {problem}",
    expected_output="python code with explanation",
    agent=analistAgent,
)

responseTask = Task(
    description="Run the code and return the output with nice explain.",
    expected_output="the code & its output with nice explain as markdown",
    output_file="res.md",
    agent=runCodeAgent,
)

# crew & run
crew = Crew(
    agents=[analistAgent, runCodeAgent],
    tasks=[codeTask, responseTask],
    verbose=True,
)

question = input("what you want?")

result = crew.kickoff(inputs={"problem": question})
print(result)
