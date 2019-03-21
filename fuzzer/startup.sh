#!/usr/bin/env bash

trap "kill 0" EXIT

cd ~/redis-stable/src
./redis-server ../redis.conf &
sleep 1
./redis-cli

wait
