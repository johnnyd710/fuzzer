#!/usr/bin/env bash

# LAUNCH DIGITIZER TO CAPTURE TRACE -- WHERE?
~/commands/acquire_to_disk 10 400 filename 2

# split signal
~/commands/split-channels /Digitizer/captured-data/ filename

# bin 2 txt
~/commands/bin2txt 1 /Digitizer/captured-data/ filename?-channelA 10 400mV
~/commands/bin2txt 1 /Digitizer/captured-data/ filename?-channelB 10 400mV

# cut signal to just the relevant trace with cut.py which will stream data to redis
~/commands/cut.py filename