#!/bin/bash

# Install pip
sudo apt-get install python3-pip

# Updating pip...
python -m pip install --upgrade pip

# Download virtual env
sudo apt install python3-virtualenv

# Activate virtual env
source myenv/bin/activate

# Updating and installing required modules...
pip install --upgrade tk

# Installation and update complete. Running kalimba_player...
python grader-gui.py
