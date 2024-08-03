import requests
import PyPDF2
import os
import xml.etree.ElementTree as ET
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage


# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Initialize the ChatAnthropic model
anthropic_api_key = os.environ['ANTHROPIC_API_KEY']
llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", api_key=anthropic_api_key)

# Define the tools we are using
@tool
def search_arxiv(query: str, max_results: int = 3) -> str:
    """
    Searches arXiv for papers based on the given query.
    Returns a list of paper titles and their arXiv IDs.
    """
    base_url = "http://export.arxiv.org/api/query?"
    search_query = query.replace(' ', '+')
    url = f"{base_url}search_query=all:{search_query}&start=0&max_results={max_results}"
    
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error: Unable to fetch results. Status code: {response.status_code}"
    
    root = ET.fromstring(response.content)
    
    results = []
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
        title = entry.find('{http://www.w3.org/2005/Atom}title').text.strip()
        arxiv_id = entry.find('{http://www.w3.org/2005/Atom}id').text.split('/')[-1]
        summary = entry.find('{http://www.w3.org/2005/Atom}summary').text.strip()
        results.append(f"Title: {title}\nArXiv ID: {arxiv_id}\nSummary: {summary}\n")
    
    return "\n".join(results) if results else "No results found."


@tool
def download_and_extract_text(arxiv_id: str) -> str:
    """
    Downloads the PDF for a given arXiv ID and extracts its text content.
    """
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to download PDF. Status code: {response.status_code}"
    
    with open("temp.pdf", 'wb') as f:
        f.write(response.content)
    
    text = ""
    with open("temp.pdf", 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    os.remove("temp.pdf")  # Clean up the temporary file
    
    return text[:1000000]  # Limit to first 1,000,000 characters to avoid potential token limits


######################################################################################################

# Bind the tools to the LLM
tools = [search_arxiv, download_and_extract_text]
llm_with_tools = llm.bind_tools(tools)

# Initial query
query = "Interesting new ideas in improving reasoning for llms."
messages = [HumanMessage(content=f"Search arXiv for 3 papers related to: {query}")]

# Prompt the LLM to search arXiv
search_response = llm_with_tools.invoke(messages)
print(search_response.content)
print(search_response.tool_calls)
messages.append(search_response)

# Execute the tool call to actually perform the search
search_results = None
for tool_call in search_response.tool_calls:
    if tool_call["name"].lower() == "search_arxiv":
        search_results_tool_msg = search_arxiv.invoke(tool_call)
        break

if search_results_tool_msg is None:
    raise ValueError("The LLM did not call the search_arxiv tool as expected.")

print(search_results_tool_msg.content)
# Add the search results to the messages
messages.append(search_results_tool_msg)



# Ask LLM to choose the most relevant paper
messages.append(HumanMessage(content="Based on these results, which paper seems most relevant and interesting? Please use the download_and_extract_text tool to indicate your choice by providing the arXiv ID."))
paper_choice = llm_with_tools.invoke(messages)
print(paper_choice)
# print(paper_choice.tool_calls)
messages.append(paper_choice)

# Extract chosen arXiv ID from the tool call and invoke the download_and_extract_text tool
pdf_text_response = None
for tool_call in paper_choice.tool_calls:
    if tool_call['name'].lower() == 'download_and_extract_text':
        pdf_text_response = download_and_extract_text.invoke(tool_call)
        break

if pdf_text_response is None:
    raise ValueError("The LLM did not make a valid paper choice using the tool.")

# add it to the messages
messages.append(pdf_text_response)
print(pdf_text_response.content[:1000])


# Ask LLM to summarize the paper and create a Twitter thread
messages.append(HumanMessage(content="Based on the extracted text, please provide a summary of the paper and create a Twitter thread (5-7 tweets) highlighting its key points and significance."))
final_response = llm_with_tools.invoke(messages)
print(final_response.content)