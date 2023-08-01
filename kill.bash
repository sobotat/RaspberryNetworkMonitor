#!/bin/bash
ps -ef | grep "networkMonitor.py" | grep -v grep | awk '{print $2}' | xargs kill
echo "process "networkMonitor.py" killed"
