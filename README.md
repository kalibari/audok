Audok
======
Audok is a simple linux music player with streamripper and converter support. Audok is written in python3, the graphical user interface uses gtk. Audok is a free software under the GPL license.

![Screenshot](https://github.com/kalibari/audok/blob/master/audok/screenshot.png)


Version
======
Current Version is 0.7.9


Requirements
======
- pipewire
- ffmpeg
- youtube-dl
- streamripper


Installation
======
sudo apt install --no-install-recommends python3-gst-1.0 python3-cairo<br/>
sudo apt install --no-install-recommends ffmpeg flac lame<br/>
sudo apt install --no-install-recommends pipewire<br/>
sudo apt install --no-install-recommends youtube-dl<br/>
wget https://github.com/kalibari/audok/archive/refs/heads/master.zip<br/>
unzip master.zip<br/>
cd audok-master<br/>
sudo make install PREFIX=/usr APPDIR=/opt/audok<br/>


Deinstallation
======
sudo make uninstall PREFIX=/usr APPDIR=/opt/audok<br/>


Description
======
Audok provides the following features:
- play mp3,wav,flac files
- youtube-dl support (mp3 downloader)
- streamripper support
- record wav files
- covert wav,ts,flac,mp4 to mp3
- covert wav to flac
