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
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, GLib, Gtk
import logging
import main
from argparse import ArgumentParser, RawTextHelpFormatter

def parse_args(name: str, version: str):

    argparser = ArgumentParser(prog='%s' % name, formatter_class=RawTextHelpFormatter)
    argparser.description = 'Audok Music Player Version: %s' % version
    argparser.add_argument('-d', action='store_true', dest='debug', help="debug to tty")
    argparser.add_argument('-l', action='store_true', dest='log', help="redirect debug to journald log")
    argparser.add_argument('filename', metavar='filename', nargs='?')

    result = argparser.parse_args()

    return result



if __name__ == '__main__':

   stationlist=[]
   playlist=[]

   config={}

   config['name'] = 'audok'
   config['application_id'] = 'com.github.kalibari.audok'

   config['version'] = '1.0.25'

   config['app_path'] = app_path

   config['play_num_filename_tag'] = (0,'','')
   config['play_duration_bitrate_codec'] = (0,'','')
   config['check_new_file'] = ''

   config['stations_changed'] = False

   config['bin_you2mp3'] = 'yt-dlp'
   config['options_you2mp3'] = ['--extract-audio', '--audio-format', 'mp3']

   config['bin_streamripper'] = 'streamripper'
   config['options_streamripper'] = ['-u', 'WinampMPEG/5.0']

   config['bin_ffmpeg'] = 'ffmpeg'
   config['options_ffmpeg'] = ['-v', 'error']

   config['bin_pwcli'] = 'pw-cli'
   config['options_pwcli'] = ['list-objects']

   config['bin_pwrecord'] = 'pw-record'
   config['options_pwrecord'] = ['--verbose','--record','--channels=2', '--format=s32', '--rate=48000', '--volume=0.99']

   config['bin_parecord'] = 'parecord'
   config['options_parecord'] = ['--verbose','--record','--channels=2', '--format=s32', '--rate=48000', '--volume=0.99', '--file-format=wav']

   config['bin_pactl'] = 'pactl'
   config['options_pactl'] = ['list']

   config['bin_nice'] = 'nice'
   config['options_nice'] = ['-n', '19']

   config['supported_audio_files'] = ['mp3','ogg','aac','flac','midi','mp4','mpeg','wma','asx','wav','mpegurl','webm']

   config['music_path'] = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_MUSIC)
   if not config['music_path']:
      config['music_path']=os.getenv('HOME')

   config['debug'] = 0
   config['log'] = 0


   result = parse_args(name=config['name'], version=config['version'])
   if result.debug:
      config['debug'] = 1
   if result.log:
      config['log'] = 1



   log = logging.getLogger(config['name'])
   log.propagate = False

   fm='%(module)s - %(funcName)s - %(message)s'
   formatter = logging.Formatter(fm)

   if config['debug'] == 1:
      sh = logging.StreamHandler()
      sh.setFormatter(formatter)
      log.addHandler(sh)

   if config['log'] == 1:
      from systemd.journal import JournalHandler
      jo = JournalHandler(SYSLOG_IDENTIFIER=config['application_id'])
      jo.setFormatter(formatter)
      log.addHandler(jo)

   log.setLevel(logging.DEBUG)



   settings={}

   settings['version'] = config['version']


   # setup default settings
   settings['config_path'] = '%s/audok' % GLib.get_user_config_dir()
   if not settings['config_path']:
      settings['config_path']=os.getenv('HOME')

   settings['filename_settings'] = 'settings.xml'
   settings['filename_stations'] = 'stations.xml'
   settings['filename_ipcport'] = 'ipc_port'

   settings['directory_new'] = ''
   settings['directory_old'] = 'Old'
   settings['directory_str'] = 'Streamripper'

   settings['checkbutton_new'] = '1'
   settings['checkbutton_old'] = '0'
   settings['checkbutton_str'] = '0'
   settings['checkbutton_auto_move'] = '0'
   settings['checkbutton_auto_play'] = '0'


   # 1280×720, 1280×960, 1024×768
   settings['size_x'] = '1000'
   settings['size_y'] = '500'

   settings['position_x'] = '0'
   settings['position_y'] = '0'

   settings['directory_converter'] = ''

   settings['directory_record'] = ''
   settings['filename_record'] = 'record.wav'

   settings['device_record'] = ''
   settings['device_record_list'] = ['']

   settings['color_scheme'] = 'default'
   settings['color_scheme_list'] = ['default', 'force_light', 'force_dark']

   settings['play_time'] = '0'
   settings['choice_play_time'] = ['0','10','20','35','50','65']

   settings['random_time_min'] = '0'
   settings['random_time_max'] = '0'
   settings['choice_random_time'] = ['0','10-30','30-50','50-70','70-90']

   settings['bitrate'] = '320k'
   settings['choice_bitrate'] = ['128k','192k','224k','320k']

   settings['directory_playlist'] = ''
   settings['filename_playlist'] = 'playlist.m3u'

   settings['ipc_port'] = '10001'

   settings['stations_toogle_on'] = ['']

   settings['label_play_show_tag'] = '0'



   # read the settings file
   path = settings['config_path']
   filename = settings['filename_settings']

   if os.path.exists(path + '/' + filename):
      log.debug('try to read file: %s' % settings['filename_settings'])

      try:
         tree = xml.etree.ElementTree.parse(path + '/' + filename)
         root = tree.getroot()

         for child in root:
            if child.tag is not None:

               element = child.tag.strip()

               if child.text is None:
                   value = ''
               else:
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
         log.debug('cannot read file: %s error: %s -> mv to .bak' % (settings['filename_settings'],e))

         path = settings['config_path']
         filename = settings['filename_settings']

         for i in range(1,100):
            if not os.path.exists('%s/%s.%s.bak' % (path,filename,i)):
               os.rename('%s/%s' % (path,filename), '%s/%s.%s.bak' % (path,filename,i))
               break


   log.debug('app_path: %s' % config['app_path'])
   log.debug('cwd: %s' % os.getcwd())
   log.debug('config path: %s' % settings['config_path'])
   log.debug('directories new: %s old: %s streamripper: %s' % (settings['directory_new'],settings['directory_old'],settings['directory_str']))



   if result.filename and os.path.exists(result.filename):
      config['check_new_file']=result.filename



   # if audok is running + playlist
   if os.path.exists('%s/%s' % (settings['config_path'],settings['filename_ipcport'])):


      # cat /tmp/audok/audok_port
      ipc_port=settings['ipc_port']
      with open('%s/%s' % (settings['config_path'],settings['filename_ipcport']),'r') as f:
         port = f.read()
         if port:
            ipc_port = port


      log.debug('name: %s is already running - try send filename: %s via socket port: %s' % (config['name'],config['check_new_file'],ipc_port))


      if not config['check_new_file']:
         os.remove('%s/%s' % (settings['config_path'],settings['filename_ipcport']))
         sys.exit(0)
      else:
         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', int(ipc_port)))
            sock.sendall(('new-file=' + config['check_new_file']).encode())
         except:
            os.remove('%s/%s' % (settings['config_path'],settings['filename_ipcport']))
         else:
            sys.exit(0)
         finally:
            sock.close()



   log.debug('name: %s try to start -> Music_Admin_Start' % config['name'])


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
         log.debug('wrong format stations.xml -> backup error: %s' % e)
         for i in range(1,100):
            if not os.path.exists('%s/%s.%s.bak' % (settings['config_path'],settings['filename_stations'],i)):
               os.rename('%s/%s' % (settings['config_path'],settings['filename_stations']), '%s/%s.%s.bak' % (settings['config_path'],settings['filename_stations'],i))
               break
         stationlist = []


   def on_activate(app):
      main.Music_Admin_Start(app, log, config, settings, playlist, stationlist)

   Adw.init()
   app = Adw.Application(application_id=config['application_id'])
   app.connect('activate', on_activate)
   app.run(None)
