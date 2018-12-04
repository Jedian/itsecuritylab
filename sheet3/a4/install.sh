#!/bin/sh

make
echo "insmod rootkit.ko $@"
