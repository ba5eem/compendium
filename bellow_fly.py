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
                >> moveTo(21.2205, -157.4242, 0, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 3, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 8, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 12, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 16, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 20, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 24, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 27, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 31, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 36, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 40, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 44, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 48, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 51, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 55, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 60, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 64, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 68, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 72, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 76, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 80, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 84, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 88, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 92, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 95, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 100, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 104, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2205, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2206, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2207, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2208, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2209, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2210, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2210, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2211, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2212, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2213, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2214, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2215, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2216, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2217, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2218, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2218, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2218, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2218, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2219, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2219, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2219, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2219, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2220, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2220, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2220, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2221, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2221, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2221, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2222, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2222, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2222, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2222, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2223, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2223, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2223, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2224, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2224, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2224, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2224, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2225, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2225, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2225, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2226, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2226, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2226, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2226, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2227, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2227, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2227, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2227, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2227, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2228, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2228, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2228, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2228, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2229, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2229, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2229, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2230, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2230, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2230, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2230, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2230, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2230, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2230, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2232, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2232, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2232, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2232, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2232, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2232, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2233, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2233, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2233, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2234, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2234, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2234, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2234, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2234, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2235, -157.4239, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2236, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2236, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2236, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2237, -157.4240, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2237, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2237, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2237, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2238, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2238, -157.4241, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2238, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2238, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2239, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2239, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2239, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2240, -157.4242, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2240, -157.4243, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2240, -157.4243, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2240, -157.4243, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2241, -157.4243, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2241, -157.4243, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2241, -157.4244, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2241, -157.4244, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2242, -157.4244, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2242, -157.4244, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2242, -157.4244, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2242, -157.4245, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2243, -157.4245, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2243, -157.4245, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2243, -157.4245, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2244, -157.4245, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2244, -157.4246, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2244, -157.4246, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2244, -157.4246, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2244, -157.4246, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2245, -157.4246, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2245, -157.4246, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2245, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2245, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2246, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2246, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2246, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2246, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2247, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2247, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2247, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2247, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2247, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2248, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2248, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2248, -157.4249, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2248, -157.4249, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2249, -157.4249, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2249, -157.4249, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2249, -157.4249, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2249, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2249, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2250, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2250, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2250, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2252, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2252, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4252, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4252, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4252, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4253, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2251, -157.4253, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2250, -157.4253, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2250, -157.4253, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2250, -157.4254, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2250, -157.4254, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2250, -157.4254, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2249, -157.4255, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2249, -157.4255, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2249, -157.4254, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2248, -157.4254, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2247, -157.4254, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2247, -157.4254, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2246, -157.4254, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2245, -157.4253, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2244, -157.4253, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2243, -157.4253, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2242, -157.4253, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2242, -157.4252, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2241, -157.4252, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2240, -157.4252, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2239, -157.4252, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2238, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2237, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2236, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2236, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2235, -157.4251, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2235, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2234, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2233, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2232, -157.4250, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2231, -157.4249, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2230, -157.4249, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2229, -157.4249, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2228, -157.4249, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2228, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2227, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2226, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2225, -157.4248, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2224, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2223, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2222, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2222, -157.4247, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2221, -157.4246, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")
>> moveTo(21.2220, -157.4246, 108, MoveTo_Orientation_mode.TO_TARGET, 0.0)
>> moveToChanged(status="DONE")

            ).wait().success()
            drone(Landing()).wait()
            assert drone(FlyingStateChanged(state="landed")).wait().success()

    assert flight_listener.has_observed_takeoff
    drone.disconnect()