#!/bin/bash

sudo apt-get update
sudo apt-get install shc
sudo apt-get install gcc

sudo shc -S -f restart_mysql.sh
sudo chmod u+s restart_mysql.sh.x
