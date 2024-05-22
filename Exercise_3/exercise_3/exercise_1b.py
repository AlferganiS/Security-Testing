"""
Use this file to implement your solution for exercise 3-1 b.
"""

from exercise_1a import *
import random
import time
random.seed(time.time())  # make random random again

def replace_subtree(tree, old_subtree, new_subtree):

        """
            This function replaces a specific subtree in the tree with a new subtree.

            Parameters:
                tree (tuple): The derivation tree.
                old_subtree (tuple): The subtree to be replaced.
                new_subtree (tuple): The new subtree to replace with.

            Returns:
                tuple: The modified derivation tree.
            """
       
        if tree[1]:
            if tree == old_subtree:
                return new_subtree
            else:
                new_children = [replace_subtree(child, old_subtree, new_subtree) for child in tree[1]]
                return (tree[0], new_children)
        else:
             return tree
            

def replace_random_subtree(tree, symbol, subtrees):

    """
    This function replaces a random subtree in the tree derived from the nonterminal symbol
    with a random subtree from the list of possible subtrees.

    Parameters:
        tree (tuple): The derivation tree.
        symbol (str): The nonterminal symbol to search for.
        subtrees (list): List of possible subtrees to replace with.

    Returns:
        tuple: The modified derivation tree.
    """
    
    # Find all subtrees in the tree derived from the specified symbol
    possible_subtrees = find_subtrees(tree, symbol)

    # Check if there are any subtrees to replace
    if possible_subtrees:
        # Randomly select a subtree from the list of possible subtrees
        replacement_subtree = random.choice(subtrees)
        #print('this is symbol -->  ', symbol)
        # Randomly select a subtree in the tree to replace with the new subtree
        index_to_replace = random.randint(0, len(possible_subtrees) - 1)

        # Replace the selected subtree with the new subtree
        modified_tree = replace_subtree(tree, possible_subtrees[index_to_replace], replacement_subtree)

        return modified_tree
    else:
        # If no matching subtrees found, return the original tree
        return tree

# Example usage

symbol = '<digit>'
possible_subtrees = [('<digit>', [('1', None)]), ('<digit>', [('2', None)])]

modified_tree2 = replace_random_subtree(expr_tree_2, symbol, possible_subtrees)
modified_tree1 = replace_random_subtree(expr_tree_1, symbol, possible_subtrees)
print(modified_tree1)
print(modified_tree2)

