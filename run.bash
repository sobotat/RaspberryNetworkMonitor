#!/bin/bash
nohup sudo python -u networkMonitor.py > "crash.log" 2>&1 < /dev/null &
echo "networkMonitor.py was started"