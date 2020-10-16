# -*- coding: UTF-8 -*-

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
    moveToChanged
)

# working subscription - drone leader takes off and moves away
# casey takes off after drone leader takes off and will follow leaders position
# this does a square flight pattern

olympe.log.update_config({"loggers": {"olympe": {"level": "WARNING"}}})

def findOffset(lat,lng,n,e):
    earthRadius=6378137
    dLat = n/earthRadius
    dLngM = earthRadius*math.cos(math.pi*lat/180)
    dLng = e/dLngM
    latOffset = lat + dLat * 180/math.pi
    lngOffset = lng + dLng * 180/math.pi
    return [latOffset,lngOffset]



def makeTriangleFormation(lat,lng):
    april = findOffset(lat,lng,20,0)
    rapheal = findOffset(lat,lng,-40,0)
    michaelangelo = findOffset(lat,lng,-20,20)
    donatello = findOffset(lat,lng,-20,-20)
    splinter = findOffset(lat,lng,-40,40)
    leonardo = findOffset(lat,lng,-40,-40)
    casey = findOffset(lat,lng,-70,0)
    return [april, rapheal, michaelangelo, donatello, splinter, leonardo, casey]

def makeSquareFormation(lat,lng):
    april = findOffset(lat,lng,40,0) # leader middle
    rapheal = findOffset(lat,lng,-40,0) # middle bottom
    michaelangelo = findOffset(lat,lng,0,40) # top right
    donatello = findOffset(lat,lng,0,-40) # top left
    splinter = findOffset(lat,lng,0,0) # middle top
    leonardo = findOffset(lat,lng,-40,-40) # bottom left
    casey = findOffset(lat,lng,-40,40) # bottom right
    return [april, rapheal, michaelangelo, donatello, splinter, leonardo, casey]

def makeLineFormation(lat,lng):
    # april = findOffset(lat,lng,100,0) 
    # rapheal = findOffset(lat,lng,80,0) 
    # michaelangelo = findOffset(lat,lng,60, 0) 
    # donatello = findOffset(lat,lng,40,0) 
    # splinter = findOffset(lat,lng,20,0) 
    # leonardo = findOffset(lat,lng,0,0) 
    casey = findOffset(lat,lng,-20,0) 
    return casey

DRONE_IP = "10.202.0.1"
casey_ip = "10.202.1.1"
donatello_ip = "10.202.2.1"
leonardo_ip = "10.202.3.1"
michelangelo_ip = "10.202.4.1"
raphael_ip = "10.202.5.1"
splinter_ip = "10.202.6.1"
casey = olympe.Drone(casey_ip)
donatello = olympe.Drone(donatello_ip)
leonardo = olympe.Drone(leonardo_ip)
michelangelo = olympe.Drone(michelangelo_ip)
# raphael = olympe.Drone(raphael_ip)
# splinter = olympe.Drone(splinter_ip)

def followerTakeOff(drone):
    drone(
        FlyingStateChanged(state="hovering")
        | (TakeOff() & FlyingStateChanged(state="hovering"))
    ).wait().success()


def print_event(event):
    # Here we're just serializing an event object and truncate the result if necessary
    # before printing it.
    if isinstance(event, olympe.ArsdkMessageEvent):
        max_args_size = 60
        args = str(event.args)
        args = (args[: max_args_size - 3] + "...") if len(args) > max_args_size else args
        print("{}({})".format(event.message.fullName, args))
    else:
        print(str(event))


# This is the simplest event listener. It just exposes one
# method that matches every event message and prints it.
class EveryEventListener(olympe.EventListener):
    @olympe.listen_event()
    def onAnyEvent(self, event, scheduler):
        print_event(event)


