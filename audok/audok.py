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
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GLib', '2.0')
from gi.repository import GLib
import logging
import main



def startup_notification_workaround():
   # https://specifications.freedesktop.org/startup-notification-spec/startup-notification-0.1.txt
   Gdk.notify_startup_complete()



if __name__ == '__main__':

   stationlist=[]
   playlist=[]

   config={}

   config['name'] = 'audok'
   config['version'] = '1.0.10'
   config['app_path'] = app_path

   config['play_num'] = 0

   config['stations_changed'] = False

   config['bin_youtubedl'] = 'youtube-dl'
   config['bin_streamripper'] = 'streamripper'
   config['bin_ffmpeg'] = 'ffmpeg'
   config['bin_pwcli'] = 'pw-cli'
   config['bin_pwrecord'] = 'pw-record'
   config['bin_nice'] = 'nice'

   config['supported_audio_files'] = ['mp3','ogg','aac','flac','midi','mp4','mpeg','wma','asx','wav','mpegurl']


   settings={}

   settings['version'] = config['version']
   settings['journald_log'] = '0'
   settings['tty_debug'] = '0'
   #settings['tty_debug'] = '1'


   log = logging.getLogger(config['name'])
   if settings['tty_debug'] == '1':
      if sys.stdin.isatty():
         log.addHandler(logging.StreamHandler())
         log.setLevel(logging.DEBUG)

   if settings['journald_log'] == '1':
      from systemd.journal import JournalHandler
      log.addHandler(JournalHandler())
      log.setLevel(logging.DEBUG)


   # setup default settings
   settings['config_path'] = '%s/audok' % GLib.get_user_config_dir()
   if not settings['config_path']:
      settings['config_path']=os.getenv('HOME')

   settings['music_path'] = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_MUSIC)
   if not settings['music_path']:
      settings['music_path']=os.getenv('HOME')

   settings['filename_settings'] = 'settings.xml'
   settings['filename_stations'] = 'stations.xml'
   settings['filename_ipcport'] = 'ipc_port'

   settings['directory_new'] = 'New'
   settings['directory_old'] = 'Old'
   settings['directory_str'] = 'Streamripper'

   settings['checkbutton_new'] = '0'
   settings['checkbutton_old'] = '0'
   settings['checkbutton_str'] = '0'
   settings['checkbutton_auto_move'] = '0'
   settings['checkbutton_auto_play'] = '0'

   settings['size_x'] = '1000'
   settings['size_y'] = '500'
   settings['position_x'] = '0'
   settings['position_y'] = '0'

   settings['directory_converter'] = 'New'

   settings['directory_pwrecord'] = 'New'
   settings['filename_pwrecord'] = 'pwrecord.wav'
   settings['device_pwrecord'] = ''

   settings['choice_device_pwrecord'] = ['']

   settings['play_time'] = '0'
   settings['choice_play_time'] = ['0','10','20','35','50','65']

   settings['random_time_min'] = '0'
   settings['random_time_max'] = '0'
   settings['choice_random_time'] = ['0','10-30','30-50','50-70','70-90']

   settings['bitrate'] = '192k'
   settings['choice_bitrate'] = ['128k','192k','224k','320k']

   settings['directory_playlist'] = 'New'
   settings['filename_playlist'] = 'playlist.m3u'

   settings['ipc_port'] = '10001'

   settings['stations_toogle_on'] = []




   # read the settings file
   path = settings['config_path']
   filename = settings['filename_settings']

   if os.path.exists(path + '/' + filename):
      log.debug('def main - try to read file: %s' % settings['filename_settings'])

      try:
         tree = xml.etree.ElementTree.parse(path + '/' + filename)
         root = tree.getroot()

         for child in root:
            if child.text is not None and child.tag is not None:

               element = child.tag.strip()
               value = child.text

               if value.startswith('[') and value.endswith(']'):
                  value=value.replace('[','',1)
                  value=value.replace(']','',1)
                  if ',' in value:
                     value=value.split(',')
                  else:
                     if value:
                        value=[value]
                     else:
                        value=[]

               settings[element]=value


      except Exception as e:
         log.debug('def main - cannot read file: %s error: %s -> mv to .bak' % (settings['filename_settings'],e))

         path = settings['config_path']
         filename = settings['filename_settings']

         for i in range(1,100):
            if not os.path.exists('%s/%s.%s.bak' % (path,filename,i)):
               os.rename('%s/%s' % (path,filename), '%s/%s.%s.bak' % (path,filename,i))
               break


   log.debug('def main - app_path: %s' % config['app_path'])
   log.debug('def main - cwd: %s' % os.getcwd())
   log.debug('def main - music path: %s' % settings['music_path'])
   log.debug('def main - config path: %s' % settings['config_path'])
   log.debug('def main - directories new: %s old: %s streamripper: %s' % (settings['directory_new'],settings['directory_old'],settings['directory_str']))
   log.debug('def main - playlist: %s' % playlist)


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
            ipc_port = port
      

      send_file=''
      if config['play_num'] < len(playlist):
         send_file='play_new_file=%s' % playlist[config['play_num']]


      log.debug('def main - name: %s is already running - try send file: %s via socket port: %s' % (config['name'],send_file,ipc_port))


      if not send_file:
         os.remove('%s/%s' % (settings['config_path'],settings['filename_ipcport']))
         sys.exit(0)
      else:
         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', int(ipc_port)))
            sock.sendall(send_file.encode())
         except:
            os.remove('%s/%s' % (settings['config_path'],settings['filename_ipcport']))
         else:
            startup_notification_workaround()
            sys.exit(0)
         finally:
            sock.close()


   log.debug('def main - name: %s try to start -> Music_Admin_Start' % config['name'])


   if os.path.exists('%s/%s' % (settings['config_path'],settings['filename_stations'])):

      try:
         tree = xml.etree.ElementTree.parse('%s/%s' % (settings['config_path'],settings['filename_stations']))
         root = tree.getroot()
         for child in root:
            col0=''
            col1=''
            col2=''
            if child[0].text:
               col0=child[0].text.strip()
            if child[1].text:
               col1=child[1].text.strip()
            if child[2].text:
               col2=child[2].text.strip()
            stationlist.extend([[col0,col1,col2]])

      except Exception as e:
         log.debug('def main - wrong format stations.xml -> backup error: %s' % e)
         for i in range(1,100):
            if not os.path.exists('%s/%s.%s.bak' % (settings['config_path'],settings['filename_stations'],i)):
               os.rename('%s/%s' % (settings['config_path'],settings['filename_stations']), '%s/%s.%s.bak' % (settings['config_path'],settings['filename_stations'],i))
               break
         stationlist = []


   Gtk.init()
   
   win = main.Music_Admin_Start(log, config, settings, playlist, stationlist)
   win.connect('destroy', Gtk.main_quit)
   win.connect('delete-event', win.on_destroy)
   win.connect('configure-event', win.ReSize)

   win.show_all()
   Gtk.main()

