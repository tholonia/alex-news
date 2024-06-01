# Python imports
import os
from pprint import pprint
from logging import log, basicConfig

basicConfig(level="INFO")

# Crew/Langchain imports
from crewai import Agent, Crew, Process, Task
