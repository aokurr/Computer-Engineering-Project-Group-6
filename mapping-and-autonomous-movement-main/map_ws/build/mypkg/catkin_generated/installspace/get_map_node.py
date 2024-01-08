#!/usr/bin/env python3


import rospy
from nav_msgs.srv import GetMap
import numpy as np
import cv2
import matplotlib.pyplot as plt
import fcntl

# convert string to numpy array
def convert_to_array(data):
    data = np.array(data.data, dtype=np.int8)
    data = data + 1
    #as uint8
    data = data.astype(np.uint8)
    return data

# reshape data to 2048*2048*x and fill with '-1's if not enough data
def reshape_data(data):
    data = np.append(data, np.zeros(2048 * 2048 - data.shape[0], dtype=np.uint8))
    data = data.reshape(2048, 2048)
    data[data < 99] = 0
    data = np.transpose(data.nonzero())
    print(data)
    #data = np.where*
    # start_index = 700
    # end_index = 1301  # The end index is exclusive, so we use 1201 instead of 1200
    # # Extract the subarray
    # return data[start_index:end_index, start_index:end_index]
    return data

def dynamic_map_client():
    rospy.init_node('dynamic_map_client_node')
    rospy.wait_for_service('dynamic_map')
    rate = rospy.Rate(1)
    
    
    while not rospy.is_shutdown():
        try:
            get_map = rospy.ServiceProxy('dynamic_map', GetMap)
            response = get_map()
            if response.map:
                data_arr = convert_to_array(response.map)
                data = reshape_data(data_arr)
                #write data to file, so we can read it from another script, delete the file first 
                try:
                    with open("/home/yusuf/map.txt", 'x') as file:
                        fcntl.flock(file,fcntl.LOCK_EX)
                        np.savetxt(file, data, fmt="%d", delimiter=",")
                        fcntl.flock(file,fcntl.LOCK_UN)
                except FileExistsError:
                    with open("/home/yusuf/map.txt", 'w') as file:
                        fcntl.flock(file,fcntl.LOCK_EX)
                        np.savetxt(file, data, fmt="%d", delimiter=",")
                        fcntl.flock(file,fcntl.LOCK_UN)
                #show the data
                rate.sleep()

                
            else:
                rospy.loginfo('Received empty map')
        except rospy.ServiceException as e:
            rospy.loginfo('Service call failed: {}'.format(e))


if __name__ == '__main__':
    try:
        dynamic_map_client()
    except rospy.ROSInterruptException:
        pass
