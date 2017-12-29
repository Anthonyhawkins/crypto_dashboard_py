#!/bin/bash
echo "PREVIOUS"
cat previous.txt
echo "NOW"
../../crypto_dashboard/Scripts/python.exe dashboard.py | tee previous.txt



