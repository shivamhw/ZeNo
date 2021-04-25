#!/bin/bash



echo "reset called"
if [[ $# -eq 0 ]]; then
  ./stop.sh
  ./start.sh
else
  cd $1
  ./stop.sh
  ./start.sh
  fi