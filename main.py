# -- main.py --
# Optimises the placement of a selection of tetromino (tetris) pieces to fit a target area

import resources
import numpy as np
from collections import defaultdict
from copy import deepcopy

pieceCoords = resources.ids()
pieceTree = resources.tree
lrud = resources.lrud


def place_piece(weighted_dict, P, x, y, width, height, piecesPlaced, solution, pas):
  """
  Places a tetromino piece on the board.

  Parameters:
  weighted_dict (dict): Dictionary form of the weighted board
  P (dict): Set of available tetromino pieces
  x (int): x position of the current target tile
  y (int): y-position of the current target tile
  width (int): width of the board
  height (int): height of the board
  piecesPlaced (int): the number of pieces currently placed
  solution (arr): current solution 
  pas (int): board pass (the nth time that the board has been fully scanned for placing tetrominos)

  Returns:
  int: The number of pieces placed
  """

  piece = best_piece(weighted_dict, P, x, y, pieceTree, pas, width, height)[0]
  if piece:
    piecesPlaced += 1
    P[piece] -= 1
    for block in range(4):
      dy, dx = y + pieceCoords[piece][block][0], x + pieceCoords[piece][block][1]
      solution[dy][dx] = (piece, piecesPlaced)
      weighted_dict[(dy, dx)] = -1
      if pas == 1: updateWeights(weighted_dict, pieceCoords[piece], x, y)

  return piecesPlaced


def best_piece(D, P, x, y, node, pas, width, height, weightCount=0, candidate=[0,0]):
  """
  Calculates the best piece to be placed on coordinates x y subject to edge weights.
  Uses recursion to search through a binary tree containing all piece information.
  Using recursion neatly encapsulates logic and efficiently prunes any sub-optimal pieces.

  Parameters:
  D (dict): Dictionary form of solution board
  P (dict): Set of available tetromino pieces
  x (int): x coordinate of tile to place
  y (int): y coordinate of tile to place  
  node (dict): current node in binary tree
  pas (int): board pass (the nth time that the board has been fully scanned for placing tetrominos)
  width (int): width of board
  height (int): height of board
  weightCount (int): current accumilated weight of piece
  candidate (arr): current best candidate piece with the highest weight
  """

  if not node.children:  # Base case
    if P[node.value] == 0: return [0, 0]  # If the piece has run out
    elif pas == 2 and weightCount < 3: return [0, 0]  # 2nd pass
    else: return [node.value, weightCount]  # return candidate [piece_id, weight]

  dy, dx = y + node.value[0], x + node.value[1] # Calculate current tile in piece
  if D[(dy, dx)] < 2-pas: return [0, 0]  # If coordinate is invalid or not a target block
  weightCount += D[(dy, dx)] if pas == 1 else min(1, D[(dy, dx)]) # Add weight

  for i in range(len(node.children)): # For all other piece descendants of node
    new_candidate = best_piece(D, P, x, y, node.children[i], pas, width, height, weightCount, candidate) # Recursively find best piece
    if width*height < 2000: # If board is sufficiently large, switch criteria for optimum candidate
      if candidate[1] <= new_candidate[1]: candidate = new_candidate
    else:
      if candidate[1] < new_candidate[1]: candidate = new_candidate

  return candidate


def weightBoard(T):
  """
  Calculates the weight for each target tile in the board.
  The weight is based on how many adjacent edges a target tile has.
  This weighting is used because it favours tetromino placements which tightly fit against the edge of a target, leaving minimal 'rogue' inaccessible tiles. 

  Parameters:
  T (arr): Target board

  Returns:
  arr: Weighted target board
  """

  W = np.array(T, copy=True) # Copy the board
  Tp = 1 - np.pad(T, pad_width=1, mode='constant', constant_values=0) # Create an array of edges
  W = W + Tp[1:-1, 0:-2] + Tp[0:-2, 1:-1] + Tp[1:-1, 2:] + Tp[2:, 1:-1] # Add up weights to each tile
  np.place(W, T == 0, 0) # Replace the weight of all none-target tiles with a 0

  return W


