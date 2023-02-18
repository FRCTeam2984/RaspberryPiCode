import sys
import time
from networktables import NetworkTables

NetworkTables.initialize()
print("is server: " + str(NetworkTables.isServer()))
print("is connected: " + str(NetworkTables.isConnected()))

sd = NetworkTables.getTable("SmartDashboard")

while True:
    cone_x = sd.getNumber("cone_x", 0)
    cone_y = sd.getNumber("cone_y", 0)
    print(str(cone_x) + ", " + str(cone_y))
    time.sleep(0.1)