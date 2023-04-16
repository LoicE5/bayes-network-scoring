from time import time as now
from typing import Callable

def show_exec_time(func:Callable, args:list=[])->None:
    start_time = now()
    print(f"Output : {func(*args)}")
    print(f"{func.__name__} have been executed in {round(now() - start_time,3)} seconds")