from crewai_tools import WebsiteSearchTool
from crewai.tools import BaseTool
from ddgs import DDGS

web_rag_tool = WebsiteSearchTool()

class WebSearchTool(BaseTool):
    name: str= "web_search"
    description: str = "Search the web. Returns titles, URLs and snippets."
