
import dotenv
import os
import platform
import sys
from pprint import pprint
from importlib.metadata import version
from dateutil.relativedelta import relativedelta
from datetime import datetime
import datetime as fubared_datetime # python's datetime functions are very badly designed (see note in code)




def get_llm():
    from langchain_openai import ChatOpenAI as OpenAI

    llm_server = OpenAI(
        openai_api_base=gget("LIVE_API_BASE_URL"),
        openai_api_key=gget("LIVE_API_KEY"),
        model=gget("LIVE_MODEL_NAME"),
        temperature=0.3,
        verbose=is_verbose(gget("verbose")),
        max_tokens=4096,  # gpt-3.5 max_tokens = 4096
    )
    return llm_server


def test_prefix(substring):
    """
    Checks if the given substring matches any part of the file names in the ./configs directory.

    :param substring: The substring to search for in the file names.
    :return: True of match, otherwise False
    """
    directory = "src/news/config"
    # Ensure the directory exists
    if not os.path.isdir(directory):
        print(f"The directory {directory} does not exist.")
        exit()

    # Iterate through each file in the directory
    for file_name in os.listdir(directory):
        # Check if the substring is in the file name
        if substring in file_name:
            return True
    return False
 
def tryit(kwargs, arg, default):
    """assign a vale to var from a kwargs ary, or set to default """
    try:
        rs = kwargs[arg]
    except:
        rs = default
    return rs

def mkdir(directory_path):
    """
    Check if the directory exists, and if not, create it.
    :param directory_path: Path of the directory to check/create.
    """
    if not os.path.exists(directory_path):
        # print(f"Directory '{directory_path}' does not exist. Creating it now.")
        os.makedirs(directory_path)
    else:
        pass
        # print(f"Directory '{directory_path}' already exists.")
    return directory_path

def gget(key):
    """
    The `gget` function retrieves a specific key from a .env file located at a specified path.
    
    :param key: The `key` parameter in the `gget` function is the key that you want to retrieve from the
    specified dotenv file located at "/home/jw/src/crewai/news/.env". This function is designed to fetch
    the value associated with the given key from the dotenv file
    :return: The `gget` function is returning the value associated with the specified key from the .env
    file located at "/home/jw/src/crewai/news/.env".
    """
    return dotenv.get_key(dotenv_path="/home/jw/src/crewai/news/.env",key_to_get=key)
#%% TODO 
def gput(key,val):
    """
    The `gput` function sets a key-value pair in a .env file and also updates the corresponding
    environment variable in Python.
    
    :param key: The `key` parameter in the `gput` function is a string representing the key under which
    the value will be stored in the environment variables and in the `.env` file. It is used to identify
    the specific value that you want to set or update
    :param val: The `val` parameter in the `gput` function is the value that you want to set for the
    specified key in the environment variables. In the provided code snippet, the `val` parameter is
    converted to a string using `str(val)` before setting it in the environment variables
    """
    val = str(val)
    # print(type(val))
    dotenv.set_key(dotenv_path="/home/jw/src/crewai/news/.env",key_to_set=key,value_to_set=val)
    os.environ[key]=val
    return val

def printstats(stage):
    """Prints stats and data before and after run"""
    
    before = f"""
    ┌──────────────────────────────────────────────────────────── 
    │           PROJECT_NAME: {gget("LANGCHAIN_PROJECT")} ({gget("server")})
    │      LIVE_API_BASE_URL: {gget("LIVE_API_BASE_URL")}
    │        LIVE_MODEL_NAME: {gget("LIVE_MODEL_NAME")}
    │                  Topic: |{gget("topic")}|
    │              InoutFile: |{gget("inputfile")}|
    │                Seacher: {gget("searcher")}
    │                Verbose: {gget("verbose")}/{is_verbose(gget("verbose"))}
    │                 Memory: {gget("memory")}
    │             Delegation: {gget("delegation")}
    │                 prefix: {gget("prefix")}
    │             Date Range: {gget("start_date")} - {gget("end_date")}
    │           Agent config: {gget("agents_yaml")}
    │            Task config: {gget("tasks_yaml")}
    └────────────────────────────────────────────────────────────
    """
     
    after = before + f"""
        Runtime: {gget("runtime")}
    
        Current versions
            langchain           {version('langchain')}
            langchain_community {version('langchain_community')}
            crewai              {version('crewai')}
            crewai_tools        {version('crewai_tools')}
            Python              {sys.version}
            System              {platform.system()} {platform.release()}
    """
    if stage == "before": print(before)
    if stage == "after": print(after)
    
def is_verbose(verbose):
    """The function `is_verbose` checks if a given value `verbose` is equal to 0 and returns True if it is not."""
    if verbose == 0:
        return False
    else:
        return True


