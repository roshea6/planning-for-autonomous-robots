import numpy as np

class eightPuzzleSolver():
    def __init__(self):
        node_state_i = [[],
                        [],
                        []]
        
        goal_state = [[1, 2, 3],
                        [4, 5, 6],
                        [7, 8, 0]]
        
        visited_configs = []
        
        node_index_i = 0
        
        parent_node_index_i = 0
        
    # Gets the current location of the blank space as an (i, j) pair
    def getCurrentNodeState(self):
        pass
    
    # Determien the valid actions that can be taken then executes them
    def performValidMoves(self):
        pass
    
    # Moves blank space left
    def ActionMoveLeft(self):
        pass
    
    # Moves blank space right
    def ActionMoveRight(self):
        pass
    
    # Moves blank space up
    def ActionMoveUp(self):
        pass
    
    # Moves blank space down
    def ActionMoveDown(self):
        pass
    
    # Backtraces the state path once a path to the goal is found
    def generatePath(self):
        self
    
    # Writes the finals nodes visited, node info, and path taken to files
    def writeFiles(self):
        pass
    
    # Main driver function for solving the puzzle for a given configuration
    def solvePuzzle(self, puzzle):
        print(puzzle)
    
if __name__ == "__main__":
    solver = eightPuzzleSolver()
    
    puzzle = [[1, 4, 6],
              [2, 0, 7],
              [5, 3, 8]]
    
    solver.solvePuzzle(puzzle)