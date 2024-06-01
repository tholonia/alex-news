#~~ first load env vars 
import dotenv 
dotenv.load_dotenv(dotenv_path='/home/jw/src/crewai/anews/.env', override=True)

#~~ python pkgs
import sys
import getopt
import time

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
)

from src.news.lib.setserver import set_server
# needs internet

#~~ 3rd party
#~~ -- enable to turn on remote realtime monitoring
# from langsmith.wrappers import wrap_openai
# from langsmith import traceable


#~~ Initialize vars to defaults
start_date, end_date = getdates("100 years ago:today") or (0, 0)
gput('start_date', start_date)  # Defaults to 100 years ago
gput('end_date', end_date)  # Defaults to today
gput('searcher', 'SER')  # Defaults to Serper
gput("LANGCHAIN_PROJECT", new_project_name())
gput("inputfile","None") 
gput("topic","None") #%% TODO 
gput("agents_yaml","agents.yaml") 
gput("tasks_yaml","tasks.yaml") 
gput("prefix","test") 


#~~ Parse command-line arguments provided
try:
    opts, args = getopt.getopt(sys.argv[1:], "ht:v:m:s:r:p:l:d:S:i:", 
                                 ["help","topic=","verbose=","memory=","server=",
                                  "daterange=","prefix=","llm=","delegation=","searcher=","inputfile="])
except getopt.GetoptError as e:
    print(str(e))
    showhelp()
    sys.exit(2)

for opt, arg in opts:
    """_summary_
    Test to see if 'topic' can be used as a prefix, if not defer to the -p, --prefix argument'
    """
    if opt in ("-t", "--topic"):
        gput("topic", arg)
        if test_prefix(arg):
            gput("prefix", arg)  # set prefix of there is a match   
        elif opt in ("-p", "--prefix"): #otherwise use expliciet -p arg
            arg = arg.replace("'","")
            gput("prefix", arg)
            
    if opt in ("-h", "--help"):       showhelp()
    elif opt in ("-m", "--memory"):     gput("memory", int(arg))
    elif opt in ("-d", "--delegation"): gput("delegation", int(arg))
    elif opt in ("-v", "--verbose"):    gput("verbose", int(arg))
    elif opt in ("-l", "--llm"):        gput("LIVE_MODEL_NAME", arg)
    elif opt in ("-S", "--searcher"):   gput("searcher", arg)
    elif opt in ("-i", "--inputfile"):  gput("inputfile", arg)
    
    if opt in ("-r", "--daterange"):
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


# If there is IS a specified inputfile AND no topic specified, make the topic the name inputfile name
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
    
    inputs = {
    "var_1": "bitcoin",
    "var_2": "news",
    "var_3": "March, 2024"
    }

    start_timer = time.time()
    AnewsCrew().crew().kickoff(inputs=inputs)
    gput("runtime", int(time.time() - start_timer))
    printstats("after")    


