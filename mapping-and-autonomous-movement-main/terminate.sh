#!/bin/bash

# Find and kill the processes
killall -q roscore
pkill -9 python3
killall -q roslaunch
killall -q rosrun

# Wait for the processes to be killed
sleep 2

# Print a message indicating the processes have been terminated
echo "All processes have been terminated."