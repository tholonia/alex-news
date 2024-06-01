from crewai_tools import tool
from exa_py import Exa
from src.news.lib.utils import gget
import dotenv
dotenv.load_dotenv(dotenv_path="/home/jw/src/crewai/news/.env")
class ExaSearchToolFull:
    @tool
    def search(query: str):
        """Search for a webpage based on the query."""
        return ExaSearchToolFull._exa().search(
            f"{query}", use_autoprompt=True, num_results=3
        )

    @tool
    def find_similar(url: str):
        """Search for webpages similar to a given URL.
        The url passed in should be a URL returned from `search`.
        """
        return ExaSearchToolFull._exa().find_similar(url, num_results=3)

    @tool
    def get_contents(ids: str):
        """Get the contents of a webpage.
        The ids must be passed in as a list, a list of ids returned from `search`.
        """

        print("ids from param:", ids)

        ids = eval(ids)
        print("eval ids:", ids)

        contents = str(ExaSearchToolFull._exa().get_contents(ids))
        print(contents)
        contents = contents.split("URL:")
        contents = [content[:1000] for content in contents]
        return "\n\n".join(contents)

    def tools():
        return [
            ExaSearchToolFull.search,
            ExaSearchToolFull.find_similar,
            ExaSearchToolFull.get_contents,
        ]
    def _exa():
        return Exa(api_key=gget('EXA_API_KEY'))
