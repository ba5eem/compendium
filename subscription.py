import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy
from olympe.messages.ardrone3.PilotingState import (
    PositionChanged,
    AlertStateChanged,
    FlyingStateChanged,
    NavigateHomeStateChanged,
)

drone = olympe.Drone("10.202.0.1")
casey = olympe.Drone("10.202.1.1")
casey.connect()
casey(
    FlyingStateChanged(state="hovering")
    | (TakeOff() & FlyingStateChanged(state="hovering"))
).wait()

class FlightListener(olympe.EventListener):

    @olympe.listen_event(PositionChanged())
    def onPositionChanged(self, event, scheduler):
        awakeSwarm("{latitude}".format(**event.args),"{longitude}".format(**event.args))
        # print("{latitude}".format(**event.args))



def awakeSwarm(lat,lng):
    print(lat,lng)
    casey(
        moveTo(lat,  lng, 0.8, MoveTo_Orientation_mode.TO_TARGET, 0.0)
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
    drone(Landing()).wait()
    drone(FlyingStateChanged(state="landed")).wait()
    drone.disconnect()
