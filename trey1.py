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

# working subscription - drone leader takes off and moves away
# casey takes off after drone leader takes off and will follow leaders position
# this does a square flight pattern

olympe.log.update_config({"loggers": {"olympe": {"level": "WARNING"}}})

d1_route = [
{"lat":"21.43378258952731","lng":"-157.7882350477468","alt":"2.867914736270905e-05"},
{"lat":"21.43378258971239","lng":"-157.7882350475352","alt":"10.00002867821604"},
{"lat":"21.43378258989746","lng":"-157.7882350473236","alt":"20.00002867821604"},
{"lat":"21.43378259008253","lng":"-157.7882350471119","alt":"30.00002867821604"},
{"lat":"21.4337825902676","lng":"-157.7882350469003","alt":"40.00002867821604"},
{"lat":"21.43378259045268","lng":"-157.7882350466886","alt":"50.00002867821604"},
{"lat":"21.43378259063775","lng":"-157.788235046477","alt":"60.00002867635339"},
{"lat":"21.43378259082282","lng":"-157.7882350462654","alt":"70.00002867821604"},
{"lat":"21.43378259100789","lng":"-157.7882350460537","alt":"80.00002867821604"},
{"lat":"21.43378259119296","lng":"-157.7882350458421","alt":"90.00002867914736"},
{"lat":"21.43378259137803","lng":"-157.7882350456304","alt":"100.000028678216"},
{"lat":"21.4337825915631","lng":"-157.7882350454188","alt":"110.0000286791474"},
{"lat":"21.43378259174817","lng":"-157.7882350452072","alt":"120.000028678216"},
{"lat":"21.43378259193324","lng":"-157.7882350449956","alt":"130.000028678216"},
{"lat":"21.43378259211831","lng":"-157.7882350447839","alt":"140.0000286772847"},
{"lat":"21.43378259230337","lng":"-157.7882350445723","alt":"150.000028678216"},
{"lat":"21.43378259230337","lng":"-157.7882350445723","alt":"150.000028678216"},
{"lat":"21.43378259230337","lng":"-157.7882350445723","alt":"150.000028678216"},
{"lat":"21.43378259230337","lng":"-157.7882350445723","alt":"150.000028678216"},
{"lat":"21.43378259230337","lng":"-157.7882350445723","alt":"150.000028678216"},
{"lat":"21.43378259230337","lng":"-157.7882350445723","alt":"150.000028678216"},
{"lat":"21.43378259230337","lng":"-157.7882350445723","alt":"150.000028678216"},
{"lat":"21.43382774908902","lng":"-157.7882350446139","alt":"150.0000204024836"},
{"lat":"21.43387290587442","lng":"-157.7882350446554","alt":"150.0000160671771"},
{"lat":"21.43391806265958","lng":"-157.7882350446969","alt":"150.0000156741589"},
{"lat":"21.4339632194445","lng":"-157.7882350447385","alt":"150.0000192206353"},
{"lat":"21.43400837622917","lng":"-157.78823504478","alt":"150.0000267084688"},
{"lat":"21.4340535330136","lng":"-157.7882350448215","alt":"150.0000381348655"},
{"lat":"21.43409868979779","lng":"-157.7882350448631","alt":"150.0000535035506"},
{"lat":"21.43414384658173","lng":"-157.7882350449046","alt":"150.0000728117302"},
{"lat":"21.43418900336543","lng":"-157.7882350449461","alt":"150.0000960631296"},
{"lat":"21.43423416014888","lng":"-157.7882350449877","alt":"150.0001232540235"},
{"lat":"21.4342793169321","lng":"-157.7882350450292","alt":"150.0001543853432"},
{"lat":"21.43432447371506","lng":"-157.7882350450708","alt":"150.00018945802"},
{"lat":"21.43436963049779","lng":"-157.7882350451123","alt":"150.0002284701914"},
{"lat":"21.43441478728027","lng":"-157.7882350451539","alt":"150.0002714246511"},
{"lat":"21.43441478728027","lng":"-157.7882350451539","alt":"150.0002714246511"},
{"lat":"21.43441478723443","lng":"-157.788283275566","alt":"150.0002843532711"},
{"lat":"21.4344147871747","lng":"-157.7883315059781","alt":"150.0003011999652"},
{"lat":"21.43441478710107","lng":"-157.7883797363901","alt":"150.000321963802"},
{"lat":"21.43441478701356","lng":"-157.7884279668023","alt":"150.0003466457129"},
{"lat":"21.43441478691216","lng":"-157.7884761972144","alt":"150.0003752447665"},
{"lat":"21.43441478679686","lng":"-157.7885244276264","alt":"150.0004077628255"},
{"lat":"21.43441478666768","lng":"-157.7885726580386","alt":"150.0004441980273"},
{"lat":"21.4344147865246","lng":"-157.7886208884507","alt":"150.0004845522344"},
{"lat":"21.43441478636763","lng":"-157.7886691188627","alt":"150.000528822653"},
{"lat":"21.43441478636763","lng":"-157.7886691188627","alt":"150.000528822653"},
{"lat":"21.43436962969169","lng":"-157.7886594726959","alt":"149.0004767002538"},
{"lat":"21.43432447300071","lng":"-157.788649826532","alt":"148.0004286775365"},
{"lat":"21.43427931629468","lng":"-157.7886401803709","alt":"147.0003847526386"},
{"lat":"21.43423415957363","lng":"-157.7886305342128","alt":"146.0003449227661"},
{"lat":"21.43418900283754","lng":"-157.7886208880576","alt":"145.0003091925755"},
{"lat":"21.43414384608641","lng":"-157.7886112419053","alt":"144.0002775574103"},
{"lat":"21.43409868932025","lng":"-157.788601595756","alt":"143.0002500209957"},
{"lat":"21.43405353253906","lng":"-157.7885919496095","alt":"142.0002265814692"},
{"lat":"21.43400837574283","lng":"-157.7885823034659","alt":"141.0002072397619"},
{"lat":"21.43400837574283","lng":"-157.7885823034659","alt":"141.0002072397619"},
{"lat":"21.43396321893156","lng":"-157.7885726573253","alt":"140.000191995874"},
{"lat":"21.43391806210527","lng":"-157.7885630111876","alt":"139.0001808479428"},
{"lat":"21.43387290526393","lng":"-157.7885533650528","alt":"138.0001737987623"},
{"lat":"21.43382774840756","lng":"-157.7885437189208","alt":"137.0001708464697"},
{"lat":"21.43378259153616","lng":"-157.7885340727919","alt":"136.0001719910651"},
{"lat":"21.43373743464972","lng":"-157.7885244266658","alt":"135.0001772334799"},
{"lat":"21.43369227774824","lng":"-157.7885147805426","alt":"134.000186573714"},
{"lat":"21.43364712083173","lng":"-157.7885051344223","alt":"133.0002000108361"},
{"lat":"21.43360196390019","lng":"-157.788495488305","alt":"132.0002175448462"},
{"lat":"21.43360196390019","lng":"-157.788495488305","alt":"132.0002175448462"},
{"lat":"21.43360196377935","lng":"-157.7885437185861","alt":"132.0002516293898"},
{"lat":"21.43360196364461","lng":"-157.7885919488672","alt":"132.0002896320075"},
{"lat":"21.43360196349598","lng":"-157.7886401791483","alt":"132.0003315545619"},
{"lat":"21.43360196333346","lng":"-157.7886884094293","alt":"132.000377391465"},
{"lat":"21.43360196315705","lng":"-157.7887366397105","alt":"132.0004271483049"},
{"lat":"21.43360196296675","lng":"-157.7887848699916","alt":"132.0004808222875"},
{"lat":"21.43360196276256","lng":"-157.7888331002726","alt":"132.0005384143442"},
{"lat":"21.43360196254448","lng":"-157.7888813305537","alt":"132.0005999235436"},
{"lat":"21.43360196231251","lng":"-157.7889295608348","alt":"132.0006653517485"},
{"lat":"21.43360196231251","lng":"-157.7889295608348","alt":"132.0006653517485"},
{"lat":"21.43364711922725","lng":"-157.78892956109","alt":"132.0006413133815"},
{"lat":"21.43369227614174","lng":"-157.7889295613452","alt":"132.0006212154403"},
{"lat":"21.43373743305599","lng":"-157.7889295616004","alt":"132.0006050588563"},
{"lat":"21.43378258997","lng":"-157.7889295618555","alt":"132.0005928417668"},
{"lat":"21.43382774688376","lng":"-157.7889295621107","alt":"132.0005845660344"},
{"lat":"21.43387290379729","lng":"-157.7889295623659","alt":"132.0005802325904"},
{"lat":"21.43391806071057","lng":"-157.7889295626211","alt":"132.0005798377097"},
{"lat":"21.43396321762361","lng":"-157.7889295628763","alt":"132.000583384186"},
{"lat":"21.4340083745364","lng":"-157.7889295631314","alt":"132.0005908710882"},
{"lat":"21.43405353144895","lng":"-157.7889295633866","alt":"132.0006022993475"},
{"lat":"21.43409868836125","lng":"-157.7889295636418","alt":"132.000617668964"},
{"lat":"21.4341438452733","lng":"-157.788929563897","alt":"132.0006369762123"},
{"lat":"21.43418900218512","lng":"-157.7889295641521","alt":"132.000660228543"},
{"lat":"21.4342341590967","lng":"-157.7889295644074","alt":"132.0006874175742"},
{"lat":"21.43427931600803","lng":"-157.7889295646625","alt":"132.0007185498253"},
{"lat":"21.43432447291912","lng":"-157.7889295649177","alt":"132.0007536206394"},
{"lat":"21.43436962982997","lng":"-157.7889295651729","alt":"132.0007926346734"},
{"lat":"21.43441478674056","lng":"-157.7889295654281","alt":"132.0008355891332"},
{"lat":"21.43445994365091","lng":"-157.7889295656832","alt":"132.0008824830875"},
{"lat":"21.43445994365091","lng":"-157.7889295656832","alt":"132.0008824830875"},
{"lat":"21.43443284964559","lng":"-157.7889006271977","alt":"132.0008141463622"},
{"lat":"21.43440575563517","lng":"-157.7888716887228","alt":"132.0007486399263"},
{"lat":"21.43437866161966","lng":"-157.7888427502587","alt":"132.000685961917"},
{"lat":"21.43435156759907","lng":"-157.7888138118051","alt":"132.0006261132658"},
{"lat":"21.43432447357338","lng":"-157.7887848733623","alt":"132.0005690930411"},
{"lat":"21.43429737954261","lng":"-157.7887559349302","alt":"132.0005149021745"},
{"lat":"21.43427028550675","lng":"-157.7887269965087","alt":"132.0004635406658"},
{"lat":"21.4342431914658","lng":"-157.7886980580979","alt":"132.0004150066525"},
{"lat":"21.43421609741976","lng":"-157.7886691196978","alt":"132.0003693057224"},
{"lat":"21.43418900336863","lng":"-157.7886401813084","alt":"132.000326430425"},
{"lat":"21.43416190931242","lng":"-157.7886112429297","alt":"132.000286385417"},
{"lat":"21.43413481525111","lng":"-157.7885823045616","alt":"132.0002491688356"},
{"lat":"21.43410772118472","lng":"-157.7885533662042","alt":"132.0002147816122"},
{"lat":"21.43408062711323","lng":"-157.7885244278575","alt":"132.000183224678"},
{"lat":"21.43405353303666","lng":"-157.7884954895216","alt":"132.0001544943079"},
{"lat":"21.434026438955","lng":"-157.7884665511962","alt":"132.0001285951585"},
{"lat":"21.43399934486826","lng":"-157.7884376128816","alt":"132.0001055235043"},
{"lat":"21.43397225077642","lng":"-157.7884086745776","alt":"132.0000852812082"},
{"lat":"21.43394515667949","lng":"-157.7883797362843","alt":"132.00006786827"},
{"lat":"21.43391806257748","lng":"-157.7883507980017","alt":"132.0000532846898"},
{"lat":"21.43389096847038","lng":"-157.7883218597298","alt":"132.0000415295362"},
{"lat":"21.43386387435819","lng":"-157.7882929214686","alt":"132.0000326037407"},
{"lat":"21.43383678024091","lng":"-157.788263983218","alt":"132.0000265073031"},
{"lat":"21.43380968611854","lng":"-157.7882350449782","alt":"132.0000232411548"},
{"lat":"21.43378259199108","lng":"-157.788206106749","alt":"132.0000228015706"},
{"lat":"21.43375549785854","lng":"-157.7881771685305","alt":"132.0000251913443"},
{"lat":"21.43372840372091","lng":"-157.7881482303226","alt":"132.0000304114074"},
{"lat":"21.43370130957819","lng":"-157.7881192921255","alt":"132.0000384589657"},
{"lat":"21.43367421543038","lng":"-157.788090353939","alt":"132.0000493377447"}
]


