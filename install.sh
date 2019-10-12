#!/bin/bash

#-> Make sure we don't run as root
if (( EUID == 0 )); then
	echo 'Please run without sudo!' 1>&2
	exit 1
fi

#-> Update packags and install python and pip
sudo apt update
sudo apt install -y python3 python3-pip

#-> Install ipython and pyserial package
sudo -H pip3 install -U ipython pyserial
