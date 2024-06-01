import os
import dotenv
dotenv.load_dotenv("/.env", override=True)
from pprint import pprint
from langchain_community.utilities import SerpAPIWrapper

print(os.environ['SERPAPI_API_KEY'])

serpapi = SerpAPIWrapper()
pprint(dict(serpapi))

rs = serpapi.run("coffee")

pprint(rs)

