import random
# import the fuzzing book chapter here

from fuzzingbook.Fuzzer import fuzzer

if __name__ == '__main__':
    random.seed()
    data = fuzzer() # call the fuzzer function here to generate data
    with open('solution_3b.txt', 'w') as f:
        f.write(data)