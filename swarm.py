# -*- coding: UTF-8 -*-

import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy

# moveBy(0, 0, 0, 0)# (a,b,c,d) a = X-axis, b = Z-axis, c = Y-axis, d = Y-axis pivot

april_ip = "10.202.0.1" 
casey_ip = "10.202.1.1"
donatello_ip = "10.202.2.1"
leonardo_ip = "10.202.3.1"
michelangelo_ip = "10.202.4.1"
raphael_ip = "10.202.5.1"
splinter_ip = "10.202.6.1"

# back = -1
# foreward = 1
# right = 1
# left = -1
# up = -1
# down = 1
# pivot = 0


def main():
		
    april = olympe.Drone(april_ip)
    casey = olympe.Drone(casey_ip)
    donatello = olympe.Drone(donatello_ip)
    leonardo = olympe.Drone(leonardo_ip)
    michelangelo = olympe.Drone(michelangelo_ip)
    raphael = olympe.Drone(raphael_ip)
    splinter = olympe.Drone(splinter_ip)

    swarm = [april, casey, donatello, leonardo, michelangelo, raphael, splinter]

    for drone in swarm:
    	drone.connect()

    for drone in swarm:
    	drone(TakeOff()).wait().success()

    for drone in swarm:
    	drone(moveBy( 0 , 0 , -2 , 0 )).wait() 

    for drone in swarm: # x = back/forward z = right/left y = up/down
    	drone(moveBy( 0 , -2 , 0 , 0 )).wait() # drone moves up left/-Z by 3

    for drone in swarm: # x = back/forward z = right/left y = up/down
    	drone(moveBy( 2 , 0 , 0 , 0 )).wait() # drone moves up foreward by 3
  


if __name__ == "__main__":
    main()