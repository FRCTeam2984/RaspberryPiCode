import sys
from networktables import NetworkTables
import random
import time

if len(sys.argv) != 2:
    print("Cannot connect to robot")
    exit(0)

ip = sys.argv[1]
NetworkTables.initialize(server=ip)
sd = NetworkTables.getTable("SmartDashboard")

def send_cube_data(data):
    print(f"has cube = {data[0]}, x={data[1]}, y={data[2]}")
    sd.putBoolean("has_cube", data[0])
    sd.putNumber("cube_x", data[1])
    sd.putNumber("cube_y", data[2])
    
    
def send_cone_data(data):
    print(f"has ;cone = {data[0]}, x={data[1]}, y={data[2]}")
    sd.putBoolean("has_cone", data[0])
    sd.putNumber("cone_x", data[1])
    sd.putNumber("cone_y", data[2])
    
    

def random_num():
    return random.randint(0, 200)

def random_bool():
    num = random.randint(0, 1)
    
    if num == 1:
        return True
    else:
        return False
    
    
    
while True:
    has_cube = random_bool()
    cube_x = random_num()
    cube_y = random_num()
    
    send_cube_data([has_cube, cube_x, cube_y])
    
    time.sleep(1)