# olympe.EventListener implements the visitor pattern.
# You should use the `olympe.listen_event` decorator to
# select the type(s) of events associated with each method
class FlightListener(olympe.EventListener):

    # This set a default queue size for every listener method
    default_queue_size = 100

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.has_observed_takeoff = False

    @olympe.listen_event(PositionChanged())
    def onPositionChanged(self, event, scheduler):
        casey_coords = findOffset(event.args["latitude"],event.args["longitude"],0,10)
        donatello_coords = findOffset(event.args["latitude"],event.args["longitude"],0,30)
        leonardo_coords = findOffset(event.args["latitude"],event.args["longitude"],0,50)
        michelangelo_coords = findOffset(event.args["latitude"],event.args["longitude"],0,70)
        
        casey(moveTo(casey_coords[0], casey_coords[1], 10, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        donatello(moveTo(donatello_coords[0], donatello_coords[1], 15, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        leonardo(moveTo(leonardo_coords[0], leonardo_coords[1], 20, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        michelangelo(moveTo(michelangelo_coords[0], michelangelo_coords[1], 15, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        print(
            "latitude = {latitude} longitude = {longitude} altitude = {altitude}".format(
                **event.args
            )
        )

    

    # @olympe.listen_event(moveToChanged())
    # def onmoveToChanged(self, event, scheduler):
    #     print("--------->HEADING = {heading}".format(**event.args))    

    @olympe.listen_event(AttitudeChanged())
    def onAttitudeChanged(self, event, scheduler):
        print("roll = {roll} pitch = {pitch} yaw = {yaw}".format(**event.args))

    @olympe.listen_event(AltitudeAboveGroundChanged())
    def onAltitudeAboveGroundChanged(self, event, scheduler):
        print("height above ground = {altitude}".format(**event.args))

    @olympe.listen_event(SpeedChanged())
    def onSpeedChanged(self, event, scheduler):
        print("speedXYZ = ({speedX}, {speedY}, {speedZ})".format(**event.args))

    # You can also handle multiple message types with the same method
    @olympe.listen_event(
        FlyingStateChanged() | AlertStateChanged() | NavigateHomeStateChanged()
    )
    def onStateChanged(self, event, scheduler):
        # Here, since every "*StateChanged" message has a `state` argument
        # we can handle them uniformly to print the current associated state
        print("{} = {}".format(event.message.name, event.args["state"]))

    # You can also monitor a sequence of event using the complete Olympe DSL syntax
    @olympe.listen_event(
        FlyingStateChanged(state="takingoff", _timeout=1.)
        >> FlyingStateChanged(state="hovering", _timeout=5.)
    )
    def onTakeOff(self, event, scheduler):
        # This method will be called once for each completed sequence of event
        # FlyingStateChanged: motor_ramping -> takingoff -> hovering
        # followerTakeOff(casey)
        # followerTakeOff(donatello)
        # followerTakeOff(leonardo)
        # followerTakeOff(michelangelo)
        casey(TakeOff())
        donatello(TakeOff())
        leonardo(TakeOff())
        michelangelo(TakeOff())
        print("The drone has taken off!")
        self.has_observed_takeoff = True

    # The `default` listener method is only called when no other method
    # matched the event message The `olympe.listen_event` decorator usage
    # is optional for the default method, but you can use it to further
    # restrict the event messages handled by this method or to limit the
    # maximum size of it associated event queue (remember that the oldest
    # events are dropped silently when the event queue is full).
    @olympe.listen_event(queue_size=10)
    def default(self, event, scheduler):
        print_event(event)


if __name__ == "__main__":
    drone = olympe.Drone(DRONE_IP)
    # Explicit subscription to every event
    every_event_listener = EveryEventListener(drone)
    every_event_listener.subscribe()
    drone.connect()
    casey.connect()
    donatello.connect()
    leonardo.connect()
    michelangelo.connect()
    every_event_listener.unsubscribe()

    # You can also subscribe/unsubscribe automatically using a with statement
    with FlightListener(drone) as flight_listener:
        for i in range(2):
            assert drone(
                FlyingStateChanged(state="hovering")
                | (TakeOff() & FlyingStateChanged(state="hovering"))
            ).wait().success()
            assert drone(
                FlyingStateChanged(state="hovering", _timeout=5)
                >> moveTo(21.371518652227294, -157.71239, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.371518652227294, -157.7116182859902, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
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
            ).wait().success()
            drone(Landing()).wait()
            assert drone(FlyingStateChanged(state="landed")).wait().success()

    assert flight_listener.has_observed_takeoff
    drone.disconnect()