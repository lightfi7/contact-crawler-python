#!/bin/bash

# Update package lists
sudo apt update

# Install prerequisites
sudo apt install -y software-properties-common

# Add deadsnakes PPA to your system's sources list
sudo add-apt-repository -y ppa:deadsnakes/ppa

# Once the repository is enabled, install Python 3.10
sudo apt install -y python3.10

# Verify the installation
python3.10 --version

# Install pip for Python 3.10
sudo apt install -y python3.10-distutils

sudo apt install -y python3-pip

# Optionally, set Python 3.10 as the default Python 3 version
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
sudo update-alternatives --config python3

sudo pip install -r requirements.txt
sudo python3 main.py