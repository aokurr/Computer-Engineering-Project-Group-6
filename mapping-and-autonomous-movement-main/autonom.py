import threading
import fcntl
import math
import socket

# ip adress of the robot to send messages (forward, backward...)
ip_address = "192.168.43.23"
port = 7000
# Create an object of Control
# control = Control()
myX = 0
myY = 0
goX = 0
goY = 0
angle = 0.0
forwardZone = False
turnLeft = False
turnRight = False
# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = (ip_address, port)
client_socket.connect(server_address)
print("Connected to {}:{}".format(*server_address))


# Write a function to control the robot dog according to distance value
def move_robot():
    while True:
        if forwardZone == True:
            # control.forWard()
            print("ileri git")
            # Get user input
            message = "1"
            # Send the message to the server
            client_socket.sendall(message.encode())
        elif turnLeft == True:
            # control.turnLeft()
            message = "5"
            # Send the message to the server
            client_socket.sendall(message.encode())
            print("sola git")
        elif turnRight == True:
            # control.turnRight()
            message = "7"
            # Send the message to the server
            client_socket.sendall(message.encode())
            print("saga git")


def get_values():
    global myX, myY, goX, goY, angle
    while True:
        path, x, y, angle = findPath()
        myX = x
        myY = y
        try:
            goX = path[5][0]
            goY = path[5][1]
        except:
            pass

        angle = float(angle) + 240.0
        angle = (180 / math.pi) * angle


def decideDirection(direction):
    global forwardZone, turnLeft, turnRight
    if direction >= 340 and direction <= 360 or direction >= 0 and direction <= 20:
        print("düz git")
        forwardZone = True
        turnLeft = False
        turnRight = False
    elif direction >= 160 and direction <= 200:
        print("geri git")
        forwardZone = False
        turnLeft = False
        turnRight = True
    elif direction > 200 and direction < 340:
        print("sola dön")
        forwardZone = False
        turnLeft = True
        turnRight = False
    else:
        print("sağa dön")
        forwardZone = False
        turnLeft = False
        turnRight = True


def findDirection():
    while True:
        dx = int(goX) - int(myX)
        dy = int(goY) - int(myY)
        print(dx, dy)
        target_angle = (180 / math.pi) * math.atan2(dy, dx)
        print(target_angle)
        direction = (angle - target_angle) % 360
        print(direction)
        decideDirection(direction)


def parser(receivedData):
    try:
        array = receivedData.split(",")
        # print(array)
        if len(array) == 5:
            first = array[0]
            second = array[1]
            third = array[2]
            fourth = array[3]
            fifth = array[4]
        return first, second, fifth
    except:
        pass


import heapq
import fcntl
import numpy as np
from scipy.ndimage import binary_dilation

def dilate(map):
    # mask is a cross size 3
    mask = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    # dilated = binary_dilation(map, mask)
    dilated = binary_dilation(map, mask)
    return dilated


def readfromfile2(filename, transfile):
    with open(filename, "r") as file:
        fcntl.flock(file, fcntl.LOCK_SH)
        mapdata = file.read()
        fcntl.flock(file, fcntl.LOCK_UN)

    mapdata = mapdata.replace("\n", ",").split(",")
    mapdata = [float(i) for i in mapdata if i]
    mapdata = np.array(mapdata)
    mapdata = mapdata.reshape(int(len(mapdata) / 2), 2)
    print(mapdata)
    # trans data is in following format and it is a single line
    # x, y, z, roll, pitch, yaw
    # read file
    with open(transfile, "r") as file:
        fcntl.flock(file, fcntl.LOCK_SH)
        transdata = file.read()
        fcntl.flock(file, fcntl.LOCK_UN)

    transdata = transdata.replace("\n", ",").split(",")
    print(transdata)
    # set x, y, z, roll, pitch and yaw
    x = int(float(transdata[0]))
    y = int(float(transdata[1]))
    yaw = float(transdata[5])

    map2data = np.zeros((2048, 2048), dtype=np.uint8)
    # mapdata is x,y pair of points
    # map2data is 2048x2048 array of 0s
    # change 0s to 1s where mapdata points are
    for point in mapdata:
        map2data[int(point[0])][int(point[1])] = 1

    dilated = dilate(map2data)
    print(map2data[0][0])
    return dilated.tolist(), x, y, yaw


def heuristic(start, goal):
    # Calculate the Manhattan distance between two points
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


def astar(grid, start, goal):
    rows = len(grid)
    cols = len(grid[0])

    # Define the possible movements (up, down, left, right, diagonal)
    movements = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Initialize the open and closed sets
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}

    # Initialize the cost to reach each cell as infinity
    g_score = [[float("inf")] * cols for _ in range(rows)]
    g_score[start[0]][start[1]] = 0

    # Initialize the estimated total cost from start to goal through each cell
    f_score = [[float("inf")] * cols for _ in range(rows)]
    f_score[start[0]][start[1]] = heuristic(start, goal)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct the path from goal to start
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for dx, dy in movements:
            neighbor = (current[0] + dx, current[1] + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1:
                    # Skip obstacles
                    continue

                # Calculate the cost to move to the neighbor
                g_score_neighbor = g_score[current[0]][current[1]] + 1

                if g_score_neighbor < g_score[neighbor[0]][neighbor[1]]:
                    # Update the cost and priority of the neighbor
                    came_from[neighbor] = current
                    g_score[neighbor[0]][neighbor[1]] = g_score_neighbor
                    f_score[neighbor[0]][neighbor[1]] = g_score_neighbor + heuristic(
                        neighbor, goal
                    )

                    # Add the neighbor to the open set
                    heapq.heappush(
                        open_set, (f_score[neighbor[0]][neighbor[1]], neighbor)
                    )

    # No path found
    return None


def readGoal():
    with open("goal.txt", "r") as file:
        fcntl.flock(file, fcntl.LOCK_SH)
        goaldata = file.read().split(",")
        fcntl.flock(file, fcntl.LOCK_UN)
	if(int(goaldata[0]) == -1):
            exit()
    return (int(goaldata[0]), int(goaldata[1]))


def findPath():
    # Example usage
    goal = readGoal()
    grid, x, y, yaw = readfromfile2("/home/yusuf/map.txt", "/home/yusuf/transform.txt")
    start = (1024 + x, 1024 + y)
    path = astar(grid, start, goal)

    if path:
        print("Path found:")
        for point in path:
            print(point)
    else:
        print("No path found.")

    # #add path to map and plot

    # #addPathandPlot(grid,path)

    # writefile = open("/home/yusuf/path.txt", "w")
    # for point in path:
    #     fcntl.flock(writefile, fcntl.LOCK_EX)
    #     writefile.write(str(point[0]) + "," + str(point[1]) + "," + str(x) +  "," +str(y)+ "," + str(yaw)+ "\n")
    #     fcntl.flock(writefile, fcntl.LOCK_UN)
    # writefile.close()
    return path, 1024 + x, 1024 + y, yaw


if __name__ == "__main__":
    print("Start")

    # Make a thread to listen to the port
    t = threading.Thread(target=move_robot, args=())
    t1 = threading.Thread(target=get_values, args=())
    t2 = threading.Thread(target=findDirection, args=())

    t.start()
    t1.start()
    t2.start()

    t.join()
    t1.join()
    t2.join()

    print("End")
