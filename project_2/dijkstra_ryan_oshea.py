import cv2
import numpy as np
import copy
from queue import PriorityQueue
import math

class dijkstraMapSolver():
    def __init__(self, record_video=False):
        # Define the map colors
        self.map_colors = {"obstacle": [0, 0, 255],
                           "clearance": [0, 255, 0],
                           "unexplored": [0, 0, 0],
                           "explored": [255, 0, 0],
                           "path": [255, 255, 255],
                           "start": [0, 255, 255],
                           "goal": [255, 0, 255]}
        
        self.map_dim = (500, 1200)
        
        # Clearance in milimeters
        self.clearance = 5
        
        # TODO: Move these to user input
        self.start_node = (10, 10)
        
        
        self.goal_node = (480, 60)
        
        
        
        self.action_set = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,1), (1,-1), (-1,-1)]
        
        self.node_index = 0
        
        node = (0, self.node_index, self.start_node, self.start_node)
        
        self.open_list = PriorityQueue()
        
        # Nodes that we've checked in general
        # Will be used to easily reference nodes by their pixel location to keep track of lowest cost for each node
        self.checked_nodes = {str(self.start_node): node}
        self.checked_pixels = set()
        
        # Keep track of the closes nodes with their ids as their dictionary keys
        self.closed_list = {}
        
        # Quickly checkable pixel pairs to avoid double searching
        self.closed_pixels = set()
        
        self.open_list.put(node)
        self.node_index += 1
        
        self.world_map = self.makeMap()
        
        # Make a map that will be drawn on from the world map
        self.draw_map = copy.copy(self.world_map)
        
        # Draw a square for the start and end nodes
        self.draw_map = cv2.rectangle(self.draw_map, 
                                      (self.start_node[1], self.start_node[0]), 
                                      (self.start_node[1] + 3, self.start_node[0] + 3),
                                      color=self.map_colors["start"],
                                      thickness=-1)
        
        self.draw_map = cv2.rectangle(self.draw_map, 
                                      (self.goal_node[1], self.goal_node[0]), 
                                      (self.goal_node[1] + 3, self.goal_node[0] + 3),
                                      color=self.map_colors["goal"],
                                      thickness=-1)
        
        # Add the starting node to the draw map
        self.draw_map[self.start_node[0], self.start_node[1]] = self.map_colors["explored"]
        
        self.record = record_video
        
        if self.record:
            self.video_rec = cv2.VideoWriter('output.mp4', -1, 600.0, (self.map_dim[1], self.map_dim[0]))
            
            self.video_rec.write(self.draw_map)
            
        self.path_pixels = []
    
    # Makes the map image based on the parameters defined in the assigment
    def makeMap(self):
        # Make an all black map to start
        blank_map = np.zeros((self.map_dim[0], self.map_dim[1], 3), np.uint8)
        
        # Border edges
        # Left wall
        obstacle_map = cv2.rectangle(blank_map, 
                                     (0, 0), 
                                     (self.clearance, self.map_dim[1] - self.clearance),
                                      thickness=-1, 
                                      color=self.map_colors["clearance"])
        
        # Top wall
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (0, 0), 
                                     (self.map_dim[1], self.clearance),
                                      thickness=-1, 
                                      color=self.map_colors["clearance"])
        
        # Right wall
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (self.map_dim[1] - self.clearance, 0), 
                                     (self.map_dim[1], self.map_dim[0]),
                                      thickness=-1, 
                                      color=self.map_colors["clearance"])
        
        # Bottom wall
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (0, self.map_dim[0] - self.clearance), 
                                     (self.map_dim[1], self.map_dim[0]),
                                      thickness=-1, 
                                      color=self.map_colors["clearance"])
        
        # Draw the clearance first because the obstacles will be contained within them
        # Rectangles
        # Rectangle 1
        # Define the top left and bottom right of the normal rectangle 
        top_left = (100, 0)
        bottom_right = (175, 400)
        
        # First draw the clearance rectangle
        obstacle_map = cv2.rectangle(obstacle_map, 
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
        obstacle_map = cv2.rectangle(obstacle_map, 
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
        
        # Hexagon
        hex_origin = (650, 250)
        hex_x_len = 130
        hex_y_len = 150
        
        # Clearance
        # Define the hexagon vertices starting with the top center and working clockwise
        # TODO: Looks like this doesn't make the full 5 pixel clerance on the sides
        # Might need to define manual lines for this part
        hex_pts = np.array([[hex_origin[0], hex_origin[1] - hex_y_len - self.clearance], # top center
                   [hex_origin[0] + hex_x_len + self.clearance, hex_origin[1] - hex_y_len/2], # top right
                   [hex_origin[0] + hex_x_len + self.clearance, hex_origin[1] + hex_y_len/2], # bottom right
                   [hex_origin[0], hex_origin[1] + hex_y_len + self.clearance], # bottom center
                   [hex_origin[0] - hex_x_len - self.clearance, hex_origin[1] + hex_y_len/2], # bottom left
                   [hex_origin[0] - hex_x_len - self.clearance, hex_origin[1] - hex_y_len/2]], np.int32) # top left
        
        # Draw the hexagon
        obstacle_map = cv2.fillPoly(obstacle_map, [hex_pts], color=self.map_colors["clearance"])
        
        # Obstacle hexagon
        # Define the hexagon vertices starting with the top center and working clockwise
        hex_pts = np.array([[hex_origin[0], hex_origin[1] - hex_y_len], # top center
                   [hex_origin[0] + hex_x_len, hex_origin[1] - hex_y_len/2], # top right
                   [hex_origin[0] + hex_x_len, hex_origin[1] + hex_y_len/2], # bottom right
                   [hex_origin[0], hex_origin[1] + hex_y_len], # bottom center
                   [hex_origin[0] - hex_x_len, hex_origin[1] + hex_y_len/2], # bottom left
                   [hex_origin[0] - hex_x_len, hex_origin[1] - hex_y_len/2]], np.int32) # top left
        
        # Draw the hexagon
        obstacle_map = cv2.fillPoly(obstacle_map, [hex_pts], color=self.map_colors["obstacle"])
        
        # Backwards C shape
        # Draw the 3 clearance sub rectangles that make up the shape first
        # Top rectangle
        c_top_top_left = (900, 50)
        c_top_bottom_right = (1020, 125)
        
        # Top clearance rectangle
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (c_top_top_left[0]-self.clearance, c_top_top_left[1] - self.clearance), 
                                     (c_top_bottom_right[0] + self.clearance, c_top_bottom_right[1] + self.clearance),
                                      thickness=-1, 
                                      color=self.map_colors["clearance"])
        
        # Middle clearance rectangle
        c_middle_top_left = (1020, 50)
        c_middle_bottom_right = (1100, 450)
        
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (c_middle_top_left[0]-self.clearance, c_middle_top_left[1] - self.clearance), 
                                     (c_middle_bottom_right[0] + self.clearance, c_middle_bottom_right[1] + self.clearance),
                                      thickness=-1, 
                                      color=self.map_colors["clearance"])
        
        c_bottom_top_left = (900, 375)
        c_bottom_bottom_right = (1020, 450)
        
        # Bottom clearance rectangle
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (c_bottom_top_left[0]-self.clearance, c_bottom_top_left[1] - self.clearance), 
                                     (c_bottom_bottom_right[0] + self.clearance, c_bottom_bottom_right[1] + self.clearance),
                                      thickness=-1, 
                                      color=self.map_colors["clearance"])
        
        # Obstacle rectangles
        # Top clearance rectangle
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (c_top_top_left[0], c_top_top_left[1]), 
                                     (c_top_bottom_right[0], c_top_bottom_right[1]),
                                      thickness=-1, 
                                      color=self.map_colors["obstacle"])
        
        # Middle clearance rectangle
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (c_middle_top_left[0], c_middle_top_left[1]), 
                                     (c_middle_bottom_right[0], c_middle_bottom_right[1]),
                                      thickness=-1, 
                                      color=self.map_colors["obstacle"])
        
        # Bottom clearance rectangle
        obstacle_map = cv2.rectangle(obstacle_map, 
                                     (c_bottom_top_left[0], c_bottom_top_left[1]), 
                                     (c_bottom_bottom_right[0], c_bottom_bottom_right[1]),
                                      thickness=-1, 
                                      color=self.map_colors["obstacle"])
        
        
        # cv2.imshow("Map", obstacle_map)
        # cv2.waitKey(0)
        
        return obstacle_map
    
    # Gets the start and end point from user input and stores them
    def getStartAndGoalInput(self):
        pass
    
    def applyMoves(self, start_pixel, cost):
        for move in self.action_set:
            new_loc = (start_pixel[0] + move[0], start_pixel[1] + move[1])
            
            # Check if we're in an obstacle or clearance pixel
            if list(self.world_map[new_loc[0], new_loc[1]]) == self.map_colors["obstacle"] or list(self.world_map[new_loc[0], new_loc[1]]) == self.map_colors["clearance"]:
                # If we are don't add it to the list of new nodes
                # print("HIT OBSTACLE")
                
                continue
            
            # Calculate cost to get the new pixel from the parent pixel
            cost_to_go = cost + math.sqrt(move[0]**2 + move[1]**2)
            
            
            # Check if the pixel is in the list of working pixels and grab it's current cost if it is
            if str(new_loc) in self.checked_pixels:
                existing_node = self.checked_nodes[str(new_loc)]
                
                existing_cost = existing_node[0]
                
                # If the new found cost is less than the existing cost then update the node with the new cost and 
                # parent pixel that gives it the lower cost
                if cost_to_go < existing_cost:
                    updated_node = (cost_to_go, existing_node[1], start_pixel, existing_node[3])
                    
                    # Update the checked nodes dict with the updated now
                    self.checked_nodes[str(new_loc)] = updated_node
                    
                    # Add the node with the updated cost to the priority queue
                    self.open_list.put(updated_node)
                    
                    # TODO: Do we need to remove the old node from the priority queue?
                 
            # Otherwise add the new pixel to the checked nodes and pixel locations we're tracking   
            else:
                new_node = (cost_to_go, self.node_index, start_pixel, new_loc)
                self.node_index += 1
                
                # Update the drawing map with the latest explored node
                self.draw_map[new_loc[0], new_loc[1]] = self.map_colors["explored"]  
                
                # Write the latest frame to the video
                if self.record:
                    self.video_rec.write(self.draw_map)  
                
                # Update the checked nodes dict with the updated now
                self.checked_nodes[str(new_loc)] = new_node
                self.checked_pixels.add(str(new_loc))
                
                # Add the new node to the priority queue
                self.open_list.put(new_node)
        
    # backtrack from the goal node to trace a path of pixels 
    def backtrack(self, goal_node):
        pix_loc = goal_node[3]
        
        self.path_pixels.append(pix_loc)
        
        # Loop through the parent nodes until we get back to the start location
        while not pix_loc == self.start_node:
            # Draw the path pixel
            self.draw_map[pix_loc[0], pix_loc[1]] = self.map_colors["path"]
            
            # Grab the previous node from it's pixel
            prev_node = self.checked_nodes[str(pix_loc)]
            
            # Grab the next pixel from the current node's parent pixel
            pix_loc = prev_node[2]
            
            # print(pix_loc)
            
            # Save the pixel so we can trace it later
            self.path_pixels.append(pix_loc)
            
        # Draw the start and goal nodes again
        self.draw_map = cv2.rectangle(self.draw_map, 
                                    (self.start_node[1], self.start_node[0]), 
                                    (self.start_node[1] + 3, self.start_node[0] + 3),
                                    color=self.map_colors["start"],
                                    thickness=-1)
        
        self.draw_map = cv2.rectangle(self.draw_map, 
                                    (self.goal_node[1], self.goal_node[0]), 
                                    (self.goal_node[1] + 3, self.goal_node[0] + 3),
                                    color=self.map_colors["goal"],
                                    thickness=-1)
        
        # Write the final frame to the video
        if self.record:
            self.video_rec.write(self.draw_map) 
            
            
    
    # Finds the shortest path from the start to end goal using Dijkstra's algorithm
    def findPath(self):
        # Loop until we've removed all nodes from the open list
        while not self.open_list.empty():
            # Pop off the highest priority node
            priority_node = self.open_list.get()
            
            print(priority_node)
            
            # First check if this is the goal node
            if priority_node[3] == self.goal_node:
                print("Goal found")
                self.backtrack(priority_node)
                
                break
            
            # TODO: Check to make sure an updated lower cost for the nodes wasn't already found
            
            cost = priority_node[0]
            
            pixel_loc = priority_node[3]
            
            self.applyMoves(pixel_loc, cost)
            
            # Move the current node to the closed nodes list
            self.closed_list[str(pixel_loc)] = priority_node
            
        cv2.imshow("Exploration map", self.draw_map)
        cv2.waitKey(0)
        
        if self.record:
            self.video_rec.release()
    
if __name__ == '__main__':
    solver = dijkstraMapSolver(record_video=False)
    
    solver.findPath()