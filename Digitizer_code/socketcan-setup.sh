#!/bin/bash

# Set up SocketCAN interface

CAN_IFACE=can0
BITRATE=125000

echo "Bringing up $CAN_IFACE interface with bitrate $BITRATE"
sudo ip link set $CAN_IFACE type can bitrate $BITRATE
sudo ip link set $CAN_IFACE up

