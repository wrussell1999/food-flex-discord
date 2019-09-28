#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo apt-get install libopenjp2-7
sudo apt install libtiff5
sudo apt install ttf-mscorefonts-installer