def findOffset(lat,lng,n,e):
    earthRadius=6378137
    dLat = n/earthRadius
    dLngM = earthRadius*math.cos(math.pi*lat/180)
    dLng = e/dLngM
    latOffset = lat + dLat * 180/math.pi
    lngOffset = lng + dLng * 180/math.pi
    return [latOffset,lngOffset]





DRONE_IP = "10.202.0.1"

# casey_ip = "10.202.1.1"
# donatello_ip = "10.202.2.1"
# leonardo_ip = "10.202.3.1"
# michelangelo_ip = "10.202.4.1"
# raphael_ip = "10.202.5.1"
# splinter_ip = "10.202.6.1"
# casey = olympe.Drone(casey_ip)
# donatello = olympe.Drone(donatello_ip)
# leonardo = olympe.Drone(leonardo_ip)
# michelangelo = olympe.Drone(michelangelo_ip)
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
        # lat = event.args["latitude"]
        # lon = event.args["longitude"]
        # c_poi = (lat, lon)
        # poi = (21.371518, -157.71161)
        # print('\n ------->')
        # print('\n ------->')
        # print('\n ------->')
        # meters = haversine(poi, c_poi, unit='m')
        # print(meters)
        # print(meters < 2)
        # print('\n ------->')
        # print('\n ------->')
        # print('\n ------->')

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
        # followerTakeOff(casey)
        # followerTakeOff(donatello)
        # followerTakeOff(leonardo)
        # followerTakeOff(michelangelo)
        # followerTakeOff(raphael)
        # followerTakeOff(splinter)



 
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


    # casey.connect()
    # donatello.connect()
    # leonardo.connect()
    # michelangelo.connect()
    # raphael.connect()
    # splinter.connect()

    every_event_listener.unsubscribe()

    # You can also subscribe/unsubscribe automatically using a with statement
    with FlightListener(drone) as flight_listener:
        for i in range(2):
            assert drone(
                FlyingStateChanged(state="hovering")
                | (TakeOff() & FlyingStateChanged(state="hovering"))
            ).wait().success()

        for poi in route:
            assert drone(
                FlyingStateChanged(state="hovering", _timeout=5)
                >> moveTo(poi["lat"], poi["lng"], 15, MoveTo_Orientation_mode.TO_TARGET, 0.0)
                >> moveToChanged(status="DONE")
            )

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