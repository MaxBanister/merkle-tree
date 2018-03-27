from utils import *
import math
from node import Node
from merkle_tree import *


def merkle_proof(tx, merkle_tree):
    """Given a tx and a Merkle tree object, retrieve its list of tx's and
    parse through it to arrive at the minimum amount of information required
    to arrive at the correct block header. This does not include the tx
    itself.

    Return this data as a list; remember that order matters!
    """
    proof = []
    tx_index = merkle_tree.leaves.index(tx)
    lower = 0
    upper = len(merkle_tree.leaves)
    curr_node = merkle_tree._root
    while upper - lower > 1:
        median = (lower + upper) // 2
        if tx_index < median:
            proof.append(Node("r", curr_node._right.data if type(curr_node._right) != str else curr_node._right))
            curr_node = curr_node._left
            upper = median
        else:
            proof.append(Node("l", curr_node._left.data if type(curr_node._left) != str else curr_node._left))
            curr_node = curr_node._right
            lower = median
    return proof


def verify_proof(tx, merkle_proof):
    """Given a Merkle proof - constructed via `merkle_proof(...)` - verify
    that the correct block header can be retrieved by properly hashing the tx
    along with every other piece of data in the proof in the correct order
    """
    lst = [tx] + list(merkle_proof)[::-1]
    while len(lst) > 1:
        if lst[1].direction == 'r':
            lst.insert(0, hash_data(lst.pop(0) + lst.pop(0).tx))
        else:
            lst.insert(0, hash_data(lst.pop(1).tx + lst.pop(0)))
    return lst[0]
