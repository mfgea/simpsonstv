
The original project was created by the user buba447. Manual is [here](https://withrow.io/simpsons-tv-build-guide) and source is [here](https://github.com/buba447/simpsonstv). Original 3D model is [here](https://www.thingiverse.com/thing:4943159)

Second user created new 3D model for THE 3.5" Adafruit PiTFT DISPLAY. Original 3D model is [here](https://www.thingiverse.com/thing:4951026)

Third user created a great guide for assembly [here](https://www.instructables.com/The-Simpsons-TV-35-Screen-Version/)

Fourth user johnyHV created what would become the base for this repo [here](https://github.com/johnyHV/simpsonstv)

Fifth user (me, mfgea) took all the above and built a mix of hardware and some new software.

---
# Manual Content
1. [ My changes ](#my_changes)
2. [ HW construction ](#hw_construction)
3. [ Instalation ](#instalation)
4. [ How to use ](#howtouse)

---
<a name="my_changes"></a>
# My changes

My changes, all tested on the RPI ZERO:
- Created a semi-autoated installation script based on DietPi
- Compiled (automatically) omxPlayer (not available through apt-get)
- Compiled (automatically) fbcp-ili9341 (awesome render speed, but lack of touchscreen support)
- display-on & display-off console commands
- Splash screen
- New Player script.
- New buttons script (supports rotary encoder, with "next video" and "rewind 15 secs" features)
- Separate partition for videos (FAT32)
- Videos partition accessible through Samba

# TODO
- Move buttons and player to the same app
- Auto updater script
- Support "channels" (different folders in the videos partition, rotary encoder would change channels)
- Freeze the root partition; without writes to the sd you could just unplug the RPi without risk
- Autohotspot: When there's no wifi network available for connection, put up a Hotspot. The admin can then connect to it and configure Wifi credentials. Useful when taking the tv on a trip.

---
<a name="hw_construction"></a>
# HW construction

Audio amplifier
```
AUDIO AMPLIFIER SIGNAL -> GPIO19 (through sound filter circuit)
AUDIO AMPLIFIER POWER -> +5V
AUDIO AMPLIFIER GROUND -> GND
```
Buttons
```
ROTARY ENCODER CLICK -> GPI26
ROTARY ENCODER A -> 27
ROTARY ENCODER B -> 22
```

---

<a name="instalation"></a>
# Instalation


Instructions document is WIP and can be found at [./dietpi-draft-script.md]

---
<a name="howtouse"></a>
# How to use

***TODO***
