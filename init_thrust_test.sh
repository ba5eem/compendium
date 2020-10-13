#!/bin/bash



#V=1 sphinx /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=leonardo::stolen_interface=::simple_front_cam=false /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=raphael::stolen_interface=::with_front_cam=false /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=donatello::stolen_interface=::with_front_cam=false /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=michelangelo::stolen_interface=::with_front_cam=false /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=splinter::stolen_interface=::with_front_cam=false /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=april::stolen_interface=::with_front_cam=false /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=casey::stolen_interface=::with_front_cam=false::pose="0 0 0 1 0 0 2 0 0 3 0 0 4 0 0 5 0 0 6 0 0"



#V=1 sphinx /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=drone1::stolen_interface=::simple_front_cam=true /opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone::name=drone2::stolen_interface=::pose="5 0 0.2 0 0 0"::with_front_cam=false

V=1 sphinx april.drone::stolen_interface=::simple_front_cam=false casey.drone::stolen_interface=::simple_front_cam=false

