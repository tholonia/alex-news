from colorama import Back, Fore 
from pprint import pprint
import functools
from src.news.lib.utils import tryit

"""
These routines are for creating a decorator that trckas the entering and exiting of an agent opr task.
Sadly, it turned out to be useless in debugging, but keeping teh code here because it was a bit
of work to figure it.

It called before an agent or task definition with:

```
@agent_tracer(
    before_func=pre(
        name="reporting_analyst", 
        colors=F.GREEN+B.BLACK
    ), 
    after_func=post(
        name="reporting_analyst",
        colors=F.GREEN+B.BLACK,
    )
)
def some_agent(self) -> Agent:
        return Agent(...)
```


The colors are to make the output distinguishable, and the name is just a label.

def pre(name, colors):
# def pre(args,kwargs):
    # print("-------------------------------------------------------------------------")
    # pprint(args)
    # pprint(kwargs)
    # print("=========================================================================")
    # print(Fore.LIGHTWHITE_EX + Back.RED + f"{colors}" + Fore.RESET)
    print(colors, flush=True,end="")
    print(f"ENTERING {name}", flush=True,end="")
    print(Fore.RESET+Back.RESET,flush=True,)

def post(name,colors):
    print(colors, flush=True,end="")
    print(f"LEAVING {name}", flush=True,end="")
    print(Fore.RESET+Back.RESET, flush=True,)
    
def agent_tracer(before_func=None, after_func=None, **kwargs):
    def decorator(target_func):
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func()
            return result
        return wrapper
    return decorator

def task_tracer(before_func=None, after_func=None, **kwargs):

    def decorator(target_func):
        @functools.wraps(target_func)
        def wrapper(*args, **kwargs):
            if before_func:
                before_func(*args, **kwargs)
            result = target_func(*args, **kwargs)
            if after_func:
                after_func(*args, **kwargs)
            return result
        return wrapper
    return decorator
    
"""
    
# def on_task_completion(obj,**kwargs):
def on_task_completion(output):
    print(Fore.BLACK+Back.GREEN)
    print(output)
    print(Fore.RESET+Back.RESET)
    return()
    import json
    print(Fore.BLACK+Back.GREEN)
    name = tryit(kwargs,"name","none")
    print(f"├─  {name} has finished  ─┤")

    print(">>> kwargs:")
    pprint(kwargs)
    print(json.dumps(obj.__dict__,indent=4))

    print(Fore.RESET+Back.RESET)

# Define callback functions

# TASKS
def on_task_start(task):
    print(Back.YELLOW+f"Task {task.description} has started."+Back.RESET)

def on_task_complete(task, result):
    print(Back.MAGENTA+f"Task {task.description} completed.")
    print(f"Output: {result}"+Back.RESET)

def on_task_error(task, error):
    print(Back.CYAN+f"Task {task.description} encountered an error: {error}"+Back.RESET)

def on_task_progress(task, progress):
    print(Back.GREEN+f"Task {task.description} progress: {progress}"+Back.RESET) 
    
# AGENTS
def on_agent_start(agent):
    print(Back.YELLOW+f"Agent {agent.role} has started."+Back.RESET)

def on_agent_complete(agent, result):
    print(Back.YELLOW+f"Agent {agent.role} completed their task."+Back.RESET)
    print(f"Output: {result}")

def on_agent_error(agent, error):
    print(Back.YELLOW+f"Agent {agent.role} encountered an error: {error}"+Back.RESET)

def on_agent_progress(agent, progress):
    print(Back.YELLOW+f"Agent {agent.role} progress: {progress}"+Back.RESET)
        
    