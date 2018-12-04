#!/bin/sh

path=$(pwd)

# set crontab to run it every boot
echo "@reboot root /usr/bin/python $path/slave.py > /dev/null 2>&1" >> /etc/crontab
# start it
nohup python $path/slave.py > /dev/null 2>&1 &

