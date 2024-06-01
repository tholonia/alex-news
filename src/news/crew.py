#!/bin/env python

from dotenv import load_dotenv
load_dotenv("/home/jw/src/crewai/anews/.env",override=True)

import os
import datetime
# from getpass import getpass
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from textwrap import dedent

# ↑ uncomment to use OpenAI's API
# from langchain_groq import ChatGroq
# ↑ uncomment to use Groq's API
# from langchain_anthropic import ChatAnthropic
# ↑ uncomment to use Antrhopic's API
# from langchain_community.chat_models import ChatCohere
# ↑ uncomment to use ChatCohere API
# os.environ["SERPER_API_KEY"] = os.environ['xOPENAI_API_KEY']
# ↑ uncomment to use OpenAI's API
# os.environ["GROQ_API_KEY"] = getpass("Enter GROQ_API_KEY: ")
# ↑ uncomment to use Groq's API
# os.environ["ANTHROPIC_API_KEY"] = getpass("Enter ANTHROPIC_API_KEY: ")
# ↑ uncomment to use Anthropic's API
# os.environ["COHERE_API_KEY"] = getpass("Enter COHERE_API_KEY: ")
# ↑ uncomment to use Cohere's API

# Check if the 'output-files' directory exists, and create it if it doesn't
if not os.path.exists('reports'):
    os.makedirs('reports')
     

# @title 🔑 Input **Serper** API Key by running this cell

from crewai_tools import SerperDevTool

from crewai.project import (
    CrewBase,
    agent,
    crew,
    task,

)
# Instantiate tools

# Set the SERPER_API_KEY environment variable by prompting the user to enter the key
# The Serper API key is required to use the Serper search tool (https://serper.dev)
# os.environ["SERPER_API_KEY"] = '46xxxx2ab'


# Create an instance of the SerperDevTool class
# This tool allows performing searches using the Serper API
search_tool = SerperDevTool()
     

# @title 🕵🏻 Define your agents

# Agent Definitions

@CrewBase
class AnewsCrew():
    """News Crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def agent_1(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_1'],
            tools=[search_tool],
            llm=ChatOpenAI(model_name="gpt-4", temperature=0.8)
        )

    @agent
    def agent_2(self) -> Agent:        
        return Agent(
            config=self.agents_config['agent_2'],
            tools=[search_tool],
            llm=ChatOpenAI(model_name="gpt-4", temperature=0.8)
        )
  
    @agent
    def agent_3(self) -> Agent:
        return Agent(
            config=self.agents_config['agent_3'],
            tools=[search_tool],
            llm=ChatOpenAI(model_name="gpt-4", temperature=0.8)
        )
            

    # @title 📝 Define your tasks
    # Task Definitions

    @task
    def task_1(self) -> Task:
        return Task(
            config=self.tasks_config['task_1'],
            agent=self.agent_1(),
        )
    @task
    def task_2(self) -> Task:
        return Task(
            config=self.tasks_config['task_1'],
            agent=self.agent_2(),
        )
    @task
    def task_3(self) -> Task:
        return Task(
            config=self.tasks_config['task_1'],
            agent=self.agent_3(),
        )
        



    # @title 🚀 Get your crew to work!
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=2,  # You can set it to 1 or 2 to different logging levels
            # ↑ indicates the verbosity level for logging during execution.
            process=Process.sequential
            # ↑ the process flow that the crew will follow (e.g., sequential, hierarchical).
        )
