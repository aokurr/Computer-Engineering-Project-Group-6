# The Jokers - Computer Engineering Project Group-6

## Installation

### Connection
There is a script in Raspberry and it connects directly with the following network information:<br />
Network Name --> jokers<br />
password     --> jokers123<br /><br />
If such wifi cannot be provided, first of all, it is connected to Raspberry via hdmi. Manual access to the internet is provided.<br />
In order to connect with ssh and access the robot's shell, the robot's IP must be known.<br />
For this, ping raspberrypi.local command can be used with another linux computer on the same internet. There may be other methods. After obtaining the IP, with another computer on the same network,A request for ssh connection is sent with the ssh pi4@<IP> command.<br />

A password will be requested with this command. The password we set for our robot is 'raspberry'. This password is entered.<br />
Name     --> pi4<br />
password --> raspberry<br />

In order to run this project where we used many different libraries, follow the steps carefully and make sure you don't miss any of the steps.

1.  Robot-Side
    To run the server in the robot, create a terminal, and run the following command:
    `python3 ~/Desktop/RemoteControl/TestMain.py`

2.  Desktop App
    The desktop application requires the installation of more than one library.
    If you already have the libraries below, you can skip the installations. If not, run the commands below after installing the libraries.
    `git clone https://github.com/ProjeGroup6/desktop-app.git`
    `cd desktop-app`
    `python app.py`
    After running this code, enter the robot's IP in the input field.

If the following libraries are not installed, please install them:

- PyQt5:
  You can install this library that we used to design the interface application from this [link](https://pypi.org/project/PyQt5/).
- pyqtgraph:
  In order to run custom map and autonomous code, install this library by following this [link](https://pypi.org/project/pyqtgraph/).
- OpenCV:
  You can install this library, which we use to transfer the camera image, from this [link](https://pypi.org/project/opencv-python/).
- Tensorflow:
  You can install this library, which we used to load our custom-trained model, from this [link](https://pypi.org/project/tensorflow/).
- Tensorflow Object Detection API:
  You can install this API, which we used to detect objects using our model, by following the steps in this [link](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/tf2.md).

1. Mapping and Autonomous Movement
   You will need the ROS-Melodic Distribution installed on Ubuntu 18.04 to be able to run the map.
   (We haven't tested other distributions)
   Follow this [link](https://releases.ubuntu.com/18.04/) to get Ubuntu 18.04 and this [link](http://wiki.ros.org/melodic/Installation/Ubuntu) to install ROS-Melodic.
   Assuming your ROS installation is ready, you shouldn't need to follow the steps below:

- `git clone https://github.com/ProjeGroup6/mapping-and-autonomous-movement.git`
- `cd mapping-and-autonomous-movement/map_ws`
  After downloading map workspace, you also should download ydlidar ros driver and hector slam drivers.
  first go to `/src` folder in map_ws: `cd src`
- Then: `git clone https://github.com/tu-darmstadt-ros-pkg/hector_slam`
- Also clone yd lidar ros driver: `git clone https://github.com/YDLIDAR/ydlidar_ros_driver`
  After downloading all the packages, run the `catkin_make` command in the `/src` folder.
  Then go to the `cd mapping-and-autonomous-movement` folder and run the `./run.sh` command. This will run the ROS drivers and codes.
  (Here, make sure the robot is on and the servers are runned.)
  After running the `./run.sh` command, the robot will move autonomously to a point you click on the graphic that will open.
  Run the `./terminate.sh` command to terminate the application.

---
