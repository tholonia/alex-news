#!/bin/env python
import requests
import dotenv
import os

from exa_py import Exa

dotenv.load_dotenv(dotenv_path='/home/jw/src/crewai/news/.env')

exa = Exa(os.environ['EXA_API_KEY'])

results = exa.search('hottest AI agent startups', use_autoprompt=True)

print(results)
