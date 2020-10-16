# -*- coding: UTF-8 -*-

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged
from olympe.messages.camera import start_recording, stop_recording
from olympe.messages import gimbal

DRONE_IP = "10.202.0.1"

if __name__ == "__main__":
    with olympe.Drone(DRONE_IP) as drone:
        drone.connect()

        # Start a flying action asynchronously
        flyingAction = drone(
            TakeOff()
            >> FlyingStateChanged(state="hovering", _timeout=5)
            >> moveBy(0, -40, 0, 0)
            >> FlyingStateChanged(state="hovering", _timeout=5)
            >> moveBy(40, 0, 0, 0)
            >> FlyingStateChanged(state="hovering", _timeout=5)
            >> moveBy(0, 40, 0, 0)
            >> FlyingStateChanged(state="hovering", _timeout=5)
            >> moveBy(-40, 0, 0, 0)
            >> FlyingStateChanged(state="hovering", _timeout=5)
            >> Landing()
        )



        # Wait for the end of the flying action
        if not flyingAction.wait().success():
            assert False, "Cannot complete the flying action"


        # Leaving the with statement scope: implicit drone.disconnect() but that
        # is still a good idea to perform the drone disconnection explicitly
        drone.disconnect()