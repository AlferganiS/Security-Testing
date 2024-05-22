"""
Use this file to implement your solution for exercise 4-1 a.
"""
from fuzzingbook.Grammars import opts, is_valid_grammar
from fuzzingbook.ProbabilisticGrammarFuzzer import ProbabilisticGrammarFuzzer, exp_probabilities, PROBABILISTIC_EXPR_GRAMMAR, is_valid_probabilistic_grammar
import random
import time
random.seed(time.time())  # make random random again

SNAKE_GRAMMAR = {
    '<start>': ['<snake>', ('', opts(prob=0))],
    '<snake>': ['<digit>', ('<snake><digit>', opts(prob=(1.0 / 7) * 6)), ('', opts(prob=0))],
    '<digit>': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
}

# assert is_valid_grammar(SNAKE_GRAMMAR, supported_opts={'prob'})
# assert is_valid_probabilistic_grammar(SNAKE_GRAMMAR)

# p = ProbabilisticGrammarFuzzer(SNAKE_GRAMMAR)
# print(p.fuzz())
# print(exp_probabilities(SNAKE_GRAMMAR["<snake>"]))
