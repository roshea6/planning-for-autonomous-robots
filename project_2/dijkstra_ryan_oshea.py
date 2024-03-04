import cv2
import numpy as np

class dijkstraMapSolver():
    def __init__(self):
        # Define the map colors
        self.map_colors = {"obstacle": (0, 0, 255),
                           "clearance": (0, 255, 0),
                           "unexplored": (0, 0, 0),
                           "explored": (255, 0, 0),
                           "path": (255, 255, 255)}
        
        # Clearance in milimeters
        self.clearance = 5
        
        self.world_map = self.makeMap()
    
    # Makes the map image based on the parameters defined in the assigment
    def makeMap(self):
        # Make an all black map to start
        blank_map = np.zeros((500, 1200, 3), np.int8)
        
        # Draw the clearance first because the obstacles will be contained within them
        # Rectangles
        # Rectangle 1
        # Define the top left and bottom right of the normal rectangle 
        top_left = (100, 0)
        bottom_right = (175, 400)
        
        # First draw the clearance rectangle
        obstacle_map = cv2.rectangle(blank_map, 
                                     (top_left[0]-self.clearance, top_left[1]), 
                                     (bottom_right[0] + self.clearance, bottom_right[1] + self.clearance),
                                      thickness=-1, 
                                      color=self.map_colors["clearance"])
        
        # Draw the actual obstacle
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (top_left[0], top_left[1]), 
                                     (bottom_right[0], bottom_right[1]),
                                      thickness=-1, 
                                      color=self.map_colors["obstacle"])
        
        # Rectangle 2
        top_left = (275, 100)
        bottom_right = (350, 500)
        
        # First draw the clearance rectangle
        obstacle_map = cv2.rectangle(blank_map, 
                                     (top_left[0]-self.clearance, top_left[1] - self.clearance), 
                                     (bottom_right[0] + self.clearance, bottom_right[1]),
                                      thickness=-1, 
                                      color=self.map_colors["clearance"])
        
        # Draw the actual obstacle
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (top_left[0], top_left[1]), 
                                     (bottom_right[0], bottom_right[1]),
                                      thickness=-1, 
                                      color=self.map_colors["obstacle"])
        
        cv2.imshow("Map", obstacle_map)
        cv2.waitKey(0)
        
        # Hexagon
        
        # Backwards C shape
        
        # Outer edge?
        
    
    # Gets the start and end point from user input and stores them
    def getStartAndGoalInput(self):
        pass
    
    # Finds the shortest path from the start to end goal using Dijkstra's algorithm
    def findPath(self):
        pass
    
if __name__ == '__main__':
    solver = dijkstraMapSolver()
    
    # solver.makeMap()