Audok
======
Audok is a simple linux music player with streamripper and converter support. Audok is written in python3, the graphical user interface uses gtk. Audok is a free software under the GPL license.


Version
======
Current Version is 0.7.0


Requirements
======
- pipewire
- ffmpeg
- lame
- youtube-dl
- streamripper


Installation
======

wget https://github.com/kalibari/audok/archive/refs/heads/master.zip<br/>
unzip master.zip<br/>
sudo mv audok-master /opt/audok<br/>
sudo cp /opt/audok/share/applications/audok.desktop /usr/share/applications/<br/>
sudo cp /opt/audok/share/icons/hicolor/256x256/apps/org.audok.Audok.png /usr/share/icons/hicolor/256x256/apps/<br/>
sudo desktop-file-install /usr/share/applications/audok.desktop<br/>


Deinstallation
======
sudo rm -rf /opt/audok/
sudo rm /usr/share/icons/hicolor/256x256/apps/org.audok.Audok.png
sudo rm /usr/share/applications/audok.desktop


Description
======
Audok provides the following features:
- play mp3,wav,flac files
- youtube-dl gui (mp3 downloader)
- streamripper gui
- record wav files
- covert wav,ts,flac,mp4 to mp3
- covert wav to flac
