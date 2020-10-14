import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, moveBy, moveTo
from olympe.messages.ardrone3.PilotingState import (
    PositionChanged,
    AlertStateChanged,
    FlyingStateChanged,
    NavigateHomeStateChanged,
    moveToChanged,
    GpsLocationChanged
)
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode
olympe.log.update_config({"loggers": {"olympe": {"level": "WARNING"}}}) #quiet the output


drone = olympe.Drone("10.202.0.1")
casey = olympe.Drone("10.202.1.1")

casey.connect()
casey(
    FlyingStateChanged(state="hovering")
    | (TakeOff() & FlyingStateChanged(state="hovering"))
).wait()
drone.connect()
drone(
    FlyingStateChanged(state="hovering")
    | (TakeOff() & FlyingStateChanged(state="hovering"))
).wait()


drone(
        moveBy(-5, 0, 0, 0)
        >> casey(moveTo(drone.get_state(GpsLocationChanged)["latitude"],  drone.get_state(GpsLocationChanged)["longitude"], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        >> drone(moveBy(10, 0, 0, 0))
        >> casey(moveTo(drone.get_state(GpsLocationChanged)["latitude"],  drone.get_state(GpsLocationChanged)["longitude"], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0))
    ).wait()

# class FlightListener(olympe.EventListener):
#     @olympe.listen_event(PositionChanged())
#     def onPositionChanged(self, event, scheduler):
#         print(event.args["latitude"], event.args["longitude"])
#         moveCasey(event.args["latitude"], event.args["longitude"])





# def moveCasey(lat,lng):
#     casey(
#         moveTo(lat,  lng, 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0)
#         >> FlyingStateChanged(state="hovering", _timeout=5)
#         >> moveToChanged(latitude=lat, longitude=lng, altitude=0.8, orientation_mode=MoveTo_Orientation_mode.TO_TARGET, status='DONE', _policy='wait')
#         >> FlyingStateChanged(state="hovering", _timeout=5)
#     ).wait()



# with FlightListener(drone):
#     drone(
#         moveBy(-5, 0, 0, 0)
#         >> casey(moveTo(drone.get_state(GpsLocationChanged)["latitude"],  drone.get_state(GpsLocationChanged)["longitude"], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0))
#         >> drone(moveBy(-5, 0, 0, 0))
#         >> casey(moveTo(drone.get_state(GpsLocationChanged)["latitude"],  drone.get_state(GpsLocationChanged)["longitude"], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0))
#     ).wait()


    
    # drone(Landing()).wait()
    # drone(FlyingStateChanged(state="landed")).wait()
    # drone.disconnect()



