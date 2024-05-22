"""
Use this file to implement your solution for exercise 3-1 a.
"""

from trees import *


def find_subtrees(tree, symbol):
    """
    This function finds all subtrees derived from the given nonterminal symbol in the provided tree.

    Parameters:
        tree (tuple): The derivation tree.
        symbol (str): The nonterminal symbol to search for.

    Returns:
        list: A list containing all relevant subtrees.
    """
    
    # Initialize an empty list to store found subtrees
    subtrees = []

    # Recursive function to traverse the tree and find subtrees
    def traverse(node):
        nonlocal subtrees
        # Check if the current node is a tuple and the first element matches the symbol
        if isinstance(node, tuple) and node[0] == symbol:
            # Add the current subtree to the list
            subtrees.append(node)
        # Recursively traverse the children of the current node
        if node[1]:
            for child in node[1]:
                traverse(child)

    # Start the traversal from the root of the tree
    traverse(tree)

    return subtrees

# Test usage

result1 = find_subtrees(expr_tree_1, '<integer>')
result2 = find_subtrees(expr_tree_2, '<integer>')
print(result1)
print(result2)