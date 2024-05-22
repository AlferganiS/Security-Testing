"""
Use this file to implement your solution for exercise 5-1 b.
"""

from exercise_1a import *
from fuzzingbook.Coverage import Location

def lcsaj_n(trace: list[Location], n: int) -> set[tuple[Location, ...]]:
    if n >= 0:
        subsequent_lines_n = set()
        parsed_trace = list(lcsaj(trace))
        parsed_trace.sort()
        if n  > len(parsed_trace):
            return subsequent_lines_n
        
        subsequent_lines_n = {tuple(parsed_trace[i:i+n]) for i in range(len(parsed_trace) - n + 1)}

        return subsequent_lines_n

    
trace = [ 
    ('f', 2), 
    ('f', 3), 
    ('f', 5), 
    ('f', 6), 
    ('f', 8), 
] 

# print(lcsaj_n(trace, 2))



