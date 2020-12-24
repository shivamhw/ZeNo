#!/bin/bash 


if [[ -e process.id ]]; then
  kill `cat process.id`
  rm process.id
  echo "Stopped"
  else
    pkill python3*
    echo "Stopped forcefully"
    fi