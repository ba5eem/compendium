# -*- coding: UTF-8 -*-

import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing

# moveBy(0, 0, 0, 0)# (a,b,c,d) a = X-axis, b = Z-axis, c = Y-axis, d = Y-axis pivot

april_ip = "10.202.0.1" 
casey_ip = "10.202.1.1"
donatello_ip = "10.202.2.1"
leonardo_ip = "10.202.3.1"
michelangelo_ip = "10.202.4.1"
raphael_ip = "10.202.5.1"
splinter_ip = "10.202.6.1"

# backwards with ' - '
# left with ' - '
back_forward = -2 # X
right_left = 0 # Z
Y = 0
pivot = 0


def main():
    april = olympe.Drone(april_ip)
    casey = olympe.Drone(casey_ip)
    donatello = olympe.Drone(donatello_ip)
    leonardo = olympe.Drone(leonardo_ip)
    michelangelo = olympe.Drone(michelangelo_ip)
    raphael = olympe.Drone(raphael_ip)
    splinter = olympe.Drone(splinter_ip)

    april.connect()
    casey.connect()
    donatello.connect()
    leonardo.connect()
    michelangelo.connect()
    raphael.connect()
    splinter.connect()


    
    april(TakeOff()).wait().success()
    casey(TakeOff()).wait().success()
    donatello(TakeOff()).wait().success()
    leonardo(TakeOff()).wait().success()
    michelangelo(TakeOff()).wait().success()
    raphael(TakeOff()).wait().success()
    splinter(TakeOff()).wait().success()



    april(moveBy( -2 , 0 , 0 , 0 )).wait()
    casey(moveBy( -2 , 0 , 0 , 0 )).wait()
    donatello(moveBy( -2 , 0 , 0 , 0 )).wait()
    leonardo(moveBy( -2 , 0 , 0 , 0 )).wait()
    michelangelo(moveBy( -2 , 0 , 0 , 0 )).wait()
    raphael(moveBy( -2 , 0 , 0 , 0 )).wait()
    splinter(moveBy( -2 , 0 , 0 , 0 )).wait()



if __name__ == "__main__":
    main()