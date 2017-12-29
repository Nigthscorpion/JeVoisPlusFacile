import sys
import logging
from networktables import *
import time
import tkinter as tk

logging.basicConfig(level=logging.DEBUG)
NetworkTables.initialize(server="10.54.7.2")
while NetworkTables.isConnected() is False:
    time.sleep(.2)
table = NetworkTables.getTable("jevois")
print("Frame: {}".format(table.getNumber("Frame","N/A")))