def updateWeights(dict, piece, x, y):
  """
  Updates the weighted board once a new piece has been placed.
  Once a piece is placed, it's tiles count as non-target tiles.
  This is so that other pieces can't be placed on the these tiles.

  Parameters:
  dict (arr): Current solution board
  piece (dict): Piece that has just been placed
  x (int): x coordinate of piece
  y (int): y coordinate of piece
  """

  for i in range(len(piece)): # For each tile in piece
    dy, dx = y + piece[i][0], x + piece[i][1] # calculate coordinates of tile
    for block in range(4): # For each of the adjacent tiles
      if not dict[(dy + lrud[block][0], dx + lrud[block][1])] in [-1, 0]: # If tile is a target tile
        dict[(dy + lrud[block][0], dx + lrud[block][1])] += 1 # Add a weight


def dictBoard(array):
  """
  Creates a dictionary form of the board.
  This allows for fast access of each tile (O(1)), and instant checks for invalid tiles.

  Parameters:
  array (arr): Array form of the weighted board

  Returns:
  dict: dictionary form of the board
  """

  dd = defaultdict(lambda: -1) # Creates a dictionary whose default value is -1 if a non-existent key is accessed
  for j in range(len(array)): # For each row
    for i in range(len(array[0])): # For each column
      dd[(j, i)] = array[j, i] # Create a key using coordinates xy, whose value is the weight at tile xy
  return dd


def calculateAccuracy(originalArray, solutionArray, width, height, totalPieces):
  """
  Calculates the total accuracy of the optimisers solution.

  Parameters:
  originalArray (arr): Target board
  solutionArray (arr): Board with the calculated solution
  width (int): width of board
  height (int): height of board
  totalPieces (int): total number of pieces provided

  Returns:
  float: accuracy of optimisers solution
  """

  mistakes = 0 # Initialise mistakes

  for j in range(height): # For each row
    for i in range(width): # For each column
      if originalArray[j][i] != min(1, solutionArray[j][i][0]): # If a mistake is made
        mistakes += 1

  accuracy = 100 * ( 1 - (mistakes / (totalPieces*4) ) ) # Calculate final accuracy

  return accuracy, solutionArray


def Tetris(target, pieces):
  """
  Root function which calculates the optimal placement of tetromino pieces on a board given a target area and set of pieces.
  A greedy algorithm is used to compute the optimal placement in linear time O(n).

  Parameters:
  target (arr): Target board
  pieces (dict): Set of pieces provided

  Returns:
  arr: optimisers solution
  """

  # Initialise variables
  height, width = len(target), len(target[0])
  accuracy, bestAccuracy = 0, 0
  bestSolution = [[(0, 0) for i in range(width)] for j in range(height)]

  for offset in range(width*height if width*height < 800 else 1): # Find the best solution from starting on each tile on the
  #board if there are less than 800 tiles, otherwise only consider starting at tile 1

    solution = [[(0, 0) for i in range(width)] for j in range(height)] # Initialise solution
    totalPieces, piecesPlaced = 0, 0 # Initialise pieces
    T = deepcopy(np.array(target)) # Target board
    W = deepcopy(weightBoard(T)) # Weighted target board
    D = deepcopy(dictBoard(W)) # Dictionary form of W
    P = deepcopy(pieces) # Set of available pieces
    for i in P: totalPieces += P[i] # Calculate total pieces

    for i in range(width*height):  # first pass - pieces cannot be placed on a non-target tile
      i = (i + offset) % (width*height) # flattened index of current tile
      y, x = i // width, i % width # xy coordinates of current tile
      if not D[(y, x)] in [-1, 0]: piecesPlaced = place_piece(D, P, x, y, width, height, piecesPlaced, solution, 1)

    for i in range(width*height):  # 2nd pass - pieces can be placed on a non-target tile
      i = (i + offset) % (width * height) # flattened index of current tile
      y, x = i // width, i % width # xy coordinates of current tile
      if not D[(y, x)] in [-1,0]: piecesPlaced = place_piece(D, P, x, y, width, height, piecesPlaced, solution, 2)

    accuracy, solution = calculateAccuracy(target, solution, width, height, totalPieces) # Calculate accuracy
    if accuracy > bestAccuracy: bestAccuracy, bestSolution = accuracy, solution # Return the solution with the highest accuracy

  return bestSolution