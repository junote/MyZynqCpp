#!/bin/bash

#parted /dev/sda print
#parted /dev/sda rm 1
#parted /dev/sda mklabel gpt
#parted /dev/sda mkpart primary 0 100%
#Ignore
parted /dev/sda <<ESXU
        rm 1
        mklabel gpt
        ignore
        mkpart primary 0 100%
        quit
ESXU
mkfs.ext4 /dev/sda1
mkdir /mnt/sda
mount  /dev/sda1 /mnt/sda
scp -r lab@10.13.11.63:/home/lab/chm1r/images/* /mnt/sda/
sync
sleep 1
umount /mnt/sda
sleep 1
i2cset -f -y 1 0x71 0xa0 0xaa