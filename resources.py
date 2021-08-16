# -- resources.py --
# Provides resources for main.py, including piece coordinate data and adjacted coordinates

# Relative coordinates for each of the 19 pieces
def ids(piece_id=0):
    pieceCoords = {
        1: [[0, 0], [0, 1], [1, 0], [1, 1]],
        2: [[0, 0], [1, 0], [2, 0], [3, 0]],
        3: [[0, 0], [0, 1], [0, 2], [0, 3]],
        4: [[0, 0], [1, 0], [2, 0], [2, 1]],
        5: [[0, 0], [1, -2], [1, -1], [1, 0]],
        6: [[0, 0], [0, 1], [1, 1], [2, 1]],
        7: [[0, 0], [0, 1], [0, 2], [1, 0]],
        8: [[0, 0], [1, 0], [2, -1], [2, 0]],
        9: [[0, 0], [0, 1], [0, 2], [1, 2]],
        10: [[0, 0], [0, 1], [1, 0], [2, 0]],
        11: [[0, 0], [1, 0], [1, 1], [1, 2]],
        12: [[0, 0], [1, 0], [1, 1], [2, 0]],
        13: [[0, 0], [1, -1], [1, 0], [1, 1]],
        14: [[0, 0], [1, -1], [1, 0], [2, 0]],
        15: [[0, 0], [0, 1], [0, 2], [1, 1]],
        16: [[0, 0], [0, 1], [1, -1], [1, 0]],
        17: [[0, 0], [1, 0], [1, 1], [2, 1]],
        18: [[0, 0], [0, 1], [1, 1], [1, 2]],
        19: [[0, 0], [1, -1], [1, 0], [2, -1]]
    }

    if piece_id == 0:
        return pieceCoords
    return pieceCoords[piece_id]


# Node class used for binary tree, capable of nesting children
class Node:
  def __init__(self, value, children=None):
    self.value = value
    self.children = children

# Binary tree containing coordinates of all 19 pieces
tree = Node([0,0], [
    Node([1,0], [
        Node([0,1], [
            Node([1,1], [Node(1)]),
            Node([2,0], [Node(10)]),
            Node([1,-1], [Node(16)]),
            Node([0,2], [Node(7)])
        ]),
        Node([1,1], [
            Node([2,0], [Node(12)]),
            Node([1,-1], [Node(13)]),
            Node([2,1], [Node(17)]),
            Node([1,2], [Node(11)])
        ]),
        Node([2,0], [
            Node([1,-1], [Node(14)]),
            Node([2,1], [Node(4)]),
            Node([2,-1], [Node(8)]),
            Node([3,0], [Node(2)])
        ]),
        Node([1,-1], [
            Node([0,1], [Node(16)]),
            Node([2,-1], [Node(19)]),
            Node([1,-2], [Node(5)])
        ])
    ]),
    Node([0,1], [
        Node([1,1], [
            Node([2,1], [Node(6)]),
            Node([1,2], [Node(18)])
        ]),
        Node([0,2], [
            Node([1,1], [Node(15)]),
            Node([1,2], [Node(9)]),
            Node([0,3], [Node(3)])
        ])
    ])
])

# Coordinates for adjacent tiles (left, right, up, down)
lrud = [[0, -1], [0, 1], [0, -1], [0, 1]]