Audok
======
Audok is a simple linux music player with streamripper and converter support. Audok is written in python, the graphical user interface uses python-wx. Audok is a free software under the GPL license.


Version
======
Current Version is 0.6.4


Requirements
======
- pulseaudio-utils
- ffmpeg
- flac
- lame
- youtube-dl
- streamripper
- python-wxgtk3.0
- python-wxgtk-media3.0
- libwxgtk-media3.0-0v5


Installation
======

Install Dependencies (for Ubuntu + Debian):<br/>
apt-get install unzip pulseaudio-utils ffmpeg flac lame youtube-dl streamripper python-wxgtk3.0 python-wxgtk-media3.0 libwxgtk-media3.0-0v5<br/>

Install Audok:<br/>
-> download Audok as zip<br/>
unzip audok-master.zip<br/>
mv audok-master/ /opt/audok<br/>
chmod 0770 /opt/audok/audok<br/>
cp /opt/audok/audok.desktop /usr/share/applications/<br/>
desktop-file-install /usr/share/applications/audok.desktop<br/>


Description
======
Audok provides the following features:
- play mp3,wav,flac files
- youtube-dl gui (mp3 download)
- pulseaudio dlna gui
- streamripper gui
- record wav files
- covert wav,ts,flac,mp4 to mp3
- covert wav to flac
