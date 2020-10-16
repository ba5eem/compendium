# -*- coding: UTF-8 -*-

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveTo, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, moveToChanged
from olympe.messages.camera import start_recording, stop_recording
from olympe.messages import gimbal
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode


DRONE_IP = "10.202.0.1"

if __name__ == "__main__":
    with olympe.Drone(DRONE_IP) as drone:
        drone.connect()

        # Start a flying action asynchronously
        flyingAction = drone(
            TakeOff()
            >> FlyingStateChanged(state="hovering", _timeout=5)
            >> moveTo(21.291352, -157.830716, 15, MoveTo_Orientation_mode.NONE, 0.0)
            >> moveToChanged(status="DONE")
            >> Landing()
        )



        # Wait for the end of the flying action
        if not flyingAction.wait().success():
            assert False, "Cannot complete the flying action"


        # Leaving the with statement scope: implicit drone.disconnect() but that
        # is still a good idea to perform the drone disconnection explicitly
        drone.disconnect()