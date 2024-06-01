#!/bin/env python

from dotenv import load_dotenv
load_dotenv("/home/jw/src/crewai/news/.env",override=True)

import os
# from getpass import getpass
from src.news.crew import AnewsCrew


def run():
    inputs = {
    "var_1": "bitcoin",
    "var_2": "news",
    "var_3": "March, 2024"
    }

    AnewsCrew().crew().kickoff(inputs=inputs)
    

