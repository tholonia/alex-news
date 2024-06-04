#!/bin/env python
#~~ get env vars first
from dotenv import load_dotenv
load_dotenv("/home/jw/src/crewai/anews/.env",override=True)
import json

#~~ python imports
import os
import datetime
# from getpass import getpass
from pprint import pprint

#~~ 3rd party imports
from colorama import Fore, Back

#~~ AI related imports
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
                
from crewai_tools import Tool  
from crewai_tools import (DirectoryReadTool,  
                          FileReadTool,
                          DirectoryReadTool,
                          FileReadTool,
                          WebsiteSearchTool,
                          YoutubeChannelSearchTool,
                          YoutubeVideoSearchTool,
                          ScrapeWebsiteTool,
                          SerperDevTool,

                          
                        )                                                    
                           
from crewai.project import (CrewBase, agent, crew, task)

#~~ local lib imports
from src.news.lib.utils import (
    get_llm, 
    gget, 
    gput, 
    is_verbose,
    check_top_level_key, 
    filecounter, 
    make_filenames,
    load_workflow_from_yaml,
)

#~~ excluded until callbask is debugded
# from src.news.lib.tracing import (
#     on_task_completion,
#     on_task_error,
#     on_task_start,
#     on_task_progress,
#     on_task_complete,
#     on_agent_error,
#     on_agent_start,
#     on_agent_progress,
#     on_agent_complete,
# )


# Check if the 'reports' directory exists, and create it if it doesn't
# if not os.path.exists('reports'):
#     os.makedirs('reports')
     


search_name = "Search"
search_desc = "useful for when you need to answer questions about current events"
search_tool = False

if gget('searcher') == "EXA":
    print(f"Using Search API: EXA")
    from src.news.lib.exa_search_tool import ExaSearchToolFull
    search_tool = Tool(name=search_name, description=search_desc, func=ExaSearchToolFull._exa().search)

if gget('searcher') == "DDG":  # still get ratelimit error
    from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
    search = DuckDuckGoSearchAPIWrapper()
    search.region="us-en"
    search.safesearch="off"
    search.backend="html" # backend: api, html, lite.
    # search.max_results=1 # even with only 1 query it fails with RateLimit :/
    search_tool = Tool(name=search_name, description=search_desc, func=search.run)

if gget('searcher') == "SER":
    print(f"Using Search API: SER")
    # from langchain_community.utilities import GoogleSerperAPIWrapper
    # search = GoogleSerperAPIWrapper(params={"engine": "bing","gl": "us","hl": "en"})
    # search_tool = Tool(name=search_name, description=search_desc, func=search.run)
    search_tool = SerperDevTool()

# REF: https://python.langchain.com/v0.1/docs/integrations/providers/serpapi/
# REf: https://github.com/langchain-ai/langchain/issues/3485
print("1",gget('searcher'))
if gget('searcher') == "SAP": # defaults to SAP
    print("2",gget('searcher'))
    print(f"Using Search API: SAP")
    print(">>>",gget('SERPAPI_API_KEY'))
    # exit()
    import serpapi
    from langchain_community.utilities import SerpAPIWrapper
    search = SerpAPIWrapper(params={"engine": "bing","gl": "us","hl": "en"})
    # from crewai_tools import Tool
    search_tool = Tool(name=search_name, description=search_desc,func=search.run)







#~~ Instantiate tools
# search_tool = SerperDevTool()
# file_read_tool = FileReadTool(file_path= gget("inputfile"))
web_search_tool                 = WebsiteSearchTool(website="HTTPS://google.com")
this_DirectoryReadTool          = DirectoryReadTool()
this_FileReadTool               = FileReadTool()
this_WebsiteSearchTool          = WebsiteSearchTool()
this_YoutubeChannelSearchTool   = YoutubeChannelSearchTool()
this_YoutubeVideoSearchTool     = YoutubeVideoSearchTool()
this_ScrapeWebsiteTool          = ScrapeWebsiteTool()                      

tools_list = [
    search_tool,    
    web_search_tool,
    # this_DirectoryReadTool,
    # this_FileReadTool,
    # this_WebsiteSearchTool,
    this_YoutubeChannelSearchTool,
    this_YoutubeVideoSearchTool,
    this_ScrapeWebsiteTool,
]

