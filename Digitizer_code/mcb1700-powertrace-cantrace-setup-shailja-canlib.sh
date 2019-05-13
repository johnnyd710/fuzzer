#!/bin/bash

# Set up SocketCAN interface and log CAN messages to file using candump

BITRATE=125000
CAN_LOG=/Digitizer/disk1/$(date +%F-%H%M)-candump.log

POWERTRACE_LOG=CAN-and-powertrace
CAPTURE_LENGTH=60       # in seconds
SAMPLE_RATE=10		# in MSPS
INPUT_RANGE=400mV

echo "Starting logger.py in background"
python3 ~/.local/lib/python3.5/site-packages/can/logger.py -i kvaser -c 0 -b $BITRATE > $CAN_LOG &
CANDUMP_PID=$!

echo "Starting digitizer capture at $(date +%s)"
./acquire_to_disk $SAMPLE_RATE $INPUT_RANGE $CAPTURE_LENGTH $POWERTRACE_LOG 2
kill $CANDUMP_PID

