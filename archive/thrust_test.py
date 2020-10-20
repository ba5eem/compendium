# -*- coding: UTF-8 -*-

import olympe
import time
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy
from olympe.messages.ardrone3.GPSSettings import HomeChanged

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

# 21.432657 
# -157.786460
# SetHome(latitude, longitude, altitude, _timeout=10, _no_expect=False, _float_tol=(1e-07, 1e-09))
def main():
		
    april = olympe.Drone(april_ip)
    casey = olympe.Drone(casey_ip)


    april.connect()
    casey.connect()

    april(TakeOff()).wait().success()
    casey(TakeOff()).wait().success()

    casey(olympe.messages.ardrone3.Piloting.moveTo(21.432657, -157.786460, 3, olympe.enums.ardrone3.Piloting.MoveTo_Orientation_mode(0), 90, _timeout=20, _no_expect=False, _float_tol=(1e-07, 1e-09)))

    april(olympe.messages.ardrone3.GPSSettingsState.HomeChanged(21.432657, -157.786460))
    april(olympe.messages.rth.return_to_home())
    april(olympe.messages.ardrone3.Piloting.PCMD(0, 50, 100, 100, 100, 10, _timeout=10, _no_expect=False, _float_tol=(1e-07, 1e-09)))
    olympe.messages.ardrone3.GPSSettingsState.HomeChanged(latitude=21.432657, longitude=-157.786460, altitude=-1, _policy='check_wait', _float_tol=(1e-07, 1e-09))


    drone(moveTo(21.432657, -157.786460, 0.8617546558380127, MoveTo_Orientation_mode.TO_TARGET, 0.0))

    april(olympe.messages.ardrone3.Piloting.NavigateHome(1))

        
    april(moveBy( 0 , 0 , -2 , 0 )).wait()


    casey(moveBy( -1 , 0 , 0 , 0 )).wait() 
    casey(moveBy( 0 , 0 , -1.8 , 0 )).wait() 

april(moveBy( 2 , 0 , 0 , 0 )).wait()
casey(moveBy( 2 , 0 , 0 , 0 )).wait()
        
if __name__ == "__main__":
    main()