#~~ instantiate the LLM 
llm_server_1 = get_llm(temperature=0.8)


#~~ define Crew class
@CrewBase
class AnewsCrew():
    """News Crew"""
    agents_config = "config/" + gget('agents_yaml')
    tasks_config = "config/" + gget('tasks_yaml')
#~~ AGENTS ══════════════════════════════════════════════════════════════════════════
    @agent
    def agent_1(self) -> Agent:
        """Gather the most current and relevant information on a specified topic using various sources available on the internet."""
        print(">>> A1 >>>",is_verbose(gget("verbose")))

        key = [1,'Researcher']
        rs = Agent(
                config=self.agents_config[key[1]],
                llm=llm_server_1,
                verbose=is_verbose(gget("verbose")),
                allow_delegation=bool(int(gget("delegation"))),
                output_file=gput(f"agent_{key[0]}_outputfile",f"{gget('report_subdir')}-A{key[0]}-{filecounter()}.md"),
                tools=[search_tool,web_search_tool],
        )
        return rs # returned separatly for debugging purposes
            
    @agent
    def agent_2(self) -> Agent:      
        """ Review the research reports to ensure accuracy, completeness, and quality."""  
        key = [2,'Research_Manager']
        print(">>> A2 >>>",is_verbose(gget("verbose")))
        rs = Agent(
                config=self.agents_config[key[1]],
                llm=llm_server_1,
                verbose=is_verbose(gget("verbose")),
                allow_delegation=bool(int(gget("delegation"))),
                output_file=gput(f"agent_{key[0]}_outputfile",f"{gget('report_subdir')}-A{key[0]}-{filecounter()}.md"),
                tools= tools_list,
        )
        return rs
    
    @agent
    def agent_3(self) -> Agent:      
        """Format the final research report"""  
        key = [3,'Publisher']
        print(">>> A3 >>>",is_verbose(gget("verbose")))
        rs = Agent(
                config=self.agents_config[key[1]],
                llm=llm_server_1,
                verbose=is_verbose(gget("verbose")),
                allow_delegation=bool(int(gget("delegation"))),
                output_file=gput(f"agent_{key[0]}_outputfile",f"{gget('report_subdir')}-A{key[0]}-{filecounter()}.md"),
                tools= tools_list,
        )
        return rs

#~~ TASKS ══════════════════════════════════════════════════════════════════════════
    @task
    def task_1(self) -> Task:
        """task to search and collect information"""  
        key = [1,'Research_Information']
        print(">>> T1 >>>",is_verbose(gget("verbose")))
        rs = Task(
                config=self.tasks_config[key[1]],
                output_file=gput(f"task_{key[0]}_outputfile",f"{gget('report_subdir')}-T{key[0]}-{filecounter()}.md"),
                verbose=is_verbose(gget("verbose")),
                agent=self.agent_1(),
        )
        return rs
    
    @task
    def task_2(self) -> Task:
        """task to review information"""  
        key = [2,'Review_Research']
        print(">>> T2 >>>",is_verbose(gget("verbose")))
        rs = Task(
                config=self.tasks_config[key[1]],
                output_file=gput(f"task_{key[0]}_outputfile",f"{gget('report_subdir')}-T{key[0]}-{filecounter()}.md"),
                verbose=is_verbose(gget("verbose")),
                agent=self.agent_2(),
        )
        return rs    

    @task
    def task_3(self) -> Task:
        """task to publish information"""  
        key = [3,'Format_for_Publication']
        rs = Task(
                config=self.tasks_config[key[1]],
                output_file=gput(f"task_{key[0]}_outputfile",f"{gget('report_subdir')}-T{key[0]}-{filecounter()}.md"),
                verbose=is_verbose(gget("verbose")),
                agent=self.agent_3(),
        )
        return rs

#~~ CREW
    @crew
    def crew(self) -> Crew:     
        print(">>> C >>>",bool(int(gget("verbose"))))
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            
            
            verbose=bool(int(gget("verbose"))),
            process=Process.sequential
        )
        


