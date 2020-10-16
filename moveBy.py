# -*- coding: UTF-8 -*-

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveTo, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, moveToChanged
from olympe.messages.camera import start_recording, stop_recording
from olympe.messages import gimbal
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode


DRONE_IP = "10.202.0.1"
casey = olympe.Drone("10.202.1.1")
donatello = olympe.Drone("10.202.2.1")
drone = olympe.Drone(DRONE_IP)
# if __name__ == "__main__":
#     with olympe.Drone(DRONE_IP) as drone:
drone.connect()
casey.connect()
donatello.connect()

# Start a flying action asynchronously
drone(
    TakeOff()
    >> FlyingStateChanged(state="hovering", _timeout=5)
    >> moveTo(21.371518652227294, -157.71239, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.371518652227294, -157.7116182859902, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> casey(21.371518652227294, -157.7116182859902, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveTo(21.3708, -157.7116182859902, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.370081347772704, -157.7116182859902, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.370081347772704, -157.71239, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.370081347772704, -157.7131617140098, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.3708, -157.7131617140098, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.371518652227294, -157.7131617140098, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> Landing()
)

casey(
    TakeOff()
    >> FlyingStateChanged(state="hovering", _timeout=5)
    >> moveTo(21.372057641397767, -157.71239, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.372057641397767, -157.71103950048285, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.3708, -157.71103950048285, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.36954235860223, -157.71103950048285, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.36954235860223, -157.71239, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.36954235860223, -157.71374049951714, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.3708, -157.71374049951714, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.372057641397767, -157.71374049951714, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> Landing()
)

donatello(
    TakeOff()
    >> FlyingStateChanged(state="hovering", _timeout=5)
    >> moveTo(21.37313561973871, -157.71239, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.37313561973871, -157.70988192946817, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.3708, -157.70988192946817, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.368464380261287, -157.70988192946817, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.368464380261287, -157.71239, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.368464380261287, -157.71489807053183, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.3708, -157.71489807053183, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> moveTo(21.37313561973871, -157.71489807053183, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> moveToChanged(status="DONE")
    >> Landing()
).wait().success()

# t:21.3708,lng:-157.709881 - east
# at:21.368464380261287,lng:-157.71239 - south

# Wait for the end of the flying action
# if not flyingAction.wait().success():
#     assert False, "Cannot complete the flying action"


# Leaving the with statement scope: implicit drone.disconnect() but that
# is still a good idea to perform the drone disconnection explicitly
drone.disconnect()
casey.disconnect()
donatello.disconnect()