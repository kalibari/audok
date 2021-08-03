import os
import re
import sys
import threading
import signal
import socket
import subprocess
import tab_audioplayer
import tab_coverter
import tab_streamripper
import tab_settings
import tab_about
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('GLib', '2.0')
from gi.repository import GLib, GObject


class Files:

   def get_default_stationlist(self):


      default_stationlist =  [['Alternative', 'Radio freeFM Ulm', 'http://stream.freefm.de:7000/Studio'],
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

      return default_stationlist




   def get_default_file_settings(self, settings):

      default_file_settings = {  'Name': 'audok',
                                 'Old_Version': settings['Version'],
                                 'Size_X': 1000,
                                 'Size_Y': 500,
                                 'Position_X': 0,
                                 'Position_Y': 0,
                                 'Directory_New': 'New',
                                 'Directory_Old': 'Old',
                                 'Directory_Streamripper': 'Streamripper',
                                 'Bin_Youtubedl': 'youtube-dl',
                                 'Bin_Streamripper': 'streamripper',
                                 'Bin_Ffmpeg': 'ffmpeg',
                                 'Bin_Pwcli': 'pw-cli',
                                 'Bin_Pwrecord': 'pw-record',
                                 'Pwrecord_Device': 'alsa_output.pci-0000:00:1f.3.analog-stereo',
                                 'Pwrecord_Default_Filename': 'pwrecord',
                                 'Bin_Flac': 'flac', 
                                 'Bin_Nice': 'nice', 
                                 'Choice_Pwrecord_Device': ['alsa_output.pci-0000:00:1f.3.analog-stereo'],
                                 'Choice_Play_Time': ['0','20','35','50','65'],
                                 'Choice_Random_Time': ['0','10-30','30-50','50-70','70-90'],
                                 'Choice_Bitrate': ['128k','192k','224k','320k'],
                                 'Bitrate': '192k'}

      return default_file_settings



   def update_file_settings(self, settings, file_settings):

      if not os.path.exists(settings['Config_Path']):
         os.mkdir(settings['Config_Path'], 0o755)

      f = open('%s/%s' % (settings['Config_Path'],settings['Filename_Settings']), 'w')
      f.write('<?xml version="1.0"?>\n')
      f.write('<data>\n')
      for element in file_settings:

         value=file_settings[element]

         if element in settings:
            if isinstance(settings[element], int):
               value = int(value)
            elif isinstance(settings[element], str):
               value = str(value.strip())
            elif isinstance(settings[element], list):
               value = ','.join(value)
            elif isinstance(settings[element], float):
               value = float(value)

         f.write('\t<' + str(element) + '>' + str(value) + '</' + str(element) + '>\n')
      f.write('</data>\n')
      f.close()



   def update_file_stations(self, settings, stationlist, station_liststore):

      if not os.path.exists(settings['Config_Path']):
         os.mkdir(settings['Config_Path'], 0o755)

      f = open('%s/%s' % (settings['Config_Path'],settings['Filename_Stations']), 'w')
      f.write('<?xml version="1.0"?>\n')
      f.write('<data>\n')
      for i, item in enumerate(station_liststore):
         #print (stationlist[i][0])  # Alternative
         #print (stationlist[i][1])  # Radio freeFM Ulm
         #print (stationlist[i][2])  # http://stream.freefm.de:8100/listen.pls
         f.write('\t<station>\n' + '\t\t<name>' + str(stationlist[i][0]) + '</name>\n'  + '\t\t<genre>' + str(stationlist[i][1]) + '</genre>\n'  + '\t\t<url>' + str(stationlist[i][2]) +  '</url>\n' +  '\t</station>\n')
      f.write('</data>\n')
      f.close()





class Music_Admin_Start(Gtk.Window):

   def __init__(self, settings, playlist, stationlist):
      Gtk.Window.__init__(self, title='Audok')

      self.set_border_width(3)
      self.settings = settings
      self.playlist = playlist
      self.stationlist = stationlist


      self.set_default_size(settings['Size_X'],settings['Size_Y'])
      self.move(settings['Position_X'], settings['Position_Y'])
      self.set_resizable(True) 


      self.set_icon_from_file('%s/audok_large.png' % settings['App_Path'])

      self.pnum = 0

      # self.process_database[item]['status'] -> active, inactive, killed
      # self.process_database[item]['todo']   -> show, nooutput, result
      # self.process_database[item]['result'] -> True, False
      self.process_database = {}


      self.notebook = Gtk.Notebook()
      self.add(self.notebook)


      self.notebook_tab_audioplayer = tab_audioplayer.TabAudioPlayer(self, settings)
      self.notebook_tab_audioplayer.init_gui(self.playlist)
      self.notebook_tab_coverter = tab_coverter.TabConverter(self, settings)
      self.notebook_tab_streamripper = tab_streamripper.TabStreamRipper(self, settings, stationlist)
      self.notebook_tab_settings = tab_settings.TabSettings(self, settings)
      self.notebook_tab_about = tab_about.TabAbout(self, settings)


      self.notebook.append_page(self.notebook_tab_audioplayer.box, Gtk.Label('Audio Player'))
      self.notebook.append_page(self.notebook_tab_coverter.box, Gtk.Label('Converter'))
      self.notebook.append_page(self.notebook_tab_streamripper.hbox, Gtk.Label('Streamripper'))
      self.notebook.append_page(self.notebook_tab_settings.box, Gtk.Label('Settings'))
      self.notebook.append_page(self.notebook_tab_about.box, Gtk.Image.new_from_icon_name("help-about",Gtk.IconSize.MENU))


      try:
         thread = threading.Thread(target=self.ipc_server)
         thread.setDaemon(True)
         thread.start()
      except Exception as e:
         if self.settings['Debug']==1:
            print ('def init - Main ipc_server error: %s' % str(e))


      signal.signal(signal.SIGUSR1, self.signal_handler_sigusr1)
      signal.signal(signal.SIGUSR2, self.signal_handler_sigusr2)


      GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, self.signal_handler_sigint)



   def signal_handler_sigusr1(self, signal, frame):
      if self.settings['Debug']==1:
         print ('def signal_handler_sigusr1 start')

      if self.playlist:
         self.notebook_tab_audioplayer.play_file(newplaylist=self.playlist)



   def signal_handler_sigusr2(self, signal, frame):
      
      if self.settings['Debug']==1:
         print ('def signal_handler_sigusr2 start')


      if self.notebook_tab_audioplayer.checkbutton_loop.get_active():
         self.notebook_tab_audioplayer.choose_song(choose='repeat')
      elif len(self.notebook_tab_audioplayer.playlist)>=2:
         self.notebook_tab_audioplayer.choose_song(choose='next')



   def signal_handler_sigint(self):

      if self.settings['Debug']==1:
         print ('def signal_handler_sigint start (Ctrl+C)')


      if hasattr(self.notebook_tab_audioplayer, 'glib_timer'):
         GLib.source_remove(self.notebook_tab_audioplayer.glib_timer)


      if self.notebook_tab_audioplayer.player:
         self.notebook_tab_audioplayer.player.set_state(Gst.State.NULL)
         self.notebook_tab_audioplayer.player = None

      self.notebook_tab_audioplayer.play_timer_stop()

      self.process_all_killer()

      Gtk.main_quit()



   def ReSize(self, widget, data):

      (width,height) = self.get_size()
      (position_x, position_y) = self.get_position()

      #if self.settings['Debug']==1:
      #   print ('def Resize - width: %s height: %s position_x: %s position_y: %s' % (width, height, position_x, position_y))

      self.settings['Size_X']=width
      self.settings['Size_Y']=height
      self.settings['Position_X'] = position_x
      self.settings['Position_Y'] = position_y



   def on_destroy(self, data, event):
      if self.settings['Debug']==1:
         print ('def on_destroy - start')
      self.clean_shutdown()


   def on_reset_close(self):
      if self.settings['Debug']==1:
         print ('def on_reset_close - start')
      self.clean_shutdown()
      sys.exit()



   def clean_shutdown(self):

      if hasattr(self.notebook_tab_audioplayer, 'glib_timer_refresh_slider'):
         GLib.source_remove(self.notebook_tab_audioplayer.glib_timer_refresh_slider)

      if hasattr(self.notebook_tab_streamripper, 'glib_timer_streamripper'):
         GLib.source_remove(self.notebook_tab_streamripper.glib_timer_streamripper)


      if self.notebook_tab_audioplayer.player:
         self.notebook_tab_audioplayer.player.set_state(Gst.State.NULL)
         self.notebook_tab_audioplayer.player = None

      self.notebook_tab_audioplayer.play_timer_stop()
      self.process_all_killer()

      if os.path.exists('%s/%s' % (self.settings['Config_Path'],self.settings['Filename_Port'])):
         os.remove('%s/%s' % (self.settings['Config_Path'],self.settings['Filename_Port']))





   def process_all_killer(self):
   
      if self.settings['Debug']==1:
         print ('def process_all_killer - start')

      for item in self.process_database:
         if self.process_database[item]['status']=='active':
            try:
               os.kill(int(self.process_database[item]['pid']), signal.SIGINT)
            except:
               pass




   def process_job_killer(self, job):

      if self.settings['Debug']==1:
         print ('def process_job_killer - start')

      for item in self.process_database:
         if self.process_database[item]['status']=='active':
            if self.process_database[item]['job']==job:
               try:
                  os.kill(int(self.process_database[item]['pid']), signal.SIGINT)
                  self.process_database[item]['status']='killed'
               except:
                  pass

               if self.settings['Debug']==1:
                  if self.process_database[item]['status']=='killed':
                     print ('def process_job_killer - job: %s killed pid: %s' % (self.process_database[item]['job'],self.process_database[item]['pid']))
                  else:
                     print ('def process_job_killer - job: %s cannot kill pid: %s' % (self.process_database[item]['job'],self.process_database[item]['pid']))





   def process_starter(self, cmd=[], cwd='', job='', identifier='', source=''):

      self.pnum+=1
      k = {self.pnum: { 'status': 'active',
                        'job': job,
                        'todo': '',
                        'source': source,
                        'identifier': identifier,
                        'output': []}}

      self.process_database.update(k)


      if self.settings['Debug']==1:
         print ('def process_starter start')


      try:
         thread = threading.Thread(target=self.process, args=(cmd, cwd, self.pnum, self.process_database))
         thread.setDaemon(True)
         thread.start()
      except Exception as e:
         if self.settings['Debug']==1:
            print ('def process_starter error: %s' % str(e))




   def process(self, cmd=[], cwd='', pnum='', p_database={}):

      if self.settings['Debug']==1:
         print ('def process start cmd: %s cwd: %s' % (cmd,cwd))


      output_list=[]
      output_str=''
      process_pid=''
      i=0

      # cmd: ['streamripper', 'http://stream.freefm.de:8100/listen.pls', '-u', 'WinampMPEG/5.0', '-d', '/MyDisc/Audio/Neu/Streamripper']
      # cwd: /MyDisc/Audio/Neu/Streamripper


      try:
 
         process = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, close_fds=True)

         # add PID
         if self.settings['Debug']==1:
            print ('def process: add pid %s' % process.pid)
         p_database[pnum]['pid']=process.pid



         while True:

            line = process.stdout.readline(20)

            line = line.decode("utf-8", 'ignore')


            output_str = output_str + line

            out = output_str.split('\n')
            if len(out)<2:
               out = output_str.split('\r')

            if len(out)>=2:
               output_list.extend(out[:-1])
               for item in out[:-1]:
                  p_database[pnum]['todo']='show'
                  p_database[pnum]['output'].extend([item])

               output_str=out[-1]

            if not line:
               if p_database[pnum]['todo']!='nooutput':
                  p_database[pnum]['todo']='nooutput'

                  if self.settings['Debug']==1:
                     print ('def process - break')
                  break


         wait_erg=process.wait()
         if wait_erg==0:
            p_database[pnum]['result']=True
         else:
            p_database[pnum]['result']=False

 
      except Exception as e:
         if self.settings['Debug']==1:
            print ('def process error: %s job: %s' % (str(e),p_database[pnum]['job']))



    

      if self.settings['Debug']==1:
         print ('def process job %s done' % p_database[pnum]['job'])
      p_database[pnum]['todo']='result'



      
   def ipc_server(self):
      if self.settings['Debug']==1:
         print ('def ipc_server - thread start')

      if not os.path.exists(self.settings['Config_Path']):
         os.mkdir(self.settings['Config_Path'], 0o755)

      for num in range(0,10):

         self.settings['Ipc_Port'] = self.settings['Ipc_Port'] + num

         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', self.settings['Ipc_Port']))
            sock.listen(1)
            #sock.setblocking(0)
            #sock.settimeout(10)
            with open('%s/%s' % (self.settings['Config_Path'],self.settings['Filename_Port']),'w') as f:
               f.write(str(self.settings['Ipc_Port']))
               f.close()
               if self.settings['Debug']==1:
                  print ('def ipc_server - write %s/%s' % (self.settings['Config_Path'],self.settings['Filename_Port']))
            break
         except:
            if self.settings['Debug']==1:
               print ('def ipc_server - thread port is probably blocked -> try next port')



      if self.settings['Debug']==1:
         print ('def ipc_server - thread listen on port: %s' % self.settings['Ipc_Port'])



      while True:

         os.kill(self.settings['Pid'], signal.SIGUSR1)

         (connection, client_address) = sock.accept()

         try:
            while True:
               data = connection.recv(130)
               if data:
                  data = data.decode()
                  if self.settings['Debug']==1:
                     print ('def ipc_server - thread received "%s"' % data)
                  self.settings['Play_Num'] = 0
                  self.playlist = [data]
                  if self.settings['Debug']==1:
                     print ('def ipc_server - new playlist "%s"' % str(self.playlist))
               else:
                  if self.settings['Debug']==1:
                     print ('def ipc_server - thread send SIGUSR1 to pid: %s type: %s' % (self.settings['Pid'],type(self.settings['Pid'])))
                  # play one song
                  break

            if self.settings['Debug']==1:
               print ('def ipc_server - thread wait...')

         finally:
            connection.close()


