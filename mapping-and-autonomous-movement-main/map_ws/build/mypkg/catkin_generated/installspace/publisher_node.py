#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import socket


def myfoo():
    rospy.init_node('lidar_node')
    lidar_pub = rospy.Publisher('scan', LaserScan, queue_size=10)

    TCP_IP = '192.168.43.23'  # Empty string for any available interface
    TCP_PORT = 8080  # Choose an available port

    rospy.loginfo("Starting socket")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((TCP_IP, TCP_PORT))
    # sock.listen(1)

    # client_sock, addr = sock.accept()
    rospy.loginfo('Connected!')
    try:
        scan_msg = LaserScan()
        scan_msg.header.frame_id = 'laser_frame'
        size = 0
        ranges = []
        intensities = []
        angles = []
        while True:
            data = sock.recv(1024).decode()
            if data:
                
                # Split the data into individual tuples
                
                datasplit = data.split("x")
                for i,j in enumerate(datasplit):
                    if(len(j) > 2 and j.endswith(")") and j.startswith("(")):
                        withoutparanthesis = j.strip("()")
                        values = withoutparanthesis.split(",")
                        #rospy.loginfo(j)
                        if(values[0] == 'A'):
                            scan_msg.header.stamp = rospy.Time.now()
                            scan_msg.angle_min = min(angles)  # Set the minimum angle
                            scan_msg.angle_max = max(angles)  # Set the maximum angle
                        #calculate angle incrmenet
                            scan_msg.angle_increment = (scan_msg.angle_max - scan_msg.angle_min) / len(angles)
                            scan_msg.range_min = min(ranges)  # Set the minimum range
                            scan_msg.range_max = max(ranges)  # Set the maximum range
                            scan_msg.ranges = ranges  # Set the range values
                            scan_msg.intensities = intensities  # Set the intensity values
                        
                        # # Publish the scan_msg
                            lidar_pub.publish(scan_msg)
                            ranges.clear()
                            intensities.clear()
                            angles.clear()
                        else:
                            angles.append(float(values[0]))
                            ranges.append(float(values[1]))
                            intensities.append(10.0)
    finally:
        rospy.loginfo("Closing socket")
        # client_sock.close()
        sock.close()

rospy.loginfo("1")

try:
    myfoo()
except rospy.ROSInterruptException:
    pass
