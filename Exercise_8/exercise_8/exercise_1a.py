from fuzzingbook.Fuzzer import RandomFuzzer
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from fuzzingbook.MutationFuzzer import MutationFuzzer
from fuzzingbook.GreyboxFuzzer import GreyboxFuzzer, PowerSchedule, Mutator
from fuzzingbook.GreyboxGrammarFuzzer import LangFuzzer, GreyboxGrammarFuzzer, FragmentMutator, AFLSmartSchedule, RegionMutator
from fuzzingbook.Parser import EarleyParser

def get_random_fuzzer() -> RandomFuzzer:
    ran = RandomFuzzer()
    return ran


def get_grammar_fuzzer(grammar) -> GrammarFuzzer:
    gram = GrammarFuzzer(grammar)
    return gram


def get_mutation_fuzzer(seeds) -> MutationFuzzer:
    mut = MutationFuzzer(seed=seeds)
    return mut


def get_greybox_fuzzer(seeds) -> GreyboxFuzzer:
    mut = Mutator()
    sched = PowerSchedule()
    grey = GreyboxFuzzer(seeds=seeds, mutator=mut, schedule=sched)
    return grey


def get_lang_fuzzer(seeds, grammar) -> LangFuzzer:
    par = EarleyParser(grammar)
    frag_mut = FragmentMutator(par)
    sched = PowerSchedule()
    lang = LangFuzzer(seeds, frag_mut, sched)
    return lang
    


def get_greybox_grammar_fuzzer(seeds, grammar) -> GreyboxGrammarFuzzer:
    mut = Mutator()
    par = EarleyParser(grammar)
    reg_mut = RegionMutator(par)
    afl_sched = AFLSmartSchedule(par)
    grey_gram = GreyboxGrammarFuzzer(seeds, mut, reg_mut, afl_sched)
    return grey_gram

