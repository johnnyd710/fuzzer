#!/bin/bash

# Set up SocketCAN interface and log CAN messages to file using candump

CANDUMP=candump
CAN_IFACE=can0
#BITRATE=125000
CAN_LOG=/Digitizer/disk1/$(date +%F-%H%M)-candump.log

POWERTRACE_LOG=CAN-and-powertrace
CAPTURE_LENGTH=60      # in seconds
SAMPLE_RATE=10		# in MSPS
INPUT_RANGE=400mV

if ! [ -x "$(command -v $CANDUMP)" ]; then
	echo "Error: '$CANDUMP' binary not found. Ensure that the 'can-utils' package is installed" >&2
	exit 1
fi

if [ "$#" -gt 0 ]; then
	CAN_IFACE="$1"
fi

#echo "Setting up $CAN_IFACE interface"
#sudo ip link set $CAN_IFACE type can bitrate $BITRATE
#sudo ip link set $CAN_IFACE up

#echo "Starting $CANDUMP in background"
#$CANDUMP -ta -x -L $CAN_IFACE > $CAN_LOG &
#CANDUMP_PID=$!

echo "Starting digitizer capture at $(date +%s)"
./acquire_to_disk $SAMPLE_RATE $INPUT_RANGE $CAPTURE_LENGTH $POWERTRACE_LOG 2
#kill $CANDUMP_PID

