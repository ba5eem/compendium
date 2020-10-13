#!/bin/bash

PATH=/opt/parrot-sphinx/usr/share/sphinx/drones/anafi4k.drone

V=1 sphinx $PATH::name=leonardo::stolen_interface=::simple_front_cam=false $PATH::name=raphael::stolen_interface=::with_front_cam=false $PATH::name=donatello::stolen_interface=::with_front_cam=false $PATH::name=michelangelo::stolen_interface=::with_front_cam=false $PATH::name=splinter::stolen_interface=::with_front_cam=false $PATH::name=april::stolen_interface=::with_front_cam=false $PATH::name=casey::stolen_interface=::with_front_cam=false::pose="0 0 0 1 0 0 2 0 0 3 0 0 4 0 0 5 0 0 6 0 0"

