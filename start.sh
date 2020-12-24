#!/bin/bash


export PYTHONPATH="${PYTHONPATH}:`pwd`"
cd ..
python3 -m ZeNo > ZeNo/log 2> ZeNo/err.log &
echo $! > ZeNo/process.id
