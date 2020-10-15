import math
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode

drone = olympe.Drone("10.202.0.1")
casey = olympe.Drone("10.202.1.1")
donatello = olympe.Drone("10.202.2.1")
drone.connection()
casey.connection()
donatello.connection()

# Take-off
drone(
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
donatello(
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



drone(
    moveBy(0, 0, -100, math.pi)
    >> casey(moveBy(0, 0, -50, math.pi))
    >> donatello(moveBy(0, 0, -10, math.pi))
    >> PCMD(1, 0, 0, 0, 0, 0)
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait().success()



drone_location = drone.get_state(GpsLocationChanged)
coords = [21.377386152841197, -157.712818]
# Go back home
drone(
    moveTo(coords[0], coords[1], 100, MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> casey(moveTo(coords[0], coords[1], 50, MoveTo_Orientation_mode.TO_TARGET, 0.0))
    >> donatello(moveTo(coords[0], coords[1], 10, MoveTo_Orientation_mode.TO_TARGET, 0.0))
    >> FlyingStateChanged(state="hovering", _timeout=5)
    >> moveToChanged(latitude=drone_location["latitude"], longitude=drone_location["longitude"], altitude=drone_location["altitude"], orientation_mode=MoveTo_Orientation_mode.TO_TARGET, status='DONE', _policy='wait')
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait()



# Go back home
drone(
    moveTo(drone_location["latitude"],  drone_location["longitude"], drone_location["altitude"], MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> FlyingStateChanged(state="hovering", _timeout=5)
    >> moveToChanged(latitude=drone_location["latitude"], longitude=drone_location["longitude"], altitude=drone_location["altitude"], orientation_mode=MoveTo_Orientation_mode.TO_TARGET, status='DONE', _policy='wait')
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait()

# Go back home
casey(
    moveTo(drone_location["latitude"],  drone_location["longitude"], drone_location["altitude"], MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> FlyingStateChanged(state="hovering", _timeout=5)
    >> moveToChanged(latitude=drone_location["latitude"], longitude=drone_location["longitude"], altitude=drone_location["altitude"], orientation_mode=MoveTo_Orientation_mode.TO_TARGET, status='DONE', _policy='wait')
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait()

# Go back home
donatello(
    moveTo(drone_location["latitude"],  drone_location["longitude"], drone_location["altitude"], MoveTo_Orientation_mode.TO_TARGET, 0.0)
    >> FlyingStateChanged(state="hovering", _timeout=5)
    >> moveToChanged(latitude=drone_location["latitude"], longitude=drone_location["longitude"], altitude=drone_location["altitude"], orientation_mode=MoveTo_Orientation_mode.TO_TARGET, status='DONE', _policy='wait')
    >> FlyingStateChanged(state="hovering", _timeout=5)
).wait()

# Landing
drone(
    Landing()
    >> FlyingStateChanged(state="landed", _timeout=5)
).wait()

drone.disconnection()

# Landing
casey(
    Landing()
    >> FlyingStateChanged(state="landed", _timeout=5)
).wait()

casey.disconnection()

# Landing
donatello(
    Landing()
    >> FlyingStateChanged(state="landed", _timeout=5)
).wait()

donatello.disconnection()