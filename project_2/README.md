# O'Shea ENPM661 Project 2: Dijkstra's Path Planner
Provides a class for using Diskstra's algorithm to find the shortest path between a given start and goal point

# Dependencies
- numpy
- copy
- opencv-python
- queue
- math

# Instructions
- The dijkstra_ryan_oshea.py file can be run as is to take in a start and goal point and find the shortest path between them. By defaul this will display the end map and create a video to show the search algorithm's progress over time.
- To turn off the video creation function, set the record_video variable on line 416 to false. This can help speed up computation time as the call to the frame writing function will no longer happen.
- The x and y values for the start and end points are input by the user upon running the program. The following pairs were used to produced the output shown in the video:
    - Enter start pixel x value: 30
    - Enter start pixel y value: 450
    - Enter goal pixel x value: 1100
    - Enter goal pixel y value: 20
- This should produce a path that starts in the upper left of the image and ends in the bottom right while navigating around obstacles
- The colors shown on the map have the following meaning
    - Green: clearance around obstacles
    - Red: Obstacles
    - Black: Unexplored space
    - Blue: Explored spaces
    - Yellow Square: Start point and traced path
    - Purple: Goal point