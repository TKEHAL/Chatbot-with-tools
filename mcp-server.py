from pathlib import Path

from mcp.server.fastmcp import FastMCP
from langchain_tavily import TavilySearch
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name(".env"), override=True)
mcp = FastMCP(name="mcp-server", host=("0.0.0.0"), port = 24000)

@mcp.tool()
def get_employee_infos(name: str):
    """
    Get infos about the given employee
    """
    return{
        "name": name,
        "salary":23000,
        "seniority": 12
    }

@mcp.tool()
def web_search(query: str):
   """
   Search the live web for current or recent information using Tavily.
   Use this tool whenever the user asks to search, look up, find, or verify
   information from the internet.
   """
   web_search_client = TavilySearch()
   results = web_search_client.invoke({
        "query":query
    }) 
   return results

if __name__=="__main__":
    mcp.run(transport="streamable-http")
