#!/bin/env python
#~~ get env vars first
from dotenv import load_dotenv
load_dotenv("/home/jw/src/crewai/anews/.env",override=True)
from colorama import Fore, Back
import json

#~~ python imports
import os
import datetime
# from getpass import getpass
from pprint import pprint

#~~ AI related imports
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from crewai_tools import (SerperDevTool, FileReadTool)
from crewai.project import (CrewBase, agent, crew, task)

#~~ local lib imports
from src.news.lib.utils import (
    get_llm, 
    gget, 
    gput, 
    is_verbose,
    check_top_level_key, 
    filecounter, 
)
from src.news.lib.tracing import (
    on_task_completion,
    on_task_error,
    on_task_start,
    on_task_progress,
    on_task_complete,
    on_agent_error,
    on_agent_start,
    on_agent_progress,
    on_agent_complete,
)


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
llm_server_1 = get_llm(temperature=0.2)


#~~ define Crew class
@CrewBase
class AnewsCrew():
    """News Crew"""
    agents_config = "config/" + gget('agents_yaml')
    tasks_config = "config/" + gget('tasks_yaml')
    
    # /home/jw/src/crewai/anews/src/news/config/crypto_agents.yaml

    agent_key1 = "agent_1"
    if check_top_level_key(f"src/news/{agents_config}",agent_key1):
        @agent
        def agent_1(self) -> Agent:
            output_file=f"{report_subdir}/{gget('COUNTER')}-{self.agent_key1}-{filecounter()}.md"
            gput("agent_1_outputfile",output_file)
            rs = Agent(
                config=self.agents_config[self.agent_key1],
                tools=[search_tool],
                llm=llm_server_1,
                output_file=output_file,
                verbose=is_verbose(gget("verbose")),
                allow_delegation=bool(int(gget("delegation"))),
                #~~ `callbacks` is BUGGY AS HELL... `callback` works
               
                # callbacks={
                #     "on_start": on_agent_start,
                #     "on_complete": on_agent_complete,
                #     "on_error": on_agent_error,
                #     "on_progress": on_agent_progress
                # }
                # callbacks=[
                #     {"event": "on_start", "callback": on_agent_start},
                #     {"event": "on_complete", "callback": on_agent_complete},
                #     {"event": "on_error", "callback": on_agent_error},
                #     {"event": "on_progress", "callback": on_agent_progress}
                # ]
            )
            # # dump the returned object
            # print(Back.BLUE,Fore.WHITE)
            # pprint(rs.__dict__)
            # print(Back.RESET, Fore.RESET)

            return rs
    else:
        print(f"Undefined '{agent_key1}' in src/news/{agents_config}")
            
    agent_key2 = "agent_2"
    if check_top_level_key(f"src/news/{agents_config}",agent_key2):
        @agent
        def agent_2(self) -> Agent:        
            output_file=f"{report_subdir}/{gget('COUNTER')}-{self.agent_key2}-{filecounter()}.md"
            gput("agent_2_outputfile",output_file)
            rs = Agent(
                config=self.agents_config[self.agent_key2],
                tools=[search_tool],
                llm=llm_server_1,
                output_file=output_file,
                verbose=is_verbose(gget("verbose")),
                allow_delegation=bool(int(gget("delegation"))),
                # callback=on_agent_completion(name=self.agent_key2),
            )
            return rs
    else:
        print(f"Undefined '{agent_key2}' in src/news/{agents_config}")


    agent_key3 = "agent_3"
    if check_top_level_key(f"src/news/{agents_config}",agent_key3):
        @agent
        def agent_3(self) -> Agent:
            output_file=f"{report_subdir}/{gget('COUNTER')}-{self.agent_key3}-{filecounter()}.md"
            gput("agent_3_outputfile",output_file)
            rs = Agent(
                config=self.agents_config[self.agent_key3],
                tools=[search_tool],
                llm=llm_server_1,
                output_file=output_file,
                verbose=is_verbose(gget("verbose")),
                allow_delegation=bool(int(gget("delegation"))),
                # callback=on_agent_completion(name=self.agent_key3),
            )
            return rs
    else:
        print(f"Undefined '{agent_key3}' in src/news/{agents_config}")
            

    # @title 📝 Define your tasks
    # Task Definitions

    task_key1 = "task_1"
    if check_top_level_key(f"src/news/{tasks_config}",task_key1):
        @task
        def task_1(self) -> Task:
            output_file=f"{report_subdir}/{gget('COUNTER')}-{self.task_key1}-{filecounter()}.md"
            gput("task_1_outputfile",output_file)
            rs = Task(
                config=self.tasks_config[self.task_key1],
                agent=self.agent_1(),
                output_file=output_file,
                #~~ `callbacks` is BUGGY AS HELL... `callback` works
                # callback=on_task_completion,  # with no args it sends  results            
                # callback=on_task_completion(self,name=self.task_key1),   # with args, no results are sent... which I do not understand         
                # callbacks={
                #         "on_start": on_task_start,
                #         "on_complete": on_task_complete,
                #         "on_error": on_task_error,
                #         "on_progress": on_task_progress
                # }
            )
            
            # # dump the returned object
            # print(Back.GREEN,Fore.BLACK)
            # pprint(rs.__dict__)
            # print(Back.RESET, Fore.RESET)

            return rs
    else:
        print(f"Undefined '{task_key1}' in src/news/{tasks_config}")

    task_key2 = "task_2"
    if check_top_level_key(f"src/news/{tasks_config}",task_key2):
        @task
        def task_1(self) -> Task:
            output_file=f"{report_subdir}/{gget('COUNTER')}-{self.task_key2}-{filecounter()}.md"
            gput("task_2_outputfile",output_file)
            rs = Task(
                config=self.tasks_config[self.task_key2],
                agent=self.agent_1(),
                output_file=output_file,
                # callback=on_task_completion(name=self.task_key2),            
            )
            return rs
    else:
        print(f"Undefined '{task_key2}' in src/news/{tasks_config}")


    task_key3 = "task_3"
    if check_top_level_key(f"src/news/{tasks_config}",task_key3):
        @task
        def task_1(self) -> Task:
            output_file=f"{report_subdir}/{gget('COUNTER')}-{self.task_key3}-{filecounter()}.md"
            gput("task_3_outputfile",output_file)
            rs = Task(
                config=self.tasks_config[self.task_key3],
                agent=self.agent_1(),
                output_file=output_file,
                # callback=on_task_completion(name=self.task_key3),
            )
            return rs
    else:
        print(f"Undefined '{task_key3}' in src/news/{tasks_config}")



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