def showhelp():
    print("help")
    rs = """
    -t, --topic       <search term, keywords>
    -v, --verbose     <0|1|2>                (default is app default, False)
    -s, --server      <LMS|OLLAMA|OPENAI|GOOGLE>
    -r, --daterange   <from:to>              (ex: 'yyyy/mm/dd:yyyy/mm/dd')
    -p, --prefix      <prefix string>        (ex: "btc", "default")
    -l, --llm         <LLM name>             (ex: "gpt-4-1106-preview"*,"dolphin-llama3", server dependant")
    -m, --memory      <0|1>                  (default is app default, False)
    -d, --delegation  <0|1>                  (default is app default, False)
    -S, --searcher    <SER|EXA|DDG>          (default is SER)
    
    switches
        -h, --help          show help        (this file)
    
    Notes:
    `daterange` also supports the format "<n> <units>|'yesterday'|'today ago:<n> <units>|'yesterday'|'today' ago
                            examples:
                                today:today 
                                5 hours ago:today
                                yesterday:today
                                32 days ago:10 days ago
                                4 months ago:1 month ago
                                1 years ago:today (default)
                                2 years ago:today
                        
    """
    print(rs)
    exit()


def update_live_env(prop,label): 
    """
    The function `update_env` updates a key-value pair in a .env file using values retrieved from
    another key in the environment.
    
    :param label: Label is a variable that represents a specific identifier or category. It is used to
    create dynamic keys for environment variables based on the label provided
    :param prop: It looks like the `prop` parameter in the `update_env` function is used to specify a
    property or attribute associated with a particular label. This property is used to construct keys
    for retrieving and setting values in the environment
    """
    stored_key = f"x{label}_{prop}"
    stored_val = gget(stored_key)
    # new_key = f"OPENAI_{prop}"
    new_key = f"LIVE_{prop}"

    dotenv.set_key(
        dotenv_path="./.env", # JWFIX
        key_to_set=new_key,
        value_to_set=stored_val,            
    ) 
    
    

def getdates(xstr):
    """
    The `getdates` function in Python takes a string input representing a date range and converts it
    into a formatted date range.
    
    :param xstr: It looks like the function `getdates` is designed to take a string `xstr` as input,
    which is expected to be in the format "YYYY/MM/DD:YYYY/MM/DD" or in test like "yesterday:today". The function then splits this input
    string into two parts, where the first part represents a start date and the second part the end date.
    :return: The `getdates` function is returning a list containing two elements: the formatted start
    date (`dfrom_fmt`) and the formatted end date (`dto_fmt`). These dates are formatted in the format
    "%B %d, %Y" (e.g., "January 01, 2022").
    """
    def get_past_date(str_days_ago:str):
        """from https://stackoverflow.com/questions/28268818/how-to-find-the-date-n-days-ago-in-python """
        """Here we call `fubared_datetime` because if datetime is called it conflicts with the datetime.datetime"""
        TODAY = fubared_datetime.date.today()
        gput("today",TODAY)
        splitted = str_days_ago.split()
        if len(splitted) == 1 and splitted[0].lower() == 'today':
            return str(TODAY.isoformat())
        elif len(splitted) == 1 and splitted[0].lower() == 'yesterday':
            date = TODAY - relativedelta(days=1)
            return str(date.isoformat())
        elif splitted[1].lower() in ['hour', 'hours', 'hr', 'hrs', 'h']:
            date = datetime.datetime.now() - relativedelta(hours=int(splitted[0]))
            return str(date.date().isoformat())
        elif splitted[1].lower() in ['day', 'days', 'd']:
            date = TODAY - relativedelta(days=int(splitted[0]))
            return str(date.isoformat())
        elif splitted[1].lower() in ['wk', 'wks', 'week', 'weeks', 'w']:
            date = TODAY - relativedelta(weeks=int(splitted[0]))
            return str(date.isoformat())
        elif splitted[1].lower() in ['mon', 'mons', 'month', 'months', 'm']:
            date = TODAY - relativedelta(months=int(splitted[0]))
            return str(date.isoformat())
        elif splitted[1].lower() in ['yrs', 'yr', 'years', 'year', 'y']:
            date = TODAY - relativedelta(years=int(splitted[0]))
            return str(date.isoformat())
        else:
            return "Wrong Argument format"

    if xstr.find("-") == -1:  # not YYYY/MM/DD:YYYY/MM/DD format
        ft = xstr.split(":")
        dfrom = get_past_date(ft[0])
        dto   = get_past_date(ft[1])
   
        # Convert the ISO date string to a datetime object, Format the datetime object to the desired format
        # date_obj = datetime.date.strftime(dfrom, "%Y-%m-%d")   
        # from date 
        date_obj = datetime.strptime(dfrom, "%Y-%m-%d")
        dfrom_fmt = date_obj.strftime("%B %d, %Y")
        # to date
        date_obj = datetime.strptime(dto, "%Y-%m-%d")
        dto_fmt  = date_obj.strftime("%B %d, %Y")
        
        return [dfrom_fmt,dto_fmt]
        
def new_project_name():
    """
    The function `new_project_name` increments a counter stored in a global variable, generates a new
    project name based on the counter value and a prefix extracted from another global variable, and
    updates the global variables with the new values.  This is used for tracking by at https://smith.langchain.com/.
    :return: The function `new_project_name` returns the new project name that is generated based on the
    existing project name and a counter value.
    """
    counter = int(gget('COUNTER'))
    counter +=1
    new_counter=f"{counter:03d}"
    name = gget("LANGCHAIN_PROJECT")
    name_part = name.split("_")[0]
    gput("COUNTER",str(counter))
    new_project_name = name_part+"_"+new_counter
    gput("LANGCHAIN_PROJECT",new_project_name)
    return new_project_name