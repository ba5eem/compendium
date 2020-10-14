import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy, moveTo
from olympe.messages.ardrone3.PilotingState import (
    PositionChanged,
    AlertStateChanged,
    FlyingStateChanged,
    NavigateHomeStateChanged,
    moveToChanged
)
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode
olympe.log.update_config({"loggers": {"olympe": {"level": "WARNING"}}}) #quiet the output


drone = olympe.Drone("10.202.0.1")
casey = olympe.Drone("10.202.1.1")


class FlightListener(olympe.EventListener):
    @olympe.listen_event(PositionChanged())
    def onPositionChanged(self, event, scheduler):
        print(event.args["latitude"], event.args["longitude"])
        awakeCasey(event.args["latitude"], event.args["longitude"])


def awakeCasey(lat,lng):
    casey.connect()
    casey(
        FlyingStateChanged(state="hovering")
        | (TakeOff() & FlyingStateChanged(state="hovering"))
    ).wait()
    moveCasey(lat,lng)


def moveCasey(lat,lng):
    casey(
        moveTo(lat,  lng, 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
        >> moveToChanged(latitude=lat, longitude=lng, altitude=0.8, orientation_mode=MoveTo_Orientation_mode.TO_TARGET, status='DONE', _policy='wait')
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()



with FlightListener(drone):
    drone.connect()
    drone(
        FlyingStateChanged(state="hovering")
        | (TakeOff() & FlyingStateChanged(state="hovering"))
    ).wait()
    drone(moveBy(-5, 0, 0, 0)).wait()
    drone(moveBy(10, 0, 0, 0)).wait()
    drone(Landing()).wait()
    drone(FlyingStateChanged(state="landed")).wait()
    drone.disconnect()



