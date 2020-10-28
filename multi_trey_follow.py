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
#poiIndex = 0

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
    poiIndex = 0

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.has_observed_takeoff = False

    @olympe.listen_event(PositionChanged())
    def onPositionChanged(self, event, scheduler):
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
                >> moveTo(21.43378258952731, -157.7882350477468, 1, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378258971239, -157.7882350475352, 11, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378258989746, -157.7882350473236, 21, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259008253, -157.7882350471119, 31, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4337825902676, -157.7882350469003, 41, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259045268, -157.7882350466886, 51, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259063775, -157.788235046477, 61, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259082282, -157.7882350462654, 71, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259100789, -157.7882350460537, 81, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259119296, -157.7882350458421, 91, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259137803, -157.7882350456304, 101, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4337825915631, -157.7882350454188, 111, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259174817, -157.7882350452072, 121, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259193324, -157.7882350449956, 131, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259211831, -157.7882350447839, 141, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259230337, -157.7882350445723, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259230337, -157.7882350445723, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259230337, -157.7882350445723, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259230337, -157.7882350445723, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259230337, -157.7882350445723, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259230337, -157.7882350445723, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259230337, -157.7882350445723, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43382774908902, -157.7882350446139, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43387290587442, -157.7882350446554, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43391806265958, -157.7882350446969, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4339632194445, -157.7882350447385, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43400837622917, -157.78823504478, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4340535330136, -157.7882350448215, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43409868979779, -157.7882350448631, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43414384658173, -157.7882350449046, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43418900336543, -157.7882350449461, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43423416014888, -157.7882350449877, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4342793169321, -157.7882350450292, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43432447371506, -157.7882350450708, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43436963049779, -157.7882350451123, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478728027, -157.7882350451539, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478728027, -157.7882350451539, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478723443, -157.788283275566, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4344147871747, -157.7883315059781, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478710107, -157.7883797363901, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478701356, -157.7884279668023, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478691216, -157.7884761972144, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478679686, -157.7885244276264, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478666768, -157.7885726580386, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4344147865246, -157.7886208884507, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478636763, -157.7886691188627, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478636763, -157.7886691188627, 151, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43436962969169, -157.7886594726959, 150, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43432447300071, -157.788649826532, 149, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43427931629468, -157.7886401803709, 148, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43423415957363, -157.7886305342128, 147, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43418900283754, -157.7886208880576, 146, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43414384608641, -157.7886112419053, 145, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43409868932025, -157.788601595756, 144, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43405353253906, -157.7885919496095, 143, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43400837574283, -157.7885823034659, 142, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43400837574283, -157.7885823034659, 142, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43396321893156, -157.7885726573253, 141, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43391806210527, -157.7885630111876, 140, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43387290526393, -157.7885533650528, 139, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43382774840756, -157.7885437189208, 138, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259153616, -157.7885340727919, 137, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43373743464972, -157.7885244266658, 136, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43369227774824, -157.7885147805426, 135, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43364712083173, -157.7885051344223, 134, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196390019, -157.788495488305, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196390019, -157.788495488305, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196377935, -157.7885437185861, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196364461, -157.7885919488672, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196349598, -157.7886401791483, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196333346, -157.7886884094293, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196315705, -157.7887366397105, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196296675, -157.7887848699916, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196276256, -157.7888331002726, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196254448, -157.7888813305537, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196231251, -157.7889295608348, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43360196231251, -157.7889295608348, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43364711922725, -157.78892956109, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43369227614174, -157.7889295613452, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43373743305599, -157.7889295616004, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378258997, -157.7889295618555, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43382774688376, -157.7889295621107, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43387290379729, -157.7889295623659, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43391806071057, -157.7889295626211, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43396321762361, -157.7889295628763, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4340083745364, -157.7889295631314, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43405353144895, -157.7889295633866, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43409868836125, -157.7889295636418, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4341438452733, -157.788929563897, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43418900218512, -157.7889295641521, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4342341590967, -157.7889295644074, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43427931600803, -157.7889295646625, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43432447291912, -157.7889295649177, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43436962982997, -157.7889295651729, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43441478674056, -157.7889295654281, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43445994365091, -157.7889295656832, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43445994365091, -157.7889295656832, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43443284964559, -157.7889006271977, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43440575563517, -157.7888716887228, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43437866161966, -157.7888427502587, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43435156759907, -157.7888138118051, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43432447357338, -157.7887848733623, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43429737954261, -157.7887559349302, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43427028550675, -157.7887269965087, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.4342431914658, -157.7886980580979, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43421609741976, -157.7886691196978, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43418900336863, -157.7886401813084, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43416190931242, -157.7886112429297, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43413481525111, -157.7885823045616, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43410772118472, -157.7885533662042, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43408062711323, -157.7885244278575, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43405353303666, -157.7884954895216, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.434026438955, -157.7884665511962, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43399934486826, -157.7884376128816, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43397225077642, -157.7884086745776, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43394515667949, -157.7883797362843, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43391806257748, -157.7883507980017, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43389096847038, -157.7883218597298, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43386387435819, -157.7882929214686, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43383678024091, -157.788263983218, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43380968611854, -157.7882350449782, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43378259199108, -157.788206106749, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43375549785854, -157.7881771685305, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43372840372091, -157.7881482303226, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43370130957819, -157.7881192921255, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
                >> moveTo(21.43367421543038, -157.788090353939, 133, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
            ).wait().success()
            drone(Landing()).wait()
            assert drone(FlyingStateChanged(state="landed")).wait().success()

    assert flight_listener.has_observed_takeoff
    drone.disconnect()