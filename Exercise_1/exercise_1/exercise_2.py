from exercise_1 import levenshtein_distance
from fuzzingbook import Fuzzer

class FunctionRunner(Fuzzer.ProgramRunner):

    def run_process(self, inp: str = ""):
        # running the stored function (self.program) with the input (inp)
        return self.program(inp)
        
    def run(self, inp: str = ""):

        try:
            # Try running the function (self.run_process)
            result = (inp, self.run_process(inp))
            outcome = self.PASS

        except LookupError:
            # If a LookupError occurs, return None
            outcome = self.FAIL
            result = (inp, None)
        except:
            # For any other exception, return None
            outcome = self.UNRESOLVED
            result = (inp, None)

        return result, outcome

def ld_wrapper(inp):
    # Split the input string by '+'
    parts = inp.split('+')
    
    # If there are fewer than two splits, raise a ValueError
    if len(parts) < 2:
        raise ValueError("Input string must contain at least one '+'")

    # Calculate the Levenshtein distance between the first two parts
    result = levenshtein_distance(parts[0], parts[1])
    return result


def run():
    random_fuzzer = Fuzzer.RandomFuzzer(min_length=15, max_length=15, char_start=43, char_range=15) #  <-- here you add 43 because its + sign we split on it to have empty string
    return random_fuzzer.runs(runner=FunctionRunner(ld_wrapper), trials=10)
        


if __name__ == '__main__':

    for result in run():
        print(result)
    
    