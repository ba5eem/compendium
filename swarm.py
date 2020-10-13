# -*- coding: UTF-8 -*-

import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing

april_ip = "10.202.0.1"
casey_ip = "10.202.1.1"
donatello_ip = "10.202.2.1"
leonardo_ip = "10.202.3.1"
michelangelo_ip = "10.202.4.1"
raphael_ip = "10.202.5.1"
splinter_ip = "10.202.6.1"


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


if __name__ == "__main__":
    main()