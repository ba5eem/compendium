import math
import threading
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode

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
    april = findOffset(lat,lng,100,0) 
    rapheal = findOffset(lat,lng,80,0) 
    michaelangelo = findOffset(lat,lng,60, 0) 
    donatello = findOffset(lat,lng,40,0) 
    splinter = findOffset(lat,lng,20,0) 
    leonardo = findOffset(lat,lng,0,0) 
    casey = findOffset(lat,lng,-20,0) 
    return [april, rapheal, michaelangelo, donatello, splinter, leonardo, casey]


# arr = makeLineFormation(21.368492831528414,-157.712818)
# print(arr)



april_ip = "10.202.0.1" 
casey_ip = "10.202.1.1"
# donatello_ip = "10.202.2.1"
# leonardo_ip = "10.202.3.1"
# michelangelo_ip = "10.202.4.1"
# raphael_ip = "10.202.5.1"
# splinter_ip = "10.202.6.1"

april = olympe.Drone(april_ip)
casey = olympe.Drone(casey_ip)
# donatello = olympe.Drone(donatello_ip)
# leonardo = olympe.Drone(leonardo_ip)
# michelangelo = olympe.Drone(michelangelo_ip)
# raphael = olympe.Drone(raphael_ip)
# splinter = olympe.Drone(splinter_ip)



# swarm = [april, casey, donatello, leonardo, michelangelo, raphael, splinter]

swarm = [april, casey]

for drone in swarm:
    drone.connection()

# Take-off
def takeOff(drone):
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

for drone in swarm:
    takeOff(drone)









def move(index,coords):

    april(
        moveTo(route[index+6][0], route[index+6][1], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=1)
    ).wait().success()
    casey(
        moveTo(route[index][0], route[index][1], 1, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=2)
    ).wait().success()
    donatello(
        moveTo(route[index+6][0], route[index+6][1], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=3)
    ).wait().success()
    leonardo(
        moveTo(route[index][0], route[index][1], 1, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=4)
    ).wait().success()
    michelangelo(
        moveTo(route[index+6][0], route[index+6][1], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    raphael(
        moveTo(route[index][0], route[index][1], 1, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    splinter(
        moveTo(route[index+6][0], route[index+6][1], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()







for index, coords in enumerate(route):
    move(index,coords)




# using

# def moveDonatello():
#     poi = april.get_state(GpsLocationChanged)
#     donatello(
#         moveTo(poi["latitude"],  poi["longitude"], 0.9, MoveTo_Orientation_mode.TO_TARGET, 0.0)
#         >> PCMD(1, 0, 0, 0, 0, 0)
#         >> FlyingStateChanged(state="hovering", _timeout=5)
#     ).wait().success()

# # using
# setInterval(moveDonatello,3)
    


# def moveLeonardo():
#     poi = april.get_state(GpsLocationChanged)
#     leonardo(
#         moveTo(poi["latitude"],  poi["longitude"], 0.9, MoveTo_Orientation_mode.TO_TARGET, 0.0)
#         >> PCMD(1, 0, 0, 0, 0, 0)
#         >> FlyingStateChanged(state="hovering", _timeout=5)
#     ).wait().success()

# # using
# setInterval(moveLeonardo,4)

# def moveMichelangelo():
#     poi = april.get_state(GpsLocationChanged)
#     michelangelo(
#         moveTo(poi["latitude"],  poi["longitude"], 0.9, MoveTo_Orientation_mode.TO_TARGET, 0.0)
#         >> PCMD(1, 0, 0, 0, 0, 0)
#         >> FlyingStateChanged(state="hovering", _timeout=5)
#     ).wait().success()

# # using
# setInterval(moveMichelangelo,4)


