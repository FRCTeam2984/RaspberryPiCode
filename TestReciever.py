import sys
import time
from networktables import NetworkTables

NetworkTables.initialize()
print("is server: " + str(NetworkTables.isServer()))
print("is connected: " + str(NetworkTables.isConnected()))

sd = NetworkTables.getTable("SmartDashboard")

while True:
    
    time.sleep(0.1)