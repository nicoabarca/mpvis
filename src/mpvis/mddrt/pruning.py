import pandas as pd

from mpvis.mddrt.tree_node import TreeNode


def prune_tree_to_depth(node: TreeNode, max_depth: int) -> None:
    """
    Prunes the tree to the specified maximum depth.

    Args:
        node (TreeNode): The root node of the tree to prune.
        max_depth (int): The maximum depth to retain in the tree.
    """
    if node.depth >= max_depth - 1:
        node.children = []
    else:
        for child in node.children:
            prune_tree_to_depth(child, max_depth)
