#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import socket
import subprocess
import pwd
import xml.etree.ElementTree
share_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/share/audok'
sys.path.insert(0, share_path)
import main
import tab_audioplayer
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib



def startup_notification_workaround():
   # https://specifications.freedesktop.org/startup-notification-spec/startup-notification-0.1.txt
   Gdk.notify_startup_complete()



if __name__ == '__main__':

   playlist = []

   settings={}

   settings['Debug'] = 0
   if sys.stdin.isatty():
      settings['Debug'] = 1

   settings['Version'] = '0.7.0'
   # generate a new settings.xml
   settings['Min_Version'] = '0.7.0'
   settings['Ipc_Port'] = 10001
   settings['Pid'] = os.getpid()
   settings['Random_Time'] = 0
   settings['Play_Time'] = 0
   settings['Play_Num'] = 0
   settings['Loop'] = 'True'

   settings['gst_player'] = 'playbin'
   #settings['gst_player'] = 'pipeline'

   settings['Filename_Settings'] = 'settings.xml'
   settings['Filename_Stations'] = 'stations.xml'
   settings['Filename_Port'] = 'ipc_port'

   settings['Choice_Pwrecord_Device'] = []
   settings['Choice_Bitrate'] = []

   settings['Share_Path'] = share_path
   settings['Music_Path'] = GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_MUSIC)
   settings['Config_Path'] = '%s/audok' % GLib.get_user_config_dir()


   files = main.Files()


   default_file_settings = files.get_default_file_settings(settings)


   if not os.path.exists('%s/%s' % (settings['Config_Path'],settings['Filename_Settings'])):
      settings.update(default_file_settings)

   else:

      tree = xml.etree.ElementTree.parse('%s/%s' % (settings['Config_Path'],settings['Filename_Settings']))
      root = tree.getroot()
      file_settings={}

      for child in root:
         if child.text is not None and child.tag is not None:

            element = child.tag.strip()
            value = child.text

            if element in default_file_settings:
               if isinstance(default_file_settings[element], int):
                  value = int(value)
               elif isinstance(default_file_settings[element], str):
                  value = str(value.strip())
               elif isinstance(default_file_settings[element], list):
                  value = value.split(',')
               elif isinstance(default_file_settings[element], float):
                  value = float(value)
   
            file_settings[element]=value


      if int(file_settings['Version'].replace('.','')) < int(settings['Min_Version'].replace('.','')):
         # backup old settings.xml
         for i in range(1,100):
            if not os.path.exists('%s/%s.%s.bak' % (settings['Config_Path'],settings['Filename_Settings'],i)):
               os.rename('%s/%s' % (settings['Config_Path'],settings['Filename_Settings']), '%s/%s.%s.bak' % (settings['Config_Path'],settings['Filename_Settings'],i))
               break
         settings.update(default_file_settings)

      else:
         settings.update(file_settings)


   
   if settings['Debug']==1:
      print ('- main version: %s Share_Path: %s pid: %s cwd: %s' % (settings['Version'],settings['Share_Path'],settings['Pid'],os.getcwd()))



   if len(sys.argv)>=2:
      if os.path.join(sys.argv[1]):
         playlist = [sys.argv[1]]



   # if audok is running + playlist
   if os.path.exists('%s/%s' % (settings['Config_Path'],settings['Filename_Port'])):


      # cat /tmp/audok/audok_port
      ipc_port=settings['Ipc_Port']
      with open('%s/%s' % (settings['Config_Path'],settings['Filename_Port']),'r') as f:
         port = f.read()
         if port:
            ipc_port = int(port)
         f.close()
      

      send_file=''
      if settings['Play_Num'] < len(playlist):
         send_file=playlist[settings['Play_Num']]


      if settings['Debug']==1:
         print ('- main %s is already running - try send file: %s via socket port: %s' % (settings['Name'],send_file,ipc_port))

      if not send_file:
         os.remove('%s/%s' % (settings['Config_Path'],settings['Filename_Port']))
         sys.exit(0)
      else:
         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', ipc_port))
            sock.sendall(send_file.encode())
         except:
            os.remove('%s/%s' % (settings['Config_Path'],settings['Filename_Port']))
         else:
            startup_notification_workaround()
            sys.exit(0)
         finally:
            sock.close()


   if settings['Debug']==1:
      print ('- main %s try to start -> Music_Admin_Start' % settings['Name'])



   if not os.path.exists('%s/%s' % (settings['Config_Path'],settings['Filename_Stations'])):
      stationlist = files.get_default_stationlist()

   else:
      stationlist = []

      try:
         tree = xml.etree.ElementTree.parse('%s/%s' % (settings['Config_Path'],settings['Filename_Stations']))
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
         if settings['Debug']==1:
            print ('- main wrong format stations.xml -> backup error: %s' % e)
         for i in range(1,100):
            if not os.path.exists('%s/%s.%s.bak' % (settings['Config_Path'],settings['Filename_Stations'],i)):
               os.rename('%s/%s' % (settings['Config_Path'],settings['Filename_Stations']), '%s/%s.%s.bak' % (settings['Config_Path'],settings['Filename_Stations'],i))
               break
         stationlist = files.get_default_stationlist()




   Gtk.init()
   
   win = main.Music_Admin_Start(settings, playlist, stationlist)
   win.connect('destroy', Gtk.main_quit)
   win.connect('delete-event', win.on_destroy)
   win.connect('configure-event', win.ReSize)

   win.show_all()
   Gtk.main()
