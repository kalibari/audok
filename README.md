Audok
======
Audok is a simple linux music player with streamripper and converter support. Audok is written in python3, the graphical user interface uses gtk. Audok is a free software under the GPL license.

![Screenshot](https://github.com/kalibari/audok/blob/master/audok/screenshot.png)


Version
======
Current Version is 1.0.26


Requirements
======
- pulseaudio or pipewire
- ffmpeg
- youtube-dl
- streamripper
- gtk4
- python gstreamer, python systemd
- gstreamer plugins base, gstreamer plugins bad


Installation
======
wget https://github.com/kalibari/audok/archive/refs/heads/master.zip<br/>
unzip master.zip<br/>
cd audok-master<br/>
sudo make install all PREFIX=/usr APPDIR=/opt/audok<br/>


Deinstallation
======
sudo make uninstall PREFIX=/usr APPDIR=/opt/audok<br/>


Installation via Flatpak
======
sudo flatpak install flathub com.github.kalibari.audok<br/>


Deinstallation via Flatpak
======
sudo flatpak remove flathub com.github.kalibari.audok<br/>



Description
======
Audok provides the following features:
- play mp3,wav,flac files
- youtube-dl support (mp3 downloader)
- streamripper support
- record wav files via pulseaudio or pipewire
- covert wav,aac,flac,flv,webm to mp3
- covert wav,aac,mp3,flv,webm to flac
