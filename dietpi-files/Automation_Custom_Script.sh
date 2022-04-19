USER_PASSWORD='$1$W1PuMIz5$4ahL3Uci7yMcQtB0/XmWl/'

## Add new User bart with password and add it to the sudoers file to be able to use sudo without a password
## Password generated using `openssl passwd -crypt supersecurepassword`
useradd -m -p "$USER_PASSWORD" -s /bin/bash -G sudo,gpio,video bart
echo "" | sudo tee /etc/sudoers.d/bart

## Remove login capabilities for user dietpi
usermod -s /usr/sbin/nologin dietpi

## Modify cmdline to be less verbose when booting
## From: https://florianmuller.com/polish-your-raspberry-pi-clean-boot-splash-screen-video-noconsole-zram
echo "consoleblank=1 logo.nologo quiet loglevel=0 plymouth.enable=0 vt.global_cursor_default=0 plymouth.ignore-serial-consoles splash fastboot noatime nodiratime noram" | sudo tee -a /boot/cmdline.txt

## Update APT lists and install required deps
apt-get update
apt-get install -y raspi-gpio bc fbi git python3-dev python3-pip python3-smbus python3-spidev evtest libts-bin device-tree-compiler libraspberrypi-dev build-essential libts0 libavcodec58 libavutil56 libswresample3 libavformat58 libasound2 dbus cmake

## Create bin dir (where all scripts will be stored), copy scripts and set executable bit
mkdir -p /home/bart/bin
mkdir -p /home/bart/videos
cp -R /boot/scripts/* /home/bart/bin
chmod -R a+x /home/bart/

## Copy services files to the services dir, reload daemon and activate services
cp /boot/services/* /etc/systemd/system/
systemctl daemon-reload
systemctl disable getty@tty1
systemctl enable display-init.service
systemctl enable tvbutton.service
systemctl enable tvsplash.service
systemctl enable tvplayer.service

cp /boot/config/locale /etc/default/
cp /boot/config/smb.conf /etc/samba/

## Fetch and compile display driver
## High performance FBCP, does not use the overlay for displays, i2c or spi
cd /opt
git clone https://github.com/juj/fbcp-ili9341.git
cd /opt/fbcp-ili9341
mkdir /opt/fbcp-ili9341/build
cd /opt/fbcp-ili9341/build
cmake -DADAFRUIT_HX8357D_PITFT=ON -DSPI_BUS_CLOCK_DIVISOR=8 -DARMV6Z=ON -DSINGLE_CORE_BOARD=ON -DSTATISTICS=0 .. && make -j
cp /opt/fbcp-ili9341/build/fbcp-ili9341 /home/bart/bin/

## Install omx player and support libraries
## None of this is available in the repos of RaspberryOS Bullseye
mkdir -p /opt/omxplayer
cd /opt/omxplayer
wget http://archive.raspberrypi.org/debian/pool/main/o/omxplayer/omxplayer_20190723+gitf543a0d-1+bullseye_armhf.deb
dpkg --install omxplayer_20190723+gitf543a0d-1+bullseye_armhf.deb
git clone https://github.com/hitesh83/pwomxplayer-support.git
cd pwomxplayer-support/
sh ./install_lib.sh

