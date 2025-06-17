# from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
# from langchain_community.utilities import WikipediaAPIWrapper
# from langchain.tools import Tool
# from datetime import datetime

# def save_to_txt(data: str, filename:str = "research_output.txt"):
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     formatted_text = f"--- Research Ouput ---\nTimestamp: {timestamp}\n\n{data}\n\n"

#     with open(filename, "a", encoding="utf-8") as f:
#         f.write(formatted_text)

#     return f"Data successfully saved to {filename}"  

# save_tool = Tool(
#     name="save_text_to_file",
#     func=save_to_txt,
#     description="Saves structured research data to a test file.",

# )  

# search = DuckDuckGoSearchRun()
# search_tool = Tool(
#     name="search",
#     func=search.run,
#     description="Search the web for information",
# )

# api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
# wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime

# 1. Tool: Save output to a text file
def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f" Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file."
)

# 2. Tool: DuckDuckGo Search
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for relevant information."
)

# 3. Tool: Wikipedia search
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = Tool(
    name="wikipedia",
    func=WikipediaQueryRun(api_wrapper=api_wrapper).run,
    description="Use this to fetch information from Wikipedia articles."
)

from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
import re

def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    return f"Data successfully saved to {filename}"

save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)

# Web Search Tool
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for general information",
)

# Wikipedia Tool
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# Generic Numeric Extraction Tool
def extract_numeric_answer(query: str) -> str:
    result = search.run(query)

    # Extract numbers with surrounding text
    match = re.search(r'(\$?\d[\d,.\s]*\s*(million|billion|trillion|crore|lakh|%|percent)?)', result, re.IGNORECASE)
    if match:
        return f"Answer: {match.group(1)}\n\nSource Text: {result[:300]}..."
    else:
        return f"No exact numeric value found.\n\nSource Text: {result[:300]}..."

numeric_tool = Tool(
    name="numeric_search_tool",
    func=extract_numeric_answer,
    description="Search and extract numeric/statistical information like GDP, population, etc.",
)

