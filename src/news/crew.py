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
from src.news.lib.utils import (get_llm, gget, is_verbose,check_top_level_key)
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
    tasks_config = "config/" + gget('tasks_yaml')
    
    # /home/jw/src/crewai/anews/src/news/config/crypto_agents.yaml

    key1 = "agent_1"
    if check_top_level_key(f"src/news/{agents_config}",key1):
        @agent
        def agent_1(self) -> Agent:
            return Agent(
                config=self.agents_config[self.key1],
                tools=[search_tool],
                llm=llm_server_1,
                output_file=f"{report_subdir}/{gget('COUNTER')}-{self.key1}.md",
                verbose=is_verbose(gget("verbose")),
                allow_delegation=bool(int(gget("delegation"))),
                callback=on_agent_completion(name=self.key1),            
            )
    else:
        print(f"Missing '{key1}' in src/news/{agents_config}")
            
    key2 = "agent_2"
    if check_top_level_key(f"src/news/{agents_config}",key2):
        @agent
        def agent_2(self) -> Agent:        
            return Agent(
                config=self.agents_config[self.key2],
                tools=[search_tool],
                llm=llm_server_1,
                output_file=f"{report_subdir}/{gget('COUNTER')}-{self.key2}.md",
                verbose=is_verbose(gget("verbose")),
                allow_delegation=bool(int(gget("delegation"))),
                callback=on_agent_completion(name=self.key2),
            )
    else:
        print(f"Missing '{key2}' in src/news/{agents_config}")


    key3 = "agent_3"
    if check_top_level_key(f"src/news/{agents_config}",key3):
        @agent
        def agent_3(self) -> Agent:
            return Agent(
                config=self.agents_config[self.key3],
                tools=[search_tool],
                llm=llm_server_1,
                output_file=f"{report_subdir}/{gget('COUNTER')}-{self.key3}.md",
                verbose=is_verbose(gget("verbose")),
                allow_delegation=bool(int(gget("delegation"))),
                callback=on_agent_completion(name=self.key3),
            )
    else:
        print(f"Missing '{key3}' in src/news/{agents_config}")
            

    # @title 📝 Define your tasks
    # Task Definitions

    task_key1 = "task_1"
    if check_top_level_key(f"src/news/{tasks_config}",task_key1):
        @task
        def task_1(self) -> Task:
            return Task(
                config=self.tasks_config[self.task_key1],
                agent=self.agent_1(),
                output_file=f"{report_subdir}/{gget('COUNTER')}-{self.task_key1}.md",
                callback=on_task_completion(name=self.task_key1),            
            )
    else:
        print(f"Missing '{task_key1}' in src/news/{tasks_config}")

    task_key2 = "task_2"
    if check_top_level_key(f"src/news/{tasks_config}",task_key2):
        @task
        def task_1(self) -> Task:
            return Task(
                config=self.tasks_config[self.task_key2],
                agent=self.agent_1(),
                output_file=f"{report_subdir}/{gget('COUNTER')}-{self.task_key2}.md",
                callback=on_task_completion(name=self.task_key2),            
            )
    else:
        print(f"Missing '{task_key2}' in src/news/{tasks_config}")


    task_key3 = "task_3"
    if check_top_level_key(f"src/news/{tasks_config}",task_key3):
        @task
        def task_1(self) -> Task:
            return Task(
                config=self.tasks_config[self.task_key3],
                agent=self.agent_1(),
                output_file=f"{report_subdir}/{gget('COUNTER')}-{self.task_key3}.md",
                callback=on_task_completion(name=self.task_key3),
            )
    else:
        print(f"Missing '{task_key3}' in src/news/{tasks_config}")



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
