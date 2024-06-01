from colorama import Fore, Back
from crewai_tools import tool, SerperDevTool
from src.news.lib.utils import gget
import os
# ╔═════════════════════════════════════════════════════════════
# ║ Serper Search Tools Class
# ╚═════════════════════════════════════════════════════════════
class SerperSearch():
    @tool
    def search(query: str):
        """Search the web for information on a given topic"""
        try:
            rs = SerperDevTool(api_key=gget("SERPER_API_KEY").run(query))
            print(Fore.WHITE+Back.MAGENTA+f"{query}")
            print(Fore.WHITE+Back.MAGENTA+f"{rs}"+Fore.RESET+Back.RESET)
            return rs
        except Exception as e:
            raise e
    def tools():
        return [SerperSearch.search]