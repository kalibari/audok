#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import socket
import subprocess
import pwd
import xml.etree.ElementTree
app_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, app_path)
import main
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GLib', '2.0')
from gi.repository import GLib


def startup_notification_workaround():
   # https://specifications.freedesktop.org/startup-notification-spec/startup-notification-0.1.txt
   Gdk.notify_startup_complete()



if __name__ == '__main__':

   stationlist=[]
   playlist=[]

   config={}

   config['debug']=0
   if sys.stdin.isatty():
      config['debug']=1

   config['name'] = 'audok'
   config['version'] = '1.0.4'

   config['app_path'] = app_path

   config['play_num'] = 0

   config['stationlist_changed'] = False


   config['bin_youtubedl'] = 'youtube-dl'
   config['bin_streamripper'] = 'streamripper'
   config['bin_ffmpeg'] = 'ffmpeg'
   config['bin_pwcli'] = 'pw-cli'
   config['bin_pwrecord'] = 'pw-record'
   config['bin_nice'] = 'nice'

   config['supported_audio_files'] = ['.mp3','.ogg','.aac','.flac','.midi','.mp4','.mpeg','.wma','.asx','.wav','.mpegurl']


   settings={}

   # setup default settings
   settings['config_path'] = '%s/audok' % GLib.get_user_config_dir()
   if not settings['config_path']:
      settings['config_path']=os.getenv("HOME")

   settings['music_path'] = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_MUSIC)
   if not settings['music_path']:
      settings['music_path']=os.getenv("HOME")

   settings['filename_settings'] = 'settings.xml'
   settings['filename_stations'] = 'stations.xml'
   settings['filename_ipcport'] = 'ipc_port'

   settings['directory_new'] = 'New'
   settings['directory_old'] = 'Old'
   settings['directory_str'] = 'Streamripper'

   settings['checkbutton_new'] = 0
   settings['checkbutton_old'] = 0
   settings['checkbutton_str'] = 0

   settings['size_x'] = 1000
   settings['size_y'] = 500
   settings['position_x'] = 0
   settings['position_y'] = 0

   settings['pwrecord_default_filename'] = 'pwrecord.wav'
   settings['pwrecord_default'] = ''
   settings['choice_pwrecord_device'] = ['']

   settings['play_time'] = 0
   settings['choice_play_time'] = ['0','20','35','50','65']

   settings['random_time_min'] = 0
   settings['random_time_max'] = 0
   settings['choice_random_time'] = ['0','10-30','30-50','50-70','70-90']

   settings['bitrate'] = '192k'
   settings['choice_bitrate'] = ['128k','192k','224k','320k']

   settings['playlist_filename'] = 'playlist.m3u'


   # generate a new settings.xml
   settings['min_version'] = '0.8.6'
   settings['ipc_port'] = 10001


   # read the settings file
   path = settings['config_path']
   filename = settings['filename_settings']


   if config['debug']==1:
      print ('def main - name: %s version: %s'  % (config['name'],config['version']))


   if os.path.exists(path + '/' + filename):

      bak_old_version=False

      tree = xml.etree.ElementTree.parse(path + '/' + filename)
      root = tree.getroot()

      try:
         for child in root:
            if child.text is not None and child.tag is not None:

               element = child.tag.strip()
               value = child.text
               try:
                  value = int(value)
               except:
                  if value.startswith('[') and value.endswith(']'):
                     value=value.replace('[','',1)
                     value=value.replace(']','',1)
                     if ',' in value:
                        value=value.split(',')
                     else:
                        value=[value]
               settings[element]=value
      except:
         bak_old_version=True


      old_version=0
      if 'old_version' in settings:
         old_version=int(settings['old_version'].replace('.',''))


      min_version=0
      if 'min_version' in settings:
         min_version=int(settings['min_version'].replace('.',''))


      if old_version < min_version:
         bak_old_version=True


      if config['debug']==1:
         if bak_old_version==True:
            print ('def main - old version: %s < min version: %s' % (old_version,min_version))
         else:
            print ('def main - old version: %s >= min version: %s' % (old_version,min_version))


      if bak_old_version==True:

         path = settings['config_path']
         filename = settings['filename_settings']

         for i in range(1,100):
            if not os.path.exists('%s/%s.%s.bak' % (path,filename,i)):
               os.rename('%s/%s' % (path,filename), '%s/%s.%s.bak' % (path,filename,i))
               break



   settings['old_version']=config['version']

   if config['debug']==1:
      print ('def main - app_path: %s' % config['app_path'])
      print ('def main - cwd: %s' % os.getcwd())
      print ('def main - music path: %s' % settings['music_path'])
      print ('def main - config path: %s' % settings['config_path'])
      print ('def main - directories new: %s old: %s streamripper: %s' % (settings['directory_new'],settings['directory_old'],settings['directory_str']))
      print ('def main - playlist: %s' % playlist)




   if len(sys.argv)>=2:

      checkfile = sys.argv[1]

      if checkfile.endswith('.m3u'):
         m3ufiles = []
         with open(checkfile,'r') as f:
            m3ufiles = f.readlines()
         for item in m3ufiles:
            item=item.strip()
            if os.path.isfile(item):
               playlist.extend([item])

      else:
         for item in config['supported_audio_files']:
            if checkfile.endswith(item):
               playlist = [checkfile]
               break




   # if audok is running + playlist
   if os.path.exists('%s/%s' % (settings['config_path'],settings['filename_ipcport'])):

      # cat /tmp/audok/audok_port
      ipc_port=settings['ipc_port']
      with open('%s/%s' % (settings['config_path'],settings['filename_ipcport']),'r') as f:
         port = f.read()
         if port:
            ipc_port = int(port)
      

      send_file=''
      if config['play_num'] < len(playlist):
         send_file='play_new_file=%s' % playlist[config['play_num']]


      if config['debug']==1:
         print ('def main - name: %s is already running - try send file: %s via socket port: %s' % (config['name'],send_file,ipc_port))

      if not send_file:
         os.remove('%s/%s' % (settings['config_path'],settings['filename_ipcport']))
         sys.exit(0)
      else:
         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', ipc_port))
            sock.sendall(send_file.encode())
         except:
            os.remove('%s/%s' % (settings['config_path'],settings['filename_ipcport']))
         else:
            startup_notification_workaround()
            sys.exit(0)
         finally:
            sock.close()


   if config['debug']==1:
      print ('def main - name: %s try to start -> Music_Admin_Start' % config['name'])



   if os.path.exists('%s/%s' % (settings['config_path'],settings['filename_stations'])):

      try:
         tree = xml.etree.ElementTree.parse('%s/%s' % (settings['config_path'],settings['filename_stations']))
         root = tree.getroot()
         for child in root:
            try:
               child[0].text.strip()
               child[1].text.strip()
               child[2].text.strip()
            except:
               pass

            stationlist.extend([[child[0].text,child[1].text,child[2].text]])

      except Exception as e:
         if config['debug']==1:
            print ('def main - wrong format stations.xml -> backup error: %s' % e)
         for i in range(1,100):
            if not os.path.exists('%s/%s.%s.bak' % (settings['config_path'],settings['filename_stations'],i)):
               os.rename('%s/%s' % (settings['config_path'],settings['filename_stations']), '%s/%s.%s.bak' % (settings['config_path'],settings['filename_stations'],i))
               break
         stationlist = []



   if not stationlist:

      stationlist = [['Alternative', 'Radio freeFM Ulm', 'http://stream.freefm.de:7000/Studio'],
                     ['Alternative', 'Radio FM 4 at', 'https://orf-live.ors-shoutcast.at/fm4-q2a'],
                     ['Alternative', 'Zeilsteen Radio', 'http://live.zeilsteen.com:80'],

                     ['Mix', '1.FM - Gorilla FM', 'http://185.33.21.112:80/gorillafm_128'],

                     ['Electro', 'radio Top 40 Weimar Clubsound', 'http://antenne-th.divicon-stream.net/antth_top40electro_JlSz-mp3-192?sABC=58p2q700%230%232pn8rp1qoro76pp9n0r46nspn714s714%23fgernz.enqvbgbc40.qr'],
                     ['Electro', 'Sunshine Live','http://sunshinelive.hoerradar.de/sunshinelive-live-mp3-hq'],

                     ['Chipc_serverarts', 'radio Top 40 Weimar Charts', 'http://antenne-th.divicon-stream.net/antth_top40char_0f6x-mp3-192?sABC=58p2q6s8%230%232pn8rp1qoro76pp9n0r46nspn714s714%23fgernz.enqvbgbc40.qr'],
                     ['Charts', 'Top 100 Station','http://www.top100station.de/switch/r3472.pls'],
                     ['Charts', 'radio Top 40 Weimar Live', 'http://antenne-th.divicon-stream.net/antth_top40live_SeJx-mp3-192?sABC=58p2q6rq%230%232pn8rp1qoro76pp9n0r46nspn714s714%23fgernz.enqvbgbc40.qr'],
                     ['Charts', '"TOP 20" Radio', 'http://listen.radionomy.com:80/-TOP20-Radio'],

                     ['80s', '80s New Wave','http://yp.shoutcast.com/sbin/tunein-station.pls?id=99180471'],

                     ['Pop', 'Pophits Station', 'http://yp.shoutcast.com/sbin/tunein-station.pls?id=99183408'],
                     ['Pop', 'Bailiwick Radio_00s', 'http://listen.radionomy.com:80/BailiwickRadio-00s'],
                     ['Pop', 'Antenne 1','http://stream.antenne1.de/stream1/livestream.mp3'],
                     ['Pop', 'Antenne Bayern Fresh4You', 'http://mp3channels.webradio.antenne.de/fresh'],

                     ['Rap', 'WHOA UK!!!!', 'http://listen.radionomy.com:80/WHOAUK----'],

                     ['None', '', ''],
                     ['None', '', ''],
                     ['None', '', ''],
                     ['None', '', ''],
                     ['None', '', ''],
                     ['None', '', '']]




   Gtk.init()
   
   win = main.Music_Admin_Start(config, settings, playlist, stationlist)
   win.connect('destroy', Gtk.main_quit)
   win.connect('delete-event', win.on_destroy)
   win.connect('configure-event', win.ReSize)

   win.show_all()
   Gtk.main()

