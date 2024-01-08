#!/usr/bin/env python3
import rospy
import numpy as np
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped
import fcntl

def callback(data):
    pose = data.pose
    #write to file as x,y,z,roll,pitch,yaw
    try:
        with open('/home/yusuf/transform.txt', 'x') as file:
            fcntl.flock(file, fcntl.LOCK_EX)
            roll, pitch, yaw = quert_to_euler(pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)
            file.write(str(pose.position.x) + "," + str(pose.position.y) + "," + str(pose.position.z) + "," + str(roll) + "," + str(pitch) + "," + str(yaw) + "\n")
            fcntl.flock(file, fcntl.LOCK_UN)

    except FileExistsError:
        with open('/home/yusuf/transform.txt', 'w') as file:
            fcntl.flock(file, fcntl.LOCK_EX)
            roll, pitch, yaw = quert_to_euler(pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)
            file.write(str(pose.position.x) + "," + str(pose.position.y) + "," + str(pose.position.z) + "," + str(roll) + "," + str(pitch) + "," + str(yaw) + "\n")
            fcntl.flock(file, fcntl.LOCK_UN)

        
def quert_to_euler(qx, qy, qz, qw):
    #qx, qy, qz, qw
    #roll (x-axis rotation)
    sinr_cosp = 2 * (qw * qx + qy * qz)
    cosr_cosp = 1 - 2 * (qx * qx + qy * qy)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    #pitch (y-axis rotation)
    sinp = 2 * (qw * qy - qz * qx)
    if (np.abs(sinp) >= 1):
        pitch = np.sign(sinp) * np.pi / 2
    else:
        pitch = np.arcsin(sinp)

    #yaw (z-axis rotation)
    siny_cosp = 2 * (qw * qz + qx * qy)
    cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw

    
def listener():
    rospy.init_node('pose_listener', anonymous=True)

    rospy.Subscriber("slam_out_pose", PoseStamped, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass

