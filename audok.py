#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import re
import socket
import subprocess
import pwd
import xml.etree.ElementTree
import main
import tab_audioplayer
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk



def startup_notification_workaround():
   # https://specifications.freedesktop.org/startup-notification-spec/startup-notification-0.1.txt
   Gdk.notify_startup_complete()



def stations_xml():

   if os.path.exists('%s/.config/audok/stations.xml' % os.environ['HOME']):

      if settings['Debug']==1:
         print ('def stations_xml - read stations.xml')

      stationlist = []

      try:
         tree = xml.etree.ElementTree.parse('%s/.config/audok/stations.xml' % os.environ['HOME'])
         root = tree.getroot()

         for child in root:

            try:
               child[0].text.strip()
               child[1].text.strip()
               child[2].text.strip()
            except:
               pass

            stationlist.extend([[child[0].text,child[1].text,child[2].text]])

      except:
         if settings['Debug']==1:
            print ('- main wrong format stations.xml -> backup')
         for i in range(1,100):
            if not os.path.exists('%s/.config/audok/stations.xml.%s.bak' % (os.environ['HOME'],str(i))):
               os.rename('%s/.config/audok/stations.xml' % os.environ['HOME'], '%s/.config/audok/stations.xml.%s.bak' % (os.environ['HOME'],i))
               break



   if not os.path.exists('%s/.config/audok/stations.xml' % os.environ['HOME']):

      if settings['Debug']==1:
         print ('use predifined stations instead of stations.xml')

      # see https://directory.shoutcast.com/Search

      stationlist =  [  ['Alternative', 'Radio freeFM Ulm', 'http://stream.freefm.de:7000/Studio'],
                        ['Alternative', 'Radio FM 4 at', 'https://orf-live.ors-shoutcast.at/fm4-q2a'],
                        ['Alternative', 'Zeilsteen Radio', 'http://live.zeilsteen.com:80'],

                        ['Mix', 'Pirate Radio Bayern', 'http://78.46.126.219:8000/stream'],
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
                        ['None', '', '']]

   return stationlist




def settings_xml(version):

   settings = {}

   update_xml=False


   if not os.path.exists('%s/.config/audok/settings.xml' % os.environ['HOME']):
      update_xml=True

   else:

      check_version=''

      try:
         tree = xml.etree.ElementTree.parse('%s/.config/audok/settings.xml' % os.environ['HOME'])
         root = tree.getroot()

         for child in root:
            if child.text is not None and child.tag is not None:
               child.text.strip()
               settings[child.tag]=child.text


         if 'Version' in settings:
            check_version=settings['Version']

         if 'Play_Num' in settings:
            settings['Play_Num']=int(settings['Play_Num'])

         if 'Size_X' in settings:
            settings['Size_X']=int(settings['Size_X'])

         if 'Size_Y' in settings:
            settings['Size_Y']=int(settings['Size_Y'])

         if 'Position_X' in settings:
            settings['Position_X']=int(settings['Position_X'])

         if 'Position_Y' in settings:
            settings['Position_Y']=int(settings['Position_Y'])

         if 'Ipc_Port' in settings:
            settings['Ipc_Port']=int(settings['Ipc_Port'])

         if 'Dlna_Port' in settings:
            settings['Dlna_Port']=int(settings['Dlna_Port'])

      except:
         update_xml=True


      if update_xml==False and check_version:
         try:
            if int(version.replace('.',''))>int(check_version.replace('.','')):
               update_xml=True
         except:
            update_xml=True


      if update_xml==True:
         for i in range(1,100):
            if not os.path.exists('%s/.config/audok/settings.xml.%s.bak' % (os.environ['HOME'],i)):
               os.rename('%s/.config/audok/settings.xml' % os.environ['HOME'], '%s/.config/audok/settings.xml.%s.bak' % (os.environ['HOME'],i))
               break



   if update_xml==True:

      settings = {'Name': 'audok',
                  'Version': version,
                  'Path': '/opt/audok',
                  'Play_Num': 0,
                  'Size_X': 1000,
                  'Size_Y': 500,
                  'Position_X': 0,
                  'Position_Y': 0,
                  'Ipc_Port': 10001,
                  'Directory_New': '/home/%s/Musik/New' % pwd.getpwuid(os.getuid())[0],
                  'Directory_Old': '/home/%s/Musik/Old' % pwd.getpwuid(os.getuid())[0],
                  'Directory_Streamripper': '/home/%s/Musik/Streamripper' % pwd.getpwuid(os.getuid())[0],
                  'Bin_Youtubedl': '/usr/bin/youtube-dl',
                  'Bin_Streamripper': '/usr/bin/streamripper',
                  'Bin_Ffmpeg': '/usr/bin/ffmpeg',
                  'Bin_Pwrecord': '/usr/bin/pw-record',
                  'Bin_Pwcli': '/usr/bin/pw-cli',
                  'Pwcli_object_path': 'alsa:pcm:0:front:0:playback',
                  'Bin_Flac': '/usr/bin/flac', 
                  'Bin_Nice': '/usr/bin/nice', 
                  'Dlna_Port': 10921,
                  'Dlna_Filter': '',
                  'Choice_Play_Time': '0,20,35,50,65',
                  'Choice_Random_Time': '0,10-30,30-50,50-70,70-90',
                  'File2mp3_Bitrate': '192k',
                  'Choice_File2mp3_Bitrate': '128k,192k,224k,320k',
                  'Record2wav_Default_Wav_Filename': 'pwrecord'}


      if not os.path.exists('%s/.config/audok' % os.environ['HOME']):
         os.mkdir('%s/.config/audok' % os.environ['HOME'], 0o755);

      f = open('%s/.config/audok/settings.xml' % os.environ['HOME'], 'w')
      f.write('<?xml version="1.0"?>\n')
      f.write('<data>\n')
      for item in settings:
         f.write('\t<' + str(item) + '>' + str(settings[item]) + '</' + str(item) + '>\n')
      f.write('</data>\n')
      f.close()


   return settings




