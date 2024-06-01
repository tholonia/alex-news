#!/bin/env python
#~~ get env vars first
from dotenv import load_dotenv
load_dotenv("/home/jw/src/crewai/anews/.env",override=True)

#~~ python imports
import os
import datetime
# from getpass import getpass

#~~ AI related imports
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai_tools import (SerperDevTool, FileReadTool)
from crewai.project import (CrewBase, agent, crew, task)

#~~ local lib imports
from src.news.lib.utils import (get_llm, gget, is_verbose)
from src.news.lib.tracing import (on_task_completion, on_agent_completion)
 
# Check if the 'reports' directory exists, and create it if it doesn't
if not os.path.exists('reports'):
    os.makedirs('reports')
     

#~~ create filenames
topic_stub=gget('topic')[:10].replace(" ", "-")
report_subdir = f"reports/reports-{topic_stub}-{gget('server')[:3]}-{gget('LIVE_MODEL_NAME')}"

#~~ Instantiate tools
search_tool = SerperDevTool()
# file_read_tool = FileReadTool(file_path= gget("inputfile"))
# web_search_tool = WebsiteSearchTool(website="HTTPS://google.com")
# web_rag_tool = RagTool     

#~~ instantiate the LLM 
llm_server_1 = get_llm()


#~~ define Crew class
@CrewBase
class AnewsCrew():
    """News Crew"""
    agents_config = "config/" + gget('agents_yaml')
    tasks_config = f"config/" + gget('tasks_yaml')

    @agent
    def agent_1(self) -> Agent:
        stub = "agent_1"
        return Agent(
            config=self.agents_config['agent_1'],
            tools=[search_tool],
            llm=llm_server_1,
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            verbose=is_verbose(gget("verbose")),
            allow_delegation=bool(int(gget("delegation"))),
            callback=on_agent_completion(name=stub),            
        )

    @agent
    def agent_2(self) -> Agent:        
        stub = "agent_2"
        return Agent(
            config=self.agents_config['agent_2'],
            tools=[search_tool],
            llm=llm_server_1,
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            verbose=is_verbose(gget("verbose")),
            allow_delegation=bool(int(gget("delegation"))),
            callback=on_agent_completion(name=stub),
        )
  
    @agent
    def agent_3(self) -> Agent:
        stub = "agent_3"
        return Agent(
            config=self.agents_config['agent_3'],
            tools=[search_tool],
            llm=llm_server_1,
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            verbose=is_verbose(gget("verbose")),
            allow_delegation=bool(int(gget("delegation"))),
            callback=on_agent_completion(name=stub),
        )
            

    # @title 📝 Define your tasks
    # Task Definitions

    @task
    def task_1(self) -> Task:
        stub = "task_1"
        return Task(
            config=self.tasks_config['task_1'],
            agent=self.agent_1(),
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            callback=on_task_completion(name=stub),            
        )
    @task
    def task_2(self) -> Task:
        stub = "task_2"
        return Task(
            config=self.tasks_config['task_1'],
            agent=self.agent_2(),
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            callback=on_task_completion(name=stub),
        )
    @task
    def task_3(self) -> Task:
        stub = "task_3"
        return Task(
            config=self.tasks_config['task_1'],
            agent=self.agent_3(),
            output_file=f"{report_subdir}/{gget('COUNTER')}-{stub}.md",
            callback=on_task_completion(name=stub),
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
