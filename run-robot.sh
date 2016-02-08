#!/usr/bin/env bash
#nohup cpulimit -l 10 ./robot.py video-process >& robot.log &
nohup cpulimit -l 10 ./robot.py player-activity >& robot.log &
