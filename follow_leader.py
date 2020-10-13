import math
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode


april_ip = "10.202.0.1" 
casey_ip = "10.202.1.1"

april = olympe.Drone(april_ip)
casey = olympe.Drone(casey_ip)

april.connection()
casey.connection()


# Take-off
april(
    FlyingStateChanged(state="hovering", _policy="check")
    | FlyingStateChanged(state="flying", _policy="check")
    | (
        GPSFixStateChanged(fixed=1, _timeout=10, _policy="check_wait")
        >> (
            TakeOff(_no_expect=True)
            & FlyingStateChanged(
                state="hovering", _timeout=10, _policy="check_wait")
        )
    )
).wait()


# Take-off
casey(
    FlyingStateChanged(state="hovering", _policy="check")
    | FlyingStateChanged(state="flying", _policy="check")
    | (
        GPSFixStateChanged(fixed=1, _timeout=10, _policy="check_wait")
        >> (
            TakeOff(_no_expect=True)
            & FlyingStateChanged(
                state="hovering", _timeout=10, _policy="check_wait")
        )
    )
).wait()

april(
    moveTo(21.368492831528414, -157.712818, 0.8617546558380127, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> PCMD(1, 0, 0, 0, 0, 0)
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait().success()
# drone_location = drone.get_state(GpsLocationChanged)

# move 10m N of original location
#april(moveTo(21.368492831528414, -157.712818, 0.8617546558380127, MoveTo_Orientation_mode.TO_TARGET, 0.0)).wait().success()
#april_location = april.get_state(GpsLocationChanged)

# move casey to aprils location
april_location = drone.get_state(GpsLocationChanged)
casey(
    moveTo(april_location["latitude"],  april_location["longitude"], 0.8617546558380127, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> PCMD(1, 0, 0, 0, 0, 0)
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait().success()
