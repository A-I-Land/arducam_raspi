#!bin/bash

git reset --hard
git pull
gnome-terminal -e "python3 /home/ailand/handwagon/handwagon/handdevice.py" 