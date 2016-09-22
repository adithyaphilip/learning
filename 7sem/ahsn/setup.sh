#!/bin/sh
# need to be sudo script {device} {essid} {key} {channel} {ip}
sudo ifconfig $1 down 
sudo iwconfig $1 mode ad-hoc
sudo iwconfig $1 channel $4
sudo iwconfig $1 essid $2
sudo iwconfig $1 key $3
sudo ifconfig $1 $5

