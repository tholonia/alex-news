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
    
def on_task_completion(*args,**kwargs):
    print(Fore.BLACK+Back.GREEN)
    name = tryit(kwargs,"name","none")
    print(f"├─  {name} has finished  ─┤")

    print(Fore.RESET+Back.RESET)

def on_agent_completion(*args, **kwargs):
    print(Fore.GREEN+Back.RED)
    name = tryit(kwargs,"name","none")
    print(f"├─  {name} has finished  ─┤")
    # print(f"│  {agent_result}")
    print(Fore.RESET+Back.RESET)
