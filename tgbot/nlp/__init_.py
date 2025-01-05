from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """
You are an AI assistant that helps to organize URLs for a Notion database. Given a URL and its title, you need to determine two parameters:
1. Category: The category in which this URL belongs (e.g., News, Research, Tutorial, Blog, etc.)
2. Priority: The priority of this URL (e.g., High, Medium, Low) based on the title and context.

Please analyze the following:
- Title: {title} (might be empty)
- URL: {url}

Always provide the category and priority in the format (and nothing else):
[Category]
[Priority]
"""

model = OllamaLLM(model="llama3.2:1b")


async def categorize_and_prioritize(title, url):
    try:
        prompt = ChatPromptTemplate.from_template(template.format(title=title, url=url))

        chain = prompt | model

        return await chain.ainvoke({})
    except Exception as e:
        raise Exception(f"Something's wrong with categorize_and_prioritize(): {e}")
