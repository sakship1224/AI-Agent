from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor
from tools import search_tool, wiki_tool, save_tool,numeric_tool

import json
import re
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing API key. Check your .env file.")

# Configure API
genai.configure(api_key=api_key)

# Use Gemini 1.5 Flash
model = ChatGoogleGenerativeAI(model="models/gemini-1.5-flash-latest")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Define prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that answers user queries with summarized and structured data.\n
            Use tools to look up **numeric, factual, or structured information** such as population, percentages, GDP, statistics, etc.\n
            Always return in the following format:\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Define tools correctly
tools = [search_tool, wiki_tool, save_tool,numeric_tool]

# Bind tools properly
bound_model = model.bind_tools(tools=tools)

# Create agent

agent = create_tool_calling_agent(
    llm=bound_model,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# Create executor
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# Accept user query
query = input("What can I help you research? ")
raw_response = agent_executor.invoke({"query": query})

# Parse and clean JSON output
import ast

try:
    response_text = raw_response.get("output")
    
    # If output is wrapped in triple backticks or has malformed JSON
    cleaned = re.sub(r"```json|```", "", response_text).strip()
    structured_response = parser.parse(cleaned)

    print(" Parsed Response:")
    print(structured_response)

    # Save to file
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(structured_response.model_dump(), f, indent=4)
    print(" Saved to output.json")

except Exception as e:
    print(" Error parsing response:", e)
    print(" Raw output:", raw_response)