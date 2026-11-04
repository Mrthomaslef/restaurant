#!/bin/bash
cd "/Users/thomaslefevre/.t3/projects/restaurant" || exit 1
open "http://localhost:8790"
python3 server.py
