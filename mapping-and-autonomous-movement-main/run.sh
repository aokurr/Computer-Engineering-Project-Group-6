#!/bin/bash

# Start roscore
roscore &

# Wait for roscore to initialize
sleep 2

# Start publisher_node.py
rosrun mypkg publisher_node.py &

sleep 2

# Start tutorial.launch using roslaunch
roslaunch hector_slam_launch tutorial.launch &

sleep 2

# Start get_map_node.py
rosrun mypkg get_map_node.py &

sleep 2

# Start position_node.py
rosrun mypkg position_node.py &

sleep2

python map.py &

sleep 2
python autonom.py

