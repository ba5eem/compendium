import math
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy, moveTo
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode
from olympe.messages.ardrone3.PilotingState import (
    PositionChanged,
    SpeedChanged,
    AttitudeChanged,
    AltitudeAboveGroundChanged,
    AlertStateChanged,
    FlyingStateChanged,
    NavigateHomeStateChanged,
)

olympe.log.update_config({"loggers": {"olympe": {"level": "WARNING"}}})
april_ip = "10.202.0.1"
casey_ip = "10.202.1.1"
donatello_ip = "10.202.2.1"

april = olympe.Drone(april_ip)
casey = olympe.Drone(casey_ip)
donatello = olympe.Drone(donatello_ip)

april.connect()
casey.connect()
donatello.connect()


april(
    FlyingStateChanged(state="hovering")
    | (TakeOff() & FlyingStateChanged(state="hovering"))
).wait().success()

casey(
    FlyingStateChanged(state="hovering")
    | (TakeOff() & FlyingStateChanged(state="hovering"))
).wait().success()

donatello(
    FlyingStateChanged(state="hovering")
    | (TakeOff() & FlyingStateChanged(state="hovering"))
).wait().success()


april(moveTo(21.291352585005598, -157.83071637153628, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
casey(moveTo(21.292041798528878, -157.83067882061005, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
donatello(moveTo(21.292046245732305, -157.83146202564242, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
april(moveTo(21.289915280551007, -157.83071637153628, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
casey(moveTo(21.28988584184699, -157.83067882061005, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
donatello(moveTo(21.289171636823124, -157.83146202564242, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
april(moveTo(21.290633932778302, -157.82994507905642, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
casey(moveTo(21.290963820187933, -157.8295218792944, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
donatello(moveTo(21.290608941277714, -157.8299194409449, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
april(moveTo(21.290633932778302, -157.83148766401615, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
casey(moveTo(21.290963820187933, -157.8318357619257, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
donatello(moveTo(21.290608941277714, -157.83300461033994, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
april(moveTo(21.291352585005598, -157.82994507905642, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
casey(moveTo(21.292041798528878, -157.8295218792944, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
donatello(moveTo(21.292046245732305, -157.8299194409449, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
april(moveTo(21.289915280551007, -157.82994507905642, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
casey(moveTo(21.28988584184699, -157.8295218792944, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
donatello(moveTo(21.289171636823124, -157.8299194409449, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
april(moveTo(21.291352585005598, -157.83148766401615, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
casey(moveTo(21.292041798528878, -157.8318357619257, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
donatello(moveTo(21.292046245732305, -157.83300461033994, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
april(moveTo(21.289915280551007, -157.83148766401615, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
casey(moveTo(21.28988584184699, -157.8318357619257, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))
donatello(moveTo(21.289171636823124, -157.83300461033994, 0.86, MoveTo_Orientation_mode.TO_TARGET, 0.0))


