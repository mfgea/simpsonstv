Notes: This is in a very draft state. These are the steps, but they lack all kinds of explanaition. Next step is to convert this into a readable document.

# Burn DietPi in a fresh SD card (32/64Gb)
Using Balena Etcher

# Modify Wifi Settings
cp dietpi-files/dietpi-wifi.txt.template dietpi-files/dietpi-wifi.txt
nano dietpi-files/dietpi-wifi.txt

# Modify default user password
using `openssl passwd -crypt supersecurepassword` generate a new password and copy/paste it in Automation_Custom_Script.sh

# Copy files to the card
cp -R dietpi-files/* /Volume/NONAME/

# Run the installation in the rpi
It will take a while.
While installing you can use user:pass dietpi:dietpi. Once the script is finished, you can use user:pass bart:whateverpasswordsetearlier

After the installation is finished, you should have everything running, but no videos, so you'll see a static splash screen.
SSH is available.

At this point you could scp a video like:
```
scp myvideo.mp4 bart@<ip>:./videos/
```

# Reduce partition and create new one
Move the sd to a linux system (or a virtual machine with access to the raw usb device).

Find the device using `fdisk -l`

Assuming the device is /dev/sdb and we want a 4G main partition:
Resize the partition: `resize2fs -f /dev/sdb 4G`

run `cfdisk /dev/sdb`
Arrow down to select the second partition sdb2 and go to "Resize", enter 4G and then hit "Write"

Then select the free space, hit "New", hit enter to confirm the size (all available) and hit "primary". Then goto Type and select "b W95 FAT32". Hit "Write" type "yes" and then "Quit".

`fdisk -l` should show the new sdb3 partition.

Format it as Fat32 using `mkfs.vfat -F 32 -L TVVIDEOS /dev/sdb3`

Now it's a good time to copy files to the newly created partition (will be available to mount)

# Automount vfat to the videos dir

Find the PARTUUID using `blkid`. Should be the 3rd partition, like "/dev/mmcblk0p3". The PARTUUID looks like "9282c8f4-03"

echo "PARTUUID=9282c8f4-03 /home/bart/videos vfat user,uid=1001,gid=1001 0 2" >> /etc/fstab

# Freeze root partition
