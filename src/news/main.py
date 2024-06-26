#~~ first load env vars 
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env', override=True)

#~~ python pkgs
import sys, getopt, time

#~~ local lib 
from src.news.lib.utils import (
    gget,
    gput,
    update_live_env,
    new_project_name,
    getdates,
    showhelp,
    printstats,
    test_prefix,
    make_filenames,
)
from src.news.lib.setserver import set_server
# needs internet
#~~ 3rd party
# enable to turn on remote realtime monitoring
# from langsmith.wrappers import wrap_openai
# from langsmith import traceable


#~~ Initialize vars to defaults
# start_date, end_date = getdates("100 years ago:today") or (0, 0)
start_date, end_date =      getdates("1 months ago:today") or (0, 0)
gput('start_date',          start_date)  # Defaults to 100 years ago
gput('end_date',            end_date)  # Defaults to today
gput('searcher',            'SER')  # Defaults to Serper
gput("LANGCHAIN_PROJECT",   new_project_name())
gput("inputfile",           "None") 
gput("topic",               "None") #%% TODO 
gput("agents_yaml",         "agents.yaml") 
gput("tasks_yaml",          "tasks.yaml") 
gput("prefix",              "test") 
gput("topic",               "Bitcoin") 
gput("filecounter",         "000") 
gput("task_1_outputfile",   "undefined")
gput("agent_1_outputfile",  "undefined")
gput("task_2_outputfile",   "undefined")
gput("agent_2_outputfile",  "undefined")


#~~ Parse command-line arguments provided
try:
    opts, args = getopt.getopt(
        sys.argv[1:], "ht:v:m:s:r:p:l:d:S:i:", 
            ["help","topic=","verbose=","memory=","server=", "daterange=","prefix=","llm=","delegation=","searcher=","inputfile="])
except getopt.GetoptError as e:
    print(str(e))
    showhelp()
    sys.exit(2)

for opt, arg in opts:
    """_summary_
    Test to see if 'topic' can be used as a prefix, if not defer to the -p, --prefix argument'
    """
    if opt in ("-t", "--topic"):        # if topic is provided...
        gput("topic", arg)                  # set topic to arg    
        if test_prefix(arg):                # if topic matches a prefix...
            gput("prefix", arg)                 # set prefix = topic   
        elif opt in ("-p", "--prefix"):     # otherwise, if there is a prefix already provided...
            arg = arg.replace("'","")           # clean it...
            gput("prefix", arg)                 # set prefix = topic
    elif opt in ("-p", "--prefix"):     # Otherwise if there is a prefix already provided...
        arg = arg.replace("'","")            # clean
        gput("prefix", arg)                  # set prefix = prefix  
    elif opt in ("-h", "--help"):       showhelp()
    elif opt in ("-m", "--memory"):     gput("memory", int(arg))
    elif opt in ("-d", "--delegation"): gput("delegation", int(arg))
    elif opt in ("-v", "--verbose"):    gput("verbose", int(arg))
    elif opt in ("-l", "--llm"):        gput("LIVE_MODEL_NAME", arg)
    elif opt in ("-S", "--searcher"):   gput("searcher", arg)
    elif opt in ("-i", "--inputfile"):  gput("inputfile", arg)
    elif opt in ("-r", "--daterange"):
        thesedates = getdates(arg)
        gput("start_date", thesedates[0])
        gput("end_date", thesedates[1])                
    elif opt in ("-s", "--server"):
        gput("server", set_server(arg)) 
        update_live_env("SERVER",arg)
        update_live_env("API_BASE_URL",arg)
        update_live_env("API_KEY",arg)
        update_live_env("MODEL_NAME",arg)
        
#~~ update defaults with new data
agents_yaml = f"{gget('prefix')}_agents.yaml"
tasks_yaml = f"{gget('prefix')}_tasks.yaml"
gput("agents_yaml", agents_yaml)
gput("tasks_yaml", tasks_yaml)
#~~ create filenames agents and tasks to save to
gput("report_subdir", make_filenames()+"/"+gget('COUNTER')+"/"+gget('searcher'))

# If there IS a specified inputfile AND no topic specified, make the topic the name inputfile name
if gget("inputfile") != "None" and (gget("topic") == "None" or gget("topic") == ""): 
    gput("topic",gget("inputfile")) # Defaults to Serperinput  
    
#~~ load and run the crew
from src.news.crew import AnewsCrew
def run():
    """
    The `run` function prints statistics before and after kicking off a NewsCrew task with specified
    inputs and measures the runtime.
    """
    printstats("before")
    input("Enter to continue (^C to break)")
    inputs = {
        "topic": gget("topic"),
        "start_date": start_date,
        "end_date": end_date,
    }
    start_timer = time.time()
    news_crew_instance = AnewsCrew()
    
    news_crew_instance.crew().kickoff(inputs=inputs)
    gput("runtime", int(time.time() - start_timer))
    printstats("after")    
    

    """
Action:
Delegate work to coworker
Action Input:
{
    "task": "Review and annotate the research report on 'The rise in Dengue' to ensure accuracy, completeness, and quality. Provide detailed feedback and suggestions for improvement.",
    "coworker": "Gather the most relevant information on the subject of 'The rise in Dengue' using various sources available on the internet."
} 


Error executing tool. coworker mentioned not found, it must to be one of the following options:
- gather the most relevant information on the subject of 'the rise in denge' using various sources available on the internet.

- format the final research report in the best possible way for publication, ensuring it is organized, clear, and visually appealing.
    
    
    
    """