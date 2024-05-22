"""
Use this file to implement your solution for exercise 3-2 a.
"""

from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.GrammarCoverageFuzzer import GrammarCoverageFuzzer
from re_coverage import get_coverage

from exercise_2 import RE_GRAMMAR
from exercise_2a import RE_GRAMMAR_EXPANDED

import random
import time

random.seed(time.time())

def run_experiment(fuzzer, grammar, num_trials=25):
    total_coverage = 0
    for trial in range(num_trials):
        generated_input = fuzzer(grammar)
        total_coverage += get_coverage(generated_input)
    return total_coverage / num_trials

# Run the experiment for GrammarFuzzer with RE_GRAMMAR
coverage_grammar_re = run_experiment(GrammarFuzzer, RE_GRAMMAR)

# Run the experiment for GrammarCoverageFuzzer with RE_GRAMMAR
coverage_cgrammar_re = run_experiment(GrammarCoverageFuzzer, RE_GRAMMAR)

# Run the experiment for GrammarCoverageFuzzer with RE_GRAMMAR_EXPANDED
coverage_grammar_rex = run_experiment(GrammarCoverageFuzzer, RE_GRAMMAR_EXPANDED)

print(f'GrammarFuzzer: {coverage_grammar_re}'.format(0)) # print the average code coverage for GrammarFuzzer + RE_GRAMMAR
print(f'GrammarCoverageFuzzer: {coverage_cgrammar_re}'.format(0)) # print the average code coverage for GrammarCoverageFuzzer + RE_GRAMMAR
print(f'GrammarCoverageFuzzer+: {coverage_grammar_rex}'.format(0)) # print the average code coverage for GrammarCoverageFuzzer + RE_GRAMMAR_EXPANDED
