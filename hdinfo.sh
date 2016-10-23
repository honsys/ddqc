#!/bin/bash
echo 'using lsblk, df, fdisk, and hdparm to provide disk and filt-system info'
echo 'remember, fdisk and hdparm need root/sudo priv. ...'
lsblk
echo ----------------------------------------------
df -hT
echo ----------------------------------------------
fdisk -l | grep /dev  | sort -u
echo ----------------------------------------------
hdparm -i /dev/sda /dev/sdb | egrep -i '/dev|model'
