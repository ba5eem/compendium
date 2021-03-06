import math
import threading
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, moveTo, Circle, PCMD
from olympe.messages.ardrone3.PilotingState import moveToChanged, FlyingStateChanged, PositionChanged, AttitudeChanged
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged
from olympe.messages.ardrone3.PilotingState import GpsLocationChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode

route = [
  [ 21.368492831528414, -157.712818 ],
  [ 21.368582663056824, -157.712818 ],
  [ 21.368672494585237, -157.712818 ],
  [ 21.36876232611365, -157.712818 ],
  [ 21.36885215764206, -157.712818 ],
  [ 21.368941989170473, -157.712818 ],
  [ 21.369031820698883, -157.712818 ],
  [ 21.369121652227296, -157.712818 ],
  [ 21.36921148375571, -157.712818 ],
  [ 21.36930131528412, -157.712818 ],
  [ 21.369391146812532, -157.712818 ],
  [ 21.369480978340945, -157.712818 ],
  [ 21.369570809869355, -157.712818 ],
  [ 21.36966064139777, -157.712818 ],
  [ 21.36975047292618, -157.712818 ],
  [ 21.36984030445459, -157.712818 ],
  [ 21.369930135983005, -157.712818 ],
  [ 21.370019967511414, -157.712818 ],
  [ 21.370109799039827, -157.712818 ],
  [ 21.37019963056824, -157.712818 ],
  [ 21.37019963056824, -157.7127215361443 ],
  [ 21.37019963056824, -157.7126250722886 ],
  [ 21.37019963056824, -157.7125286084329 ],
  [ 21.37019963056824, -157.7124321445772 ],
  [ 21.37019963056824, -157.7123356807215 ],
  [ 21.37019963056824, -157.7122392168658 ],
  [ 21.37019963056824, -157.7121427530101 ],
  [ 21.37019963056824, -157.71204628915442 ],
  [ 21.37019963056824, -157.71194982529872 ],
  [ 21.37019963056824, -157.71185336144302 ],
  [ 21.37019963056824, -157.7117568975873 ],
  [ 21.37019963056824, -157.7116604337316 ],
  [ 21.37019963056824, -157.7115639698759 ],
  [ 21.37019963056824, -157.7114675060202 ],
  [ 21.37019963056824, -157.7113710421645 ],
  [ 21.37019963056824, -157.7112745783088 ],
  [ 21.37019963056824, -157.7111781144531 ],
  [ 21.37019963056824, -157.7110816505974 ],
  [ 21.37019963056824, -157.7109851867417 ],
  [ 21.37019963056824, -157.710888722886 ],
  [ 21.370109799039827, -157.7107922590303 ],
  [ 21.370019967511418, -157.71069579517462 ],
  [ 21.369930135983005, -157.71059933131892 ],
  [ 21.36984030445459, -157.71050286746322 ],
  [ 21.36975047292618, -157.71040640360752 ],
  [ 21.36966064139777, -157.71030993975182 ],
  [ 21.36957080986936, -157.71021347589613 ],
  [ 21.369480978340945, -157.71011701204043 ],
  [ 21.369391146812532, -157.71002054818473 ],
  [ 21.369301315284122, -157.70992408432903 ],
  [ 21.36921148375571, -157.7098276204733 ],
  [ 21.369121652227296, -157.7097311566176 ],
  [ 21.369031820698886, -157.7096346927619 ],
  [ 21.368941989170473, -157.7095382289062 ],
  [ 21.36885215764206, -157.7094417650505 ],
  [ 21.36876232611365, -157.70934530119482 ],
  [ 21.368672494585237, -157.70924883733912 ],
  [ 21.368582663056827, -157.70915237348342 ],
  [ 21.368492831528414, -157.70905590962772 ],
  [ 21.368403, -157.70895944577202 ], # heads southwest after this - possible to split the pack
  [ 21.368313168471587, -157.70905590844418 ],
  [ 21.368223336943178, -157.70915237111635 ],
  [ 21.368133505414765, -157.7092488337885 ],
  [ 21.36804367388635, -157.70934529646067 ],
  [ 21.36795384235794, -157.70944175913283 ],
  [ 21.36786401082953, -157.70953822180496 ],
  [ 21.36777417930112, -157.70963468447712 ],
  [ 21.367684347772705, -157.70973114714928 ],
  [ 21.367594516244292, -157.70982760982145 ],
  [ 21.367504684715882, -157.7099240724936 ],
  [ 21.36741485318747, -157.71002053516577 ],
  [ 21.367325021659056, -157.71011699783793 ],
  [ 21.367235190130646, -157.7102134605101 ],
  [ 21.367145358602233, -157.71030992318225 ],
  [ 21.36705552707382, -157.7104063858544 ],
  [ 21.36696569554541, -157.71050284852654 ],
  [ 21.366875864016997, -157.7105993111987 ],
  [ 21.366786032488587, -157.71069577387087 ],
  [ 21.366696200960174, -157.71079223654303 ],
  [ 21.36660636943176, -157.7108886992152 ]
]



april_ip = "10.202.0.1" 
casey_ip = "10.202.1.1"
donatello_ip = "10.202.2.1"
leonardo_ip = "10.202.3.1"
michelangelo_ip = "10.202.4.1"
raphael_ip = "10.202.5.1"
splinter_ip = "10.202.6.1"

april = olympe.Drone(april_ip)
casey = olympe.Drone(casey_ip)
donatello = olympe.Drone(donatello_ip)
leonardo = olympe.Drone(leonardo_ip)
michelangelo = olympe.Drone(michelangelo_ip)
raphael = olympe.Drone(raphael_ip)
splinter = olympe.Drone(splinter_ip)

# april.connection()
# casey.connection()

swarm = [casey, donatello, leonardo, michelangelo, raphael, splinter]
april.connection()
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

takeOff(april)
for drone in swarm:
    takeOff(drone)



def moveSwarm(poi):
    casey(
        moveTo(poi["latitude"],  poi["longitude"], 0.9, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    donatello(
        moveTo(poi["latitude"],  poi["longitude"], 0.8, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    leonardo(
        moveTo(poi["latitude"],  poi["longitude"], 1.1, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    michelangelo(
        moveTo(poi["latitude"],  poi["longitude"], 0.7, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    raphael(
        moveTo(poi["latitude"],  poi["longitude"], 1.2, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    splinter(
        moveTo(poi["latitude"],  poi["longitude"], 0.6, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()




def updateSwarm():
    leader_location = april.get_state(GpsLocationChanged)
    moveSwarm(leader_location)



def move(coords):
    april(
        moveTo(coords[0], coords[1], 1, MoveTo_Orientation_mode.TO_TARGET, 0.0)
        >> PCMD(1, 0, 0, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    updateSwarm()



for coords in route:
    move(coords)




    





