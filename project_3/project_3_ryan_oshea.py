import cv2
import numpy as np
import copy
from queue import PriorityQueue
import math
import time

class AStarMapSolver():
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
        
        self.save_every_n_frames = 600
        
        # Clearance in milimeters
        while True:
            self.clearance = int(input("Enter the clearance value in mm (5-15 recommended): "))
            
            if self.clearance < 0 or self.clearance > 30:
                continue
            else:
                break

        self.dist_tolerance = 3
        self.angle_tolerance = 30
        
        
        self.action_set = [-60, -30, 0, 30, 60]
        
        
        self.world_map = self.makeMap()
        
        self.getStartAndGoalInput()
        
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
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.video_rec = cv2.VideoWriter('a_star_ryan_oshea_output.mp4', fourcc, 120.0, (self.map_dim[1], self.map_dim[0]))
            
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
        # Loop until a valid starting point is input
        while True:
            start_x = int(input("Enter start pixel x value: "))
            start_y = self.map_dim[0] - int(input("Enter start pixel y value: "))
            start_theta = int(input("Enter start theta value that is a multiple of 30: "))
            
            if start_x > self.map_dim[1] or start_x < 0 or start_y > self.map_dim[0] or start_y < 0:
                print("Please choose values inside the bounds of the image")
            elif list(self.world_map[start_y, start_x]) == self.map_colors["obstacle"] or list(self.world_map[start_y, start_x]) == self.map_colors["clearance"]:
                print("Start location entered collides with obstacle. Please enter a new value")
            elif not start_theta % 30 == 0:
                print("Start angle not a multiple of 30")
            else:
                break
            
        # Need to swap y and x because of the way numpy indexes things
        self.start_node = (start_y, start_x, start_theta)
                
        # Loop until a valid goal input is input
        while True:
            goal_x = int(input("Enter goal pixel x value: "))
            goal_y = self.map_dim[0] - int(input("Enter goal pixel y value: "))
            goal_theta = int(input("Enter start theta value that is a multiple of 30: "))
            
            if goal_x > self.map_dim[1] or goal_x < 0 or goal_y > self.map_dim[0] or goal_y < 0:
                print("Please choose values inside the bounds of the image")
            elif list(self.world_map[goal_y, goal_x]) == self.map_colors["obstacle"] or list(self.world_map[goal_y, goal_x]) == self.map_colors["clearance"]:
                print("Goal location entered collides with obstacle. Please enter a new value")
            elif not goal_theta % 30 == 0:
                print("Goal angle not a multiple of 30")
            else:
                break

        while True:
            self.step_size = int(input("Please enter a step size value between 1 and 10: "))

            if self.step_size < 1 or self.step_size > 10:
                print("Invalid step size")
            else:
                break

        # TODO: Add in input for the clearance and maybe robot size? The full clearance will just be the clerance + robot size if we need to add both
            
        self.goal_node = (goal_y, goal_x, goal_theta)
            

    def deg2rad(self, deg):
        return (math.pi/180) * deg
    
    def applyMoves(self, start_pixel, cost):
        for move in self.action_set:
            new_angle = start_pixel[2] + move
            # Scale the new angle to be between 0 and 360
            new_angle = new_angle % 360
            new_loc = (int(start_pixel[0] + self.step_size*math.cos(self.deg2rad(new_angle))), int(start_pixel[1] + self.step_size*math.sin(self.deg2rad(new_angle))), new_angle)

            if new_loc[0] >= self.map_dim[0] or new_loc[0] < 0:
                continue

            if new_loc[0] >= self.map_dim[1] or new_loc[1] < 0:
                continue
            
            # Check if we're in an obstacle or clearance pixel
            if list(self.world_map[new_loc[0], new_loc[1]]) == self.map_colors["obstacle"] or list(self.world_map[new_loc[0], new_loc[1]]) == self.map_colors["clearance"]:
                # If we are don't add it to the list of new nodes
                # print("HIT OBSTACLE")
                continue
            
            # Calculate cost to get to the new pixel from the parent pixel as the euclidian distance between the 2
            cost_to_go = cost + math.sqrt((start_pixel[0] - new_loc[0])**2 + (start_pixel[1] - new_loc[1])**2)

            # Calculate the cost to come as the euclidian distance between the ne config and the goal config
            # TODO: Do we need to calculate the rotation distance as well?
            cost_to_come = math.sqrt((self.goal_node[0] - new_loc[0])**2 + (self.goal_node[1] - new_loc[1])**2)

            total_cost = cost_to_go + cost_to_come
            
            
            # Check if the pixel is in the list of working pixels and grab it's current cost if it is
            if str(new_loc) in self.checked_pixels:
                existing_node = self.checked_nodes[str(new_loc)]
                
                existing_cost = existing_node[0]
                
                # If the new found cost is less than the existing cost then update the node with the new cost and 
                # parent pixel that gives it the lower cost
                if total_cost < existing_cost:
                    updated_node = (total_cost, existing_node[1], start_pixel, existing_node[3])
                    
                    # Update the checked nodes dict with the updated now
                    self.checked_nodes[str(new_loc)] = updated_node
                    
                    # Add the node with the updated cost to the priority queue
                    self.open_list.put(updated_node)
                    
                 
            # Otherwise add the new pixel to the checked nodes and pixel locations we're tracking   
            else:
                new_node = (total_cost, self.node_index, start_pixel, new_loc)
                self.node_index += 1
                
                # Update the drawing map with the latest explored node
                self.draw_map[new_loc[0], new_loc[1]] = self.map_colors["explored"]  
                
                # Write the latest frame to the video
                # TODO: Should probably make this into a save_every_n_frames param
                if self.record and self.node_index % self.save_every_n_frames == 0:
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
            
        # Animate the path
        self.path_pixels.reverse()
        
        # TODO: Might want to change these from rectangles to lines with 3 thickness to connect path with large step sizes
        for pixel in self.path_pixels:
            self.draw_map = cv2.rectangle(self.draw_map, 
                                    (pixel[1], pixel[0]), 
                                    (pixel[1] + 3, pixel[0] + 3),
                                    color=self.map_colors["start"],
                                    thickness=-1)
            if self.record:
                self.video_rec.write(self.draw_map) 
            
            
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
            # Write the final frame multiple times to let it show for a while
            for i in range(300):
                self.video_rec.write(self.draw_map) 
            
            
    # Checks if the passed in node is within the acceptable threshold of the goal
    def checkIfGoal(self, input_node):
        node = input_node[3]
        # print("Distance to goal: {}".format(math.sqrt((self.goal_node[0] - node[0])**2 + ((self.goal_node[1] - node[1])**2))))
 
        # Check euclidian distance between x and y
        if not math.sqrt((self.goal_node[0] - node[0])**2 + (self.goal_node[1] - node[1])**2) <= self.dist_tolerance:
            return False
        # Check difference between the current and goal angle
        elif not abs(self.goal_node[2] - node[2]) <= self.angle_tolerance:
            return False
        else:
            return True
    
    # Finds the shortest path from the start to end goal using Dijkstra's algorithm
    def findPath(self):
        start_time = time.time()
        # Loop until we've removed all nodes from the open list
        while not self.open_list.empty():
            # Pop off the highest priority node
            priority_node = self.open_list.get()
            
            # print(priority_node)
            
            # First check if this is the goal node
            if self.checkIfGoal(priority_node):
                print("Goal found")
                # If it is then backtrack to the start node and break out of the loop
                self.backtrack(priority_node)
                break
            
            cost = priority_node[0]
            
            pixel_loc = priority_node[3]
            
            self.applyMoves(pixel_loc, cost)
            
            # Move the current node to the closed nodes list
            self.closed_list[str(pixel_loc)] = priority_node

        print("Total time: {} seconds".format(time.time() - start_time))
            
        cv2.imshow("Exploration map", self.draw_map)
        cv2.waitKey(0)
        
        if self.record:
            self.video_rec.release()
    
if __name__ == '__main__':
    solver = AStarMapSolver(record_video=True)
    
    solver.findPath()