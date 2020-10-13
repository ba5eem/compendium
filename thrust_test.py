# -*- coding: UTF-8 -*-

import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy

# moveBy(0, 0, 0, 0)# (a,b,c,d) a = X-axis, b = Z-axis, c = Y-axis, d = Y-axis pivot

april_ip = "10.202.0.1" 
casey_ip = "10.202.1.1"


# a back = -1
# a foreward = 1
# b right = 1
# b left = -1
# c up = -1
# c down = 1
# pivot = 0


def main():
		
    april = olympe.Drone(april_ip)
    casey = olympe.Drone(casey_ip)


    swarm = [april, casey]

    for drone in swarm:
    	drone.connect()

    for drone in swarm:
    	drone(TakeOff()).wait().success()

    drone(moveBy( -1 , 0 , 0 , 0 )).wait()     



        
if __name__ == "__main__":
    main()