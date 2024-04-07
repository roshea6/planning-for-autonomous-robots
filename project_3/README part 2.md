# Ryan O'Shea and Kyle DeGuzman ENPM661 Project 3 Part 2: A* Path Planner with Holonomic Kinematic Constraints and Gazebo Simulation
Provides a class for using the A* algorithm to find the shortest path between a given start and goal point. Includes options to make it weighted A* as well. 

# Contributors
- Ryan O'Shea: roshea, 120465291
- Kyle DeGuzman: kdeguzma, 120452062

# Project Link
https://github.com/roshea6/planning-for-autonomous-robots
The project can be found at the above URL under the project 3 folder. I keep all of my code for the class in this repo so the project 0, 1, and 2 code is there as well. The ROS workspace is not uploaded to the github repo but the turtlebot package is included as part of the submission.

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
- IT IS HIGHLY RECOMMENDED THAT THE GAZEBO SIMULATION NOT BE LAUNCHED UNTIL THE IS CALCULATED AND DISPLAYED DUE TO GAZEBO TAKING UP PROCESSING POWER. My path planning time went from 10 seconds to 250 seconds when having Gazebo launched in the background.
- The proj3_part_2_ryan_kyle.py file can be run as is to take in a start and goal state (x, y, theta) and find the shortest path between them. By default this will display the end map and create a video to show the search algorithm's progress over time. The user is also prompted for input on the clearance value step size which controls. These control the clearance zone around obstacles and the size of the step the robot takes from a given start point to it's next space on the map.
- Not all combinations of parameters are guaranteed to produce a solution because of of state thresholds (location and orientation bins) and inconsitencies in how well the gazebo simulation follows the generated path.
- The x and y values for the start and end points are input by the user upon running the program. The following pairs were used to produced the output shown in the video:
    - Enter the clearance value in mm (5-50 recommended): 50
    - Enter the first rpm (30-70 recommended): 40
    - Enter the second rpm (30-70 recommended): 60
    - Enter start pixel x value: 500
    - Enter start pixel y value: 1000
    - Enter start theta value that is a multiple of 30: 0
    - Enter goal pixel x value: 5500
    - Enter goal pixel y value: 500
    - Enter start theta value that is a multiple of 30: 0
    - Please enter a step size value between 1 and 3: 2

- This should produce a path that starts in the center left of the map, navigates around the obstacles, and ends in the bottom right
- One the map is produced
- The colors shown on the map have the following meaning
    - Green: clearance around obstacles
    - Red: Obstacles
    - Black: Unexplored space
    - Blue: Explored spaces
    - Yellow Square: Start point and traced path
    - Purple: Goal point

- Once the map is displayed launch the Gazebo simulation in a different terminal using ros2 launch turtlebot3_project3 competition_world.launch.py
- After the simulation has been launch click on the OpenCv window displaying the map and hit any key to begin publishing velocity commands to the turtlebot over the cmd_vel topic.
- The publishing commands were tuned to account for the slowdown on my laptop so performance in Gazebo will likely be different from machine to machine. 

- Additional inputs: Line 607 also allows you to enter several other inputs for the path planner to change its behavior
    - c2g_weight: Scaling factor for the cost to go in the A* algorithm. Values above 1 will make it weighted A*, 1 excatly will make it standard A* and 0 will make it Dijkstra's
    - use_lines: Whether to draw lines between start and end points during explortation instead of just filling in individual explored pixels
    - save_every_n_frame: How many frames to skip between saving a frame during video recording. Wihtout this, saving every video frame greatly slows down the code and make a giant video.

# Video Links
- A* path exploration: https://drive.google.com/file/d/1ZVubO02lbz_9VhkznGPaGJQU6tnCllft/view?usp=sharing 
- Turtlebot executing the optimal path in Gazebo: https://drive.google.com/file/d/11BP7ehdM-Oh04oHShcMgfa9iJeVAKWk1/view?usp=sharing 
