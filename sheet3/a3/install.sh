#!/bin/sh

path=$(pwd)

echo "@reboot root /usr/bin/python $path/slave.py > /dev/null 2>&1" >> /etc/crontab
nohup python $path/slave.py > /dev/null 2>&1 &

