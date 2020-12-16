#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:`pwd`"
cd ..
python3 -m ZeNo > log &
