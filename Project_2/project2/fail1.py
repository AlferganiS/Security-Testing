"""
Use this file to implement your solution. You can use the `main.py` file to test your implementation.
"""
from fuzzingbook.GrammarFuzzer import GrammarFuzzer
from helpers import *
import re

def instantiate_with_nonterminals(constraint_pattern: str, nonterminals: list[str]) -> set[str]:
    # print(constraint_pattern, ' -->  ', nonterminals)

    placeholders = constraint_pattern.count("{}")
    combinations = generate_combinations(nonterminals, placeholders)
    ret = set(constraint_pattern.format(*combination) for combination in combinations)
    print(' this is ret -->  ', ret)
    return ret

def instantiate_with_subtrees(abstract_constraint: str, nts_to_subtrees: dict) -> set[str]:
    # print(abstract_constraint, ' -->  ', nts_to_subtrees)
    # print(tree_to_string(nts_to_subtrees["<start>"][0]))
    all_constraints = set()
    # for key, value in nts_to_subtrees.items():
    #     for v in value:
    #         if key == '<json>':
    #             updated_constraint = abstract_constraint.replace(f"{key}", tree_to_string(v))
    #             print(abstract_constraint)
    #             print('this is key --> ', key, ' this is value --> ', tree_to_string(v))
    #             print(updated_constraint)
    #             all_constraints.add(updated_constraint)
            # else:
                # print('this is key --> ', key, ' this is value --> ', tree_to_string(v))
    pattern = r'<(.*?)>'
    non_terminals = re.findall(pattern, abstract_constraint)
    # print(all_constraints)
    # print('non --> ', non_terminals)

    def instantiate_nonterminal(constraint, nonterminal, subtrees):
        instantiated_constraints = set()
        for subtree in subtrees:
            subtree_str = tree_to_string(subtree)
            instantiated_constraint = constraint.replace(nonterminal, subtree_str)
            instantiated_constraints.add(instantiated_constraint)
        return instantiated_constraints

    def instantiate_constraints(constraint, nts_to_subtrees):
        if not constraint:
            return {""}

        first, *rest = constraint
        # print('this is constraint --> ', constraint)

        if not is_nt(first):
            return {first + rest[0]}

        nonterminal = first
        print('this is nonterminal --> ', nonterminal)
        rest_str = rest[0]
        if nonterminal in nts_to_subtrees:
            subtrees = nts_to_subtrees[nonterminal]
            instantiated_constraints = set()
            for subtree in subtrees:
                instantiated_subconstraints = instantiate_constraints(rest_str, nts_to_subtrees)
                for instantiated_subconstraint in instantiated_subconstraints:
                    instantiated_constraints |= instantiate_nonterminal(instantiated_subconstraint, nonterminal, [subtree])
            return instantiated_constraints
        else:
            return set()
    ret = instantiate_constraints(abstract_constraint, nts_to_subtrees)
    # print('this is ret -->  ', ret)
    return ret


def learn(constraint_patterns: list[str], derivation_trees: list) -> set[str]:
    # print(constraint_patterns, '  -->  ', derivation_trees )

    # Find the nonterminal symbols that occur in every derivation tree
    candidate_nts = find_common_nonterminals(derivation_trees)
    # print(candidate_nts)
    # for t in derivation_trees:
    #     print(t)
    # for con in constraint_patterns:
    #     print(con)

    # Instantiate the constraint patterns with the candidate nonterminals
    abstract_constraints = set()
    for pattern in constraint_patterns:
        abstract_constraints.update(instantiate_with_nonterminals(pattern, candidate_nts))
    
    # Check which abstract constraints hold for all trees in derivation_trees
    valid_constraints = set()
    # for constraint in abstract_constraints:
    #     print(constraint)

    for tree in derivation_trees:
        for constraint in abstract_constraints:
            # print(constraint, '  -->  ', tree)
            x = check_constraint(constraint, tree)
            if not x:
                break
        if x:
            valid_constraints.add(constraint)
        # if all(check_constraint(constraint, tree) for tree in derivation_trees):
        #     valid_constraints.add(constraint)

    return valid_constraints

def check(abstract_constraints: set[str], derivation_tree) -> bool:
    
    nts_to_subtrees = get_all_subtrees(derivation_tree)
    for abstract_constraint in abstract_constraints:
        concrete_constraints = instantiate_with_subtrees(abstract_constraint, nts_to_subtrees)
        # for concrete_constraint in concrete_constraints:
        #     print(concrete_constraint, "  -->  ", derivation_tree)
        if not any(eval(concrete_constraint) for concrete_constraint in concrete_constraints):
            return False
    return True

def generate(abstract_constraints: set[str], grammar: dict, produce_valid_sample: True) -> str:

    fuzzer = GrammarFuzzer(grammar)
    while True:
        sample = fuzzer.fuzz()
        derivation_tree = next(EarleyParser(grammar).parse(sample))
        satisfies_constraints = check(abstract_constraints, derivation_tree)
        if satisfies_constraints == produce_valid_sample:
            return sample


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

# def check_constraint(constraint: str, tree) -> bool:
#     nts_to_subtrees = get_all_subtrees(tree)
#     concrete_constraints = instantiate_with_subtrees(constraint, nts_to_subtrees)
#     ret = any(eval(concrete_constraint) for concrete_constraint in concrete_constraints)
#     return ret

def check_constraint(constraint: str, tree) -> bool:

    nts_to_subtrees = get_all_subtrees(tree)
    concrete_constraints = instantiate_with_subtrees(constraint, nts_to_subtrees)
    # for concrete_constraint in concrete_constraints:
    #     print(concrete_constraint)

    for concrete_constraint in concrete_constraints:
        try:
            if eval(concrete_constraint):
                return True
        except:
            return False
    return False
