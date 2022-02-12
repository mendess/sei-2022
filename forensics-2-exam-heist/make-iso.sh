#!/usr/bin/env bash

echo() {
    command echo -e '\e[1;32m===>\e[0m' "$@"
}

uid=$(VBoxManage list hdds | grep -B4 kai | head -1 | cut -d: -f2 | xargs)

echo main image UUID: "$uid"

echo cloning original image as vmdk
clone_uid=$(VBoxManage clonehd disk "$uid" disk.vmdk --format VMDK | tee /dev/tty | tail -1 | cut -d: -f2 | xargs)

echo converting to raw
qemu-img convert -f vmdk disk.vmdk -O raw disk.raw

echo creating loop device
loopdev=$(sudo losetup --show -f disk.raw)
echo loop device "$loopdev" created

echo creating partitions
sudo kpartx -v -a "$loopdev"

part=$(lsblk --json | jq '.blockdevices[]|select(.name == "loop0")|.children[].name' -r|tail -1)
echo partition is "$part"

#echo making mount point
#mkdir -vp mnt-point

#echo mounting clone
#sudo mount -v "/dev/mapper/$part" mnt-point

echo creating iso
sudo dd if="/dev/mapper/$part" of=disk.iso status=progress

printf "\n"
read -r -p 'PRESS ENTER TO CLEAN UP'
printf "\n"

# echo unmounting
# umount -v mnt-point

# echo removing directory
# rmdir -v mnt-point

echo removing partitions
sudo kpartx -v -d "$loopdev"

echo removing loop device "$loopdev"
sudo losetup -v -d "$loopdev"

echo deleting raw clone
rm -v disk.raw

echo deleting vmdk clone
VBoxManage closemedium disk "$clone_uid" --delete

echo compacting disk
tar vcfJ disk.tar.xz disk.iso
