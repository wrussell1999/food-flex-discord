#!/bin/bash
sudo apt-get install build-essential python3-dev python3-venv libfreetype6-dev libjpeg-dev zlib1g-dev
python3 -m venv .venv
source .venv/bin/activate
pip install wheel
pip install -r requirements.txt
