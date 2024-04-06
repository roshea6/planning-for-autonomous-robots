# Ryan O'Shea and Kyle DeGuzman ENPM661 Project 3 Part 2: A* Path Planner with Holonomic Kinematic Constraints and Gazebo Simulation
Provides a class for using the A* algorithm to find the shortest path between a given start and goal point. Includes options to make it weighted A* as well. 

# Contributors
- Ryan O'Shea: roshea, 120465291
- Kyle DeGuzman: kdeguzma, 120452062

# Project Link
https://github.com/roshea6/planning-for-autonomous-robots
The project can be found at the above URL under the project 3 folder. I keep all of my code for the class in this repo so the project 0, 1, and 2 code are there as well.

# Dependencies
- numpy
- copy
- opencv-python
- queue
- math
- time
- queue
- rclpy
- ROS2 Geometry Messages

# Instructions
- The a_star_ryan_kyle.py file can be run as is to take in a start and goal state (x, y, theta) and find the shortest path between them. By defaul this will display the end map and create a video to show the search algorithm's progress over time. The user is also prompted for input on the clearance value step size which controls. These control the clearance zone around obstacles and the size of the step the robot takes from a given start point to it's next space on the map.
- To turn off the video creation function, set the record_video variable on line 498 to false. This can help speed up computation time as the call to the frame writing function will no longer happen.
- The x and y values for the start and end points are input by the user upon running the program. The following pairs were used to produced the output shown in the video:
    - Enter the clearance value in mm (5-15 recommended): 10
    - Enter start pixel x value: 20
    - Enter start pixel y value: 80
    - Enter start theta value that is a multiple of 30: 0
    - Enter goal pixel x value: 1175
    - Enter goal pixel y value: 250
    - Enter start theta value that is a multiple of 30: 90
    - Please enter a step size value between 1 and 10: 5
- This should produce a path that starts in the lower left of the image and ends in the center right while navigating around obstacles
- The colors shown on the map have the following meaning
    - Green: clearance around obstacles
    - Red: Obstacles
    - Black: Unexplored space
    - Blue: Explored spaces
    - Yellow Square: Start point and traced path
    - Purple: Goal point

- Additional inputs: Line 498 also allows you to enter several other inputs for the path planner to change its behavior
    - c2g_weight: Scaling factor for the cost to go in the A* algorithm. Values above 1 will make it weighted A*, 1 excatly will make it standard A* and 0 will make it Dijkstra's
    - use_lines: Whether to draw lines between start and end points during explortation instead of just filling in individual explored pixels
    - save_every_n_frame: How many frames to skip between saving a frame during video recording. Wihtout this, saving every video frame greatly slows down the code and make a giant video.