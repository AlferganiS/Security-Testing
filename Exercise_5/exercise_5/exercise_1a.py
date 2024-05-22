"""
Use this file to implement your solution for exercise 5-1 a.
"""
from fuzzingbook.Coverage import Location
from typing import List, Tuple, Set


def lcsaj(trace: List[Location]) -> Set[Tuple[Location, ...]]:
    subsequent_lines = set()
    current_tup = []

    for index, loc in enumerate(trace):
        current_tup.append(loc)
        current_line_number = loc[1]

        if index != 0:
            previous_line_number = trace[index - 1][1]

            if current_line_number != previous_line_number + 1:
                subsequent_lines.add(tuple(current_tup))
                current_tup = [loc]

    # Handle the last element of trace
    if current_tup:
        subsequent_lines.add(tuple(current_tup))

    return subsequent_lines
                
   


def f(x): 
    if x >= 10:      # L2 
        x = x % 10   # L3 
                     # L4 
    y = x - 5        # L5 
    if y < 0:        # L6 
        return 0     # L7 
    return y         # L8

trace = [ 
    ('f', 2), 
    ('f', 3), 
    ('f', 5), 
    ('f', 6), 
    ('f', 8), 
] 

# print(lcsaj(trace))