#!/bin/bash
lsblk
echo ----------------------------------------------
fdisk -l | grep /dev  | sort -u
echo ----------------------------------------------
df -hT
echo ----------------------------------------------
hdparm -i /dev/sda /dev/sdb | egrep -i '/dev|model'
