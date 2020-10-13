# -*- coding: UTF-8 -*-

import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing

DRONE_IP_A = "10.202.0.1"
DRONE_IP_B = "10.202.1.1"


def main():
    drone_A = olympe.Drone(DRONE_IP_A)
    drone_B = olympe.Drone(DRONE_IP_B)
    drone_A.connect()
    drone_B.connect()
    drone_A(TakeOff()).wait().success()
    drone_B(TakeOff()).wait().success()


if __name__ == "__main__":
    main()