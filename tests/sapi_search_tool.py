import dotenv
dotenv.load_dotenv("/.env")

from langchain_community.utilities import SerpAPIWrapper
# os.environ['SERPAPI_API_KEY']="f47f3ba78d4b7044f5d7fddcf700e0f9f925fd07e3916044a798ca2a2df8b33b"
params = {"engine": "bing","gl": "us","hl": "en"}

search = SerpAPIWrapper(params=params)
print(search.run("Obama's first name?"))
exit()
from langchain.agents import Tool
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=search.run,
)