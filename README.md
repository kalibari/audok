Audok
======
Audok is a simple linux music player with streamripper and converter support. Audok is written in python3, the graphical user interface uses gtk. Audok is a free software under the GPL license.

![Screenshot](https://github.com/kalibari/audok/blob/master/audok/screenshot.png)


Version
======
Current Version is 1.0.9


Requirements
======
- pipewire
- ffmpeg
- youtube-dl
- streamripper


Installation
======
Dependencies Debian:<br/>
sudo apt install --no-install-recommends python3-gst-1.0 python3-cairo<br/>
sudo apt install --no-install-recommends ffmpeg flac lame wget unzip<br/>
sudo apt install --no-install-recommends libgstreamer-plugins-base1.0-0 libgstreamer-plugins-bad1.0-0<br/>
sudo apt install --no-install-recommends pipewire<br/>
sudo apt install --no-install-recommends youtube-dl<br/>
sudo apt install --no-install-recommends streamripper<br/>

Dependencies Fedora:<br/>
sudo dnf install python3-gstreamer1 python3-cairo<br/>
sudo dnf install ffmpeg flac lame wget unzip<br/>
sudo dnf install gstreamer1-plugins-base gstreamer1-plugins-bad-free<br/>
sudo dnf install pipewire<br/>
sudo dnf install youtube-dl<br/>
sudo dnf install streamripper<br/>

Dependencies Manjaro:<br/>
sudo pamac install python-cairo gst-python<br/>
sudo pamac install ffmpeg flac lame wget unzip<br/>
sudo pamac install gst-plugins-base-libs gst-plugins-bad-libs<br/>
sudo pamac install pipewire-alsa<br/>
sudo pamac install youtube-dl<br/>
sudo pamac build streamripper<br/>



wget https://github.com/kalibari/audok/archive/refs/heads/master.zip<br/>
unzip master.zip<br/>
cd audok-master<br/>
sudo make install all PREFIX=/usr APPDIR=/opt/audok<br/>


Deinstallation
======
sudo make uninstall PREFIX=/usr APPDIR=/opt/audok<br/>


Description
======
Audok provides the following features:
- play mp3,wav,flac files
- youtube-dl support (mp3 downloader)
- streamripper support
- record wav files via pipewire
- covert wav,aac,flac,flv,webm to mp3
- covert wav,aac,mp3,flv,webm to flac
