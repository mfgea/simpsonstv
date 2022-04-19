TV Build URLs:
- Original: https://withrow.io/simpsons-tv-build-guide
- Another version (better sound): https://www.instructables.com/The-Simpsons-TV-35-Screen-Version/
- Improved Audio circuit (like Rpi1, lowpass, highpass filters): https://hackaday.com/2018/07/13/behind-the-pin-how-the-raspberry-pi-gets-its-audio/

DietPi:
- https://dietpi.com/docs/

Display:
- Driver (non official, faster, does not support touch): https://github.com/juj/fbcp-ili9341

Rotary Encoder:
- Rotary encoder in python: https://github.com/nstansby/rpi-rotary-encoder-python

Optimization:
- Reduce sd partition: https://forums.raspberrypi.com/viewtopic.php?t=60161#p450676
- Remount-readonly: https://medium.com/@andreas.schallwig/how-to-make-your-raspberry-pi-file-system-read-only-raspbian-stretch-80c0f7be7353
- Autohotspot: https://www.thedigitalpictureframe.com/connect-to-raspberry-pi-picture-frame-even-if-your-wifi-connection-is-down/
- No BootLogo and ZRAM Swap: https://florianmuller.com/polish-your-raspberry-pi-clean-boot-splash-screen-video-noconsole-zram
- Splash: https://yingtongli.me/blog/2016/12/21/splash.html#:~:text=Set%20up%20the%20splash%20screen&text=Install%20fbi%2C%20the%20framebuffer%20image,apt%20install%20fbi%20as%20root.&text=Replace%20%2Fopt%2Fsplash.,to%20display%20the%20image%20on.
- Systemd service 1: https://www.thedigitalpictureframe.com/ultimate-guide-systemd-autostart-scripts-raspberry-pi/
- Systemd service 2: https://github.com/zanppa/fbcp-switcher/blob/master/etc/systemd/system/fbcp.service

Cool things:
- Fade video: https://forum.recalbox.com/topic/20408/recalbox-6-1-intro-videos-how-can-i-put-a-fade-out-in-my-intro-video
- OMXPlayer DBus wrapper: https://github.com/willprice/python-omxplayer-wrapper + https://python-omxplayer-wrapper.readthedocs.io/en/latest/omxplayer/

Helper URLs:
- https://pinout.xyz/
    Check the pinout for the rpi board

- http://www.sengpielaudio.com/calculator-paralresist.htm
    Resistor Calculator (for audio circuit)

- https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README
    Rpi overlays docs

- https://www.raspberrypi.com/documentation/computers/os.html#gpio-and-the-40-pin-header
    Rpi OS docs on GPIO