if __name__ == '__main__':

   playlist = []


   ###############
   version='0.6.9'
   ###############


   settings = settings_xml(version)

   settings['Debug'] = 0
   if sys.stdin.isatty():
      settings['Debug'] = 1

   settings['Mainpid'] = os.getpid()
   settings['Random_Time'] = '0'
   settings['Play_Time'] = '0'
   settings['Loop'] = 'True'

   settings['Temp_Size_X'] = 0
   settings['Temp_Size_Y'] = 0
   settings['Temp_Position_X'] = 0
   settings['Temp_Position_Y'] = 0


   settings['gst_player'] = 'playbin'
   #settings['gst_player'] = 'pipeline'



   #Test dialogWindow:
   #dialogWindow = Gtk.MessageDialog(self, Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT, Gtk.MessageType.QUESTION, Gtk.ButtonsType.OK_CANCEL, "test")
   #dialogWindow.show_all()


   #tab_audioplayer = tab_audioplayer.TabAudioPlayer(settings)
   #tab_audioplayer.player.set_property("uri", "file:///MyDisc/Audio/Neu/Knightlife_Dont_Stop.mp3")
   #tab_audioplayer.player.set_state(Gst.State.PLAYING)



   (p1,p2) = os.path.split(os.path.realpath(sys.argv[0]))
   settings['Path'] = p1

   
   if settings['Debug']==1:
      print ('- main version: %s path: %s pid: %s cwd: %s' % (settings['Version'],settings['Path'],settings['Mainpid'],os.getcwd()))



   if len(sys.argv)>=2:
      if os.path.join(sys.argv[1]):
         playlist = [sys.argv[1]]


   # pidof
   pids=[]
   try:
      erg = subprocess.check_output(['pidof','-x',settings['Name']], shell=False, close_fds=True)
      if settings['Debug']==1:
         print ('- main pidof erg: %s' % str(erg))
      erg = erg.decode()
      pids = erg.split()
      if settings['Debug']==1:
         print ('- main pidof pids: %s' % str(pids))

      pids.remove(str(settings['Mainpid']))
   except Exception as e:
      if settings['Debug']==1:
         print ('- main pidof error: %s' % str(e))




   # if audok is running + playlist
   if len(pids)>0 and len(playlist)>0:


      if settings['Debug']==1:
         print ('- main %s is already running -> try send file: %s via socket' % (settings['Name'],playlist[settings['Play_Num']]))

      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      sock.connect(('localhost', settings['Ipc_Port']))
      try:
         sock.sendall(playlist[settings['Play_Num']].encode())
      finally:
         sock.close()


      startup_notification_workaround()
      sys.exit(0)

   else:

      if settings['Debug']==1:
         print ('- main %s try to start -> Music_Admin_Start' % settings['Name'])


      stationlist = stations_xml()

      Gtk.init()
      
      win = main.Music_Admin_Start(settings, playlist, stationlist)
      win.connect('destroy', Gtk.main_quit)
      win.connect('delete-event', win.on_destroy)
      win.connect('configure-event', win.ReSize)

      win.show_all()
      Gtk.main()
