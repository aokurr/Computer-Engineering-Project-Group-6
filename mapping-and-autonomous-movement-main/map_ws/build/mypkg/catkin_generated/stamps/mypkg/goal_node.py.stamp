#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import PointStamped
import fcntl

def clicked_point_callback(msg):
    # Callback function to handle received clicked points
    rospy.loginfo("Clicked point: (%f, %f, %f)", msg.point.x, msg.point.y, msg.point.z)
    with open('~/goal.txt', 'w') as file:
        fcntl.flock(writefile, fcntl.LOCK_EX)
        file.write(str(msg.point.x) + "," + str(msg.point.y) + "\n")
        fcntl.flock(writefile, fcntl.LOCK_UN)

def clicked_point_listener():
    # Initialize the ROS node
    rospy.init_node('clicked_point_listener', anonymous=True)

    # Subscribe to the clicked point topic
    rospy.Subscriber('/clicked_point', PointStamped, clicked_point_callback)

    # Spin ROS event loop
    rospy.spin()

if __name__ == '__main__':
    clicked_point_listener()
