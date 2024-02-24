# O'Shea ENPM661 Project 1: BFS 8 Puzzle Solver
Provides a class for using breadth first search to solve the 8 puzzle problem for a given start and goal state

# Dependencies
- numpy
- copy
- pygame
- time

# Instructions
- The proj1_ryan_oshea.py file can be run as is to solve a sample 8 puzzle configuration with the standard goal
- To change the start and goal state, change goal_state and puzzle variables in the main function
- This will produce the nodePath.txt, Nodes.txt, and NodesInfo.txt files that show the solved path, nodes visited, and all node info
- The Animate.py script can then be run to show an animation of the puzzle being solved using the found path
- There are unsolvable configurations for the 8 puzzle problem so if the code is given one it will simply run until it has checked all possible moves before printing out that the puzzle is unsolvable
- Two example solvable puzzles have been provided in the main function under the variables puzzle and challenging_puzzle. Challenging puzzle took my computer ~20 seconds to solve and went through 16992 puzzle iterations before finding the goal
- To solve the challenging puzzle just pass challenging_puzzle into the solver.solvePuzzle() call on line 302 instead of puzzle
- Example outputs for each of the text files have been included