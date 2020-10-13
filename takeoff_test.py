import math
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode

april_ip = "10.202.0.1" 
casey_ip = "10.202.1.1"
donatello_ip = "10.202.2.1"
leonardo_ip = "10.202.3.1"
michelangelo_ip = "10.202.4.1"
raphael_ip = "10.202.5.1"
splinter_ip = "10.202.6.1"

april = olympe.Drone(april_ip)
casey = olympe.Drone(casey_ip)
donatello = olympe.Drone(donatello_ip)
leonardo = olympe.Drone(leonardo_ip)
michelangelo = olympe.Drone(michelangelo_ip)
raphael = olympe.Drone(raphael_ip)
splinter = olympe.Drone(splinter_ip)

# Take-off
# drone(TakeOff()).wait()




april(
    TakeOff()
    >> casey(TakeOff())
    >> donatello(TakeOff())
).wait().success()


for coords in route:
    april(
        moveTo(coords[0], coords[1], 1, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> casey(moveTo(coords[0], coords[1], 1, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        >> donatello(moveTo(coords[0], coords[1], 1, MoveTo_Orientation_mode.TO_TARGET, 0.0))
    ).wait().success()