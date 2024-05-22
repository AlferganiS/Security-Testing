"""
Use this file to implement your solution. You can use the `main.py` file to test your implementation.
"""
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from helpers import *
from fuzzingbook.Grammars import nonterminals


def instantiate_with_nonterminals(constraint_pattern: str, nonterminals: list[str]) -> set[str]:

    placeholders = constraint_pattern.count("{}")
    combinations = generate_combinations(nonterminals, placeholders)
    ret = set(constraint_pattern.format(*combination) for combination in combinations)
    return ret

def instantiate_with_subtrees(abstract_constraint: str, nts_to_subtrees: dict) -> set[str]:

    all_comb_constraint = set()
    
    def generate_strings_recursive(current_str):
        nonterminal_index = current_str.find('<')
        if nonterminal_index == -1:
            # No more nonterminals found, add the current string to the set
            all_comb_constraint.add(current_str)
        else:
            # Find the end of the nonterminal
            end_index = current_str.find('>', nonterminal_index)
            nonterminal = current_str[nonterminal_index:end_index + 1]
            if nonterminal in nts_to_subtrees:
                # Replace the nonterminal with each possible value from the dictionary
                for value in nts_to_subtrees[nonterminal]:
                    string_v = tree_to_string(value)
                    new_str = current_str[:nonterminal_index] + string_v + current_str[end_index + 1:]
                    # Recursively generate strings with the replaced nonterminal
                    generate_strings_recursive(new_str)

    generate_strings_recursive(abstract_constraint)
    return all_comb_constraint
    

def learn(constraint_patterns: list[str], derivation_trees: list) -> set[str]:

    common_nonterminals = find_common_nonterminals(derivation_trees)
    abstract_constraints = set()

    for pattern in constraint_patterns:
        instantiated_constraints = instantiate_with_nonterminals(pattern, common_nonterminals)
        for constraint in instantiated_constraints:
            all_valid = True
            for tree in derivation_trees:
                if not check({constraint}, tree):
                    all_valid = False
                    break
            if all_valid:
                abstract_constraints.add(constraint)
    

    return abstract_constraints


def check(abstract_constraints: set[str], derivation_tree) -> bool:

    all_trees = get_all_subtrees(derivation_tree)
    non_t = list()
    objs = set()
    result = True

    for ab_constraint in abstract_constraints:
        non_t.append(nonterminals(ab_constraint))
        objs.update(instantiate_with_subtrees(ab_constraint, all_trees))
    
    for obj in objs:
        try:
            result = eval(obj)
        except:
            return False
        if result == False:
            return result
        
    return result


    
    

def generate(abstract_constraints: set[str], grammar: dict, produce_valid_sample: True) -> str:

    fuzzer = GrammarFuzzer(grammar)
    while True:
        sample = fuzzer.fuzz()
        derivation_tree = next(EarleyParser(grammar).parse(sample))
        satisfies_constraints = check(abstract_constraints, derivation_tree)
        if satisfies_constraints == produce_valid_sample:
            return sample
        

"""
help functions
"""
def generate_combinations(nonterminals: list[str], placeholders: int):

    if placeholders == 0:
        yield ()
    else:
        for nonterminal in nonterminals:
            if is_nt(nonterminal):
                for combination in generate_combinations(nonterminals, placeholders - 1):
                    yield (nonterminal,) + combination

def find_common_nonterminals(derivation_trees: list) -> list[str]:

    common_nts = set(get_all_subtrees(derivation_trees[0]).keys())
    for tree in derivation_trees[1:]:
        nts = set(get_all_subtrees(tree).keys())
        common_nts.intersection_update(nts)
    return list(common_nts)

