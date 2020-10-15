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



route = [
          [
            -157.8174018859863,
            21.371404228269693
          ],
          [
            -157.8009223937988,
            21.40816684949972
          ],
          [
            -157.79045104980466,
            21.36980564390211
          ],
          [
            -157.796630859375,
            21.386909590741197
          ],
          [
            -157.80967712402344,
            21.386909590741197
          ],
          [
            -157.79457092285156,
            21.384991490613558
          ],
          [
            -157.7889060974121,
            21.369485924934303
          ],
          [
            -157.78839111328125,
            21.407207941990915
          ],
          [
            -157.77053833007812,
            21.407367760345984
          ],
          [
            -157.7717399597168,
            21.390745715552566
          ],
          [
            -157.78701782226562,
            21.390905551903227
          ],
          [
            -157.7688217163086,
            21.36980564390211
          ],
          [
            -157.76521682739258,
            21.407527578526267
          ],
          [
            -157.76023864746094,
            21.407367760345984
          ],
          [
            -157.76350021362305,
            21.37060493826749
          ],
          [
            -157.74238586425778,
            21.37699913610513
          ],
          [
            -157.7420425415039,
            21.367887319624206
          ],
          [
            -157.81705856323242,
            21.36996550312423
          ]
        ]



drone_location = drone.get_state(GpsLocationChanged)
# coords = [21.377386152841197, -157.712818]
# # Go back home
# drone(
#     moveBy(0, -1000, 0, math.pi)
#     >> casey(moveTo(coords[0], coords[1], 50, MoveTo_Orientation_mode.TO_TARGET, 0.0))
#     >> donatello(moveTo(coords[0], coords[1], 10, MoveTo_Orientation_mode.TO_TARGET, 0.0))
#     >> FlyingStateChanged(state="hovering", _timeout=5)
#     >> moveToChanged(latitude=drone_location["latitude"], longitude=drone_location["longitude"], altitude=drone_location["altitude"], orientation_mode=MoveTo_Orientation_mode.TO_TARGET, status='DONE', _policy='wait')
#     >> FlyingStateChanged(state="hovering", _timeout=5)
# ).wait()

def move(coords):
    drone(
        moveTo(coords[0], coords[1], 100, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> casey(moveTo(coords[0], coords[1], 50, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        >> donatello(moveTo(coords[0], coords[1], 100, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    updateSwarm()

for coords in route:
    move(coords)

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