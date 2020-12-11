# -*- coding: UTF-8 -*-

import math
import olympe
from haversine import haversine, Unit
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
from d2 import d2
from d3 import d3
from d4 import d4
from d5 import d5
from d6 import d6
from d7 import d7


# working subscription - drone leader takes off and moves away
# casey takes off after drone leader takes off and will follow leaders position
# this does a square flight pattern

olympe.log.update_config({"loggers": {"olympe": {"level": "WARNING"}}})
poiIndex = 0

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
    raphael = findOffset(lat,lng,-40,0)
    michaelangelo = findOffset(lat,lng,-20,20)
    donatello = findOffset(lat,lng,-20,-20)
    splinter = findOffset(lat,lng,-40,40)
    leonardo = findOffset(lat,lng,-40,-40)
    casey = findOffset(lat,lng,-70,0)
    return [april, raphael, michaelangelo, donatello, splinter, leonardo, casey]

def makeSquareFormation(lat,lng):
    april = findOffset(lat,lng,40,0) # leader middle
    raphael = findOffset(lat,lng,-40,0) # middle bottom
    michaelangelo = findOffset(lat,lng,0,40) # top right
    donatello = findOffset(lat,lng,0,-40) # top left
    splinter = findOffset(lat,lng,0,0) # middle top
    leonardo = findOffset(lat,lng,-40,-40) # bottom left
    casey = findOffset(lat,lng,-40,40) # bottom right
    return [april, raphael, michaelangelo, donatello, splinter, leonardo, casey]

def makeLineFormation(lat,lng):
    # april = findOffset(lat,lng,100,0) 
    # raphael = findOffset(lat,lng,80,0) 
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
raphael = olympe.Drone(raphael_ip)
splinter = olympe.Drone(splinter_ip)

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
        global poiIndex
        poiIndex += 1
        # lat = event.args["latitude"]
        # lon = event.args["longitude"]
        # c_poi = (lat, lon)
        # poi = (21.371518, -157.71161)
        print('\n ------->')
        print('\n ------->')
        print('\n ------->')

        #print(poiIndex)

        print('\n ------->')
        print('\n ------->')
        print('\n ------->')

        # two_lat = event.args["latitude"]
        # two_lon = event.args["longitude"]

        # if meters < 8:
        #     casey(moveToChanged(status="CANCELED")
        #         >> moveTo(21.370950, -157.709998, 10, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        #         >> moveToChanged(status="DONE")
        #     )
        #     donatello(moveToChanged(status="CANCELED")
        #         >> moveTo(21.370950, -157.709998, 20, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        #         >> moveToChanged(status="DONE")
        #     )
        #     leonardo(moveToChanged(status="CANCELED")
        #         >> moveTo(21.370950, -157.709998, 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        #         >> moveToChanged(status="DONE")
        #     )
        #     two_lat = 21.370950
        #     two_lon = -157.709998

        
        # casey_coords = findOffset(two_lat,two_lon,-5,0)
        # donatello_coords = findOffset(two_lat,two_lon,5,0)
        # leonardo_coords = findOffset(two_lat,two_lon,0,5)

        # michelangelo_coords = findOffset(event.args["latitude"],event.args["longitude"],0,-10)
        # raphael_coords = findOffset(event.args["latitude"],event.args["longitude"],10,10)
        # splinter_coords = findOffset(event.args["latitude"],event.args["longitude"],-10,-10)
        
        donatello(
            moveTo(
                float(d2[poiIndex]["lat"]),
                float(d2[poiIndex]["lng"]),
                float(d2[poiIndex]["alt"]),
                MoveTo_Orientation_mode.TO_TARGET, 0.0))
        leonardo(
            moveTo(
                float(d3[poiIndex]["lat"]),
                float(d3[poiIndex]["lng"]),
                float(d3[poiIndex]["alt"]),
                MoveTo_Orientation_mode.TO_TARGET, 0.0))
        michelangelo(
            moveTo(
                float(d4[poiIndex]["lat"]),
                float(d4[poiIndex]["lng"]),
                float(d4[poiIndex]["alt"]),
                MoveTo_Orientation_mode.TO_TARGET, 0.0))
        raphael(
            moveTo(
                float(d5[poiIndex]["lat"]),
                float(d5[poiIndex]["lng"]),
                float(d5[poiIndex]["alt"]),
                MoveTo_Orientation_mode.TO_TARGET, 0.0))
        splinter(
            moveTo(
                float(d6[poiIndex]["lat"]),
                float(d6[poiIndex]["lng"]),
                float(d6[poiIndex]["alt"]),
                MoveTo_Orientation_mode.TO_TARGET, 0.0))


        casey(
            moveTo(
                float(d7[poiIndex]["lat"]),
                float(d7[poiIndex]["lng"]),
                float(d7[poiIndex]["alt"]),
                MoveTo_Orientation_mode.TO_TARGET, 0.0))

        


        
        # casey(moveTo(casey_coords[0], casey_coords[1], 10, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        # donatello(moveTo(donatello_coords[0], donatello_coords[1], 15, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        # leonardo(moveTo(leonardo_coords[0], leonardo_coords[1], 20, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        # michelangelo(moveTo(michelangelo_coords[0], michelangelo_coords[1], 25, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        # raphael(moveTo(raphael_coords[0], raphael_coords[1], 30, MoveTo_Orientation_mode.TO_TARGET, 0.0))
        # splinter(moveTo(splinter_coords[0], splinter_coords[1], 35, MoveTo_Orientation_mode.TO_TARGET, 0.0))



        print(
            "latitude = {latitude} longitude = {longitude} altitude = {altitude}".format(
                **event.args
            )
        )

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
        followerTakeOff(casey)

        followerTakeOff(donatello)
        followerTakeOff(leonardo)
        followerTakeOff(michelangelo)
        followerTakeOff(raphael)
        followerTakeOff(splinter)



 
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
    raphael.connect()
    splinter.connect()

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
                >> moveTo(21.36945383, -157.7133445, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37028804, -157.7134336, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37040696, -157.7134463, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37055568, -157.7134622, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37079381, -157.7134876, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37096092, -157.7135054, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37136676, -157.7135488, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37236059, -157.7128414, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37262856, -157.7126507, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37273558, -157.7125745, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37300355, -157.7123838, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.3731374, -157.7122885, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37327125, -157.7121933, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37303895, -157.7118213, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.37155529, -157.7122354, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.36980861, -157.712723, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
            ).wait().success()
            drone(Landing()).wait()
            assert drone(FlyingStateChanged(state="landed")).wait().success()

    assert flight_listener.has_observed_takeoff
    drone.disconnect()