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
from time import sleep
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('GLib', '2.0')
from gi.repository import GLib
gi.require_version('GObject', '2.0')
from gi.repository import GObject



class Music_Admin_Start(Gtk.Window):

   def __init__(self, config, settings, playlist, stationlist):
      Gtk.Window.__init__(self, title='Audok')

      self.set_border_width(3)

      self.config = config
      self.settings = settings
      self.playlist = playlist
      self.stationlist = stationlist


      self.set_default_size(settings['size_x'],settings['size_y'])
      self.move(settings['position_x'], settings['position_y'])
      self.set_resizable(True) 


      self.set_icon_from_file('%s/audok_large.png' % config['app_path'])

      self.pnum = 0

      # self.process_database[item]['status'] -> active, inactive, killed
      # self.process_database[item]['todo']   -> show, nooutput, result
      # self.process_database[item]['result'] -> True, False
      self.process_database = {}


      self.notebook = Gtk.Notebook()
      self.add(self.notebook)


      self.notebook_tab_audioplayer = tab_audioplayer.TabAudioPlayer(self, config, settings, playlist)
      self.notebook_tab_converter = tab_coverter.TabConverter(self, config, settings)
      self.notebook_tab_streamripper = tab_streamripper.TabStreamRipper(self, config, settings, stationlist)
      self.notebook_tab_settings = tab_settings.TabSettings(self, config, settings)
      self.notebook_tab_about = tab_about.TabAbout(self, config, settings)


      self.notebook.append_page(self.notebook_tab_audioplayer.box, Gtk.Label('Audio Player'))
      self.notebook.append_page(self.notebook_tab_converter.box, Gtk.Label('Converter'))
      self.notebook.append_page(self.notebook_tab_streamripper.hbox, Gtk.Label('Streamripper'))
      self.notebook.append_page(self.notebook_tab_settings.box, Gtk.Label('Settings'))
      self.notebook.append_page(self.notebook_tab_about.box, Gtk.Image.new_from_icon_name("help-about",Gtk.IconSize.MENU))


      try:
         thread = threading.Thread(target=self.ipc_server)
         thread.setDaemon(True)
         thread.start()
      except Exception as e:
         if self.config['debug']==1:
            print ('def init - Main ipc_server error: %s' % str(e))


      GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, self.signal_handler_sigint)

      if self.playlist:
         self.notebook_tab_audioplayer.choose_song(choose='keep')



   def signal_handler_sigint(self):

      if self.config['debug']==1:
         print ('def signal_handler_sigint start (Ctrl+C)')
      self.clean_shutdown()
      Gtk.main_quit()
      sys.exit()



   def on_destroy(self, data, event):
      if self.config['debug']==1:
         print ('def on_destroy - start')
      self.save_settings()
      self.clean_shutdown()
      Gtk.main_quit()
      sys.exit()



   def on_reset_close(self):
      if self.config['debug']==1:
         print ('def on_reset_close - start')
      self.clean_shutdown()
      Gtk.main_quit()
      sys.exit()




   def save_settings(self):

      # save settings to ~/.config/audok/settings.xml
      if self.config['debug']==1:
         print ('def clean_shutdown - save settings')

      path = self.settings['config_path']
      filename = self.settings['filename_settings']

      if not os.path.exists(path):
         os.mkdir(path, 0o755)

      f = open(path + '/' + filename, 'w')
      f.write('<?xml version="1.0"?>\n')
      f.write('<data>\n')
      for element in self.settings:
         value = self.settings[element]
         if isinstance(value, int):
            value = int(value)
         elif isinstance(value, str):
            value = value.strip()
         elif isinstance(value, list):
            value = '[' + ','.join(value) + ']'

         f.write('\t<' + str(element) + '>' + str(value) + '</' + str(element) + '>\n')
      f.write('</data>\n')
      f.close()


      if self.config['stationlist_changed']==True:

         station_liststore=self.notebook_tab_streamripper.station_liststore
         stationlist=self.notebook_tab_streamripper.stationlist


         f = open('%s/%s' % (self.settings['config_path'],self.settings['filename_stations']), 'w')
         f.write('<?xml version="1.0"?>\n')
         f.write('<data>\n')
         for i, item in enumerate(station_liststore):
            #print (stationlist[i][0])  # Alternative
            #print (stationlist[i][1])  # Radio freeFM Ulm
            #print (stationlist[i][2])  # http://stream.freefm.de:8100/listen.pls
            f.write('\t<station>\n' + '\t\t<name>' + str(stationlist[i][0]) + '</name>\n'  + '\t\t<genre>' + str(stationlist[i][1]) + '</genre>\n'  + '\t\t<url>' + str(stationlist[i][2]) +  '</url>\n' +  '\t</station>\n')
         f.write('</data>\n')
         f.close()





   def clean_shutdown(self):

      if self.config['debug']==1:
         print ('def clean_shutdown - start')


      if hasattr(self, 'notebook_tab_converter'):

         if self.notebook_tab_converter.obj_timer_file2flac is not None:
            GObject.source_remove(self.notebook_tab_converter.obj_timer_file2flac)

         if self.notebook_tab_converter.obj_timer_pwrecord is not None:
            GObject.source_remove(self.notebook_tab_converter.obj_timer_pwrecord)

         if self.notebook_tab_converter.obj_timer_file2mp3 is not None:
            GObject.source_remove(self.notebook_tab_converter.obj_timer_file2mp3)

         if self.notebook_tab_converter.obj_timer_you2mp3 is not None:
            GObject.source_remove(self.notebook_tab_converter.obj_timer_you2mp3)



      if hasattr(self, 'notebook_tab_audioplayer'):

         if self.notebook_tab_audioplayer.player:
            self.notebook_tab_audioplayer.player.set_state(Gst.State.NULL)

         if self.notebook_tab_audioplayer.obj_timer_refresh_slider is not None:
            GObject.source_remove(self.notebook_tab_audioplayer.obj_timer_refresh_slider)

         if self.notebook_tab_audioplayer.obj_timer_play_time is not None:
            GObject.source_remove(self.notebook_tab_audioplayer.obj_timer_play_time)


      if hasattr(self, 'notebook_tab_streamripper'):

         if self.notebook_tab_streamripper.obj_timer_streamripper is not None:
            GObject.source_remove(self.notebook_tab_streamripper.obj_timer_streamripper)



      self.process_all_killer()

      if os.path.exists('%s/%s' % (self.settings['config_path'],self.settings['filename_ipcport'])):
         os.remove('%s/%s' % (self.settings['config_path'],self.settings['filename_ipcport']))





   def ReSize(self, widget, data):

      (width,height) = self.get_size()
      (position_x, position_y) = self.get_position()

      self.settings['size_x'] = width
      self.settings['size_y'] = height
      self.settings['position_x'] = position_x
      self.settings['position_y'] = position_y



   def process_all_killer(self):
   
      if self.config['debug']==1:
         print ('def process_all_killer - start')

      for item in self.process_database:
         if self.process_database[item]['status']=='active':
            try:
               os.kill(int(self.process_database[item]['pid']), signal.SIGINT)
               sleep(0.05)
            except:
               pass

      if self.config['debug']==1:
         print ('def process_all_killer - ends')



   
   def file_scan(self, directories, extensions):

      allfiles = set()

      for directory in directories:
         if self.config['debug']==1:
            print ('def file_scan - scan directory: %s' % directory)
         for ext in extensions:
            for item in os.listdir(directory):
               if item.endswith(ext):
                  pitem = directory + '/' + item
                  if os.path.isfile(pitem):
                     allfiles.add(pitem)

      # reverse
      allfiles=list(allfiles)
      if len(allfiles)>=1:
         allfiles=allfiles[::-1]

      return allfiles




   def process_job_killer(self, job):

      if self.config['debug']==1:
         print ('def process_job_killer - start')

      for item in self.process_database:
         if self.process_database[item]['status']=='active':
            if self.process_database[item]['job']==job:
               try:
                  os.kill(int(self.process_database[item]['pid']), signal.SIGINT)
                  self.process_database[item]['status']='killed'
               except:
                  pass

               if self.config['debug']==1:
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


      if self.config['debug']==1:
         print ('def process_starter start')


      try:
         thread = threading.Thread(target=self.process, args=(cmd, cwd, self.pnum, self.process_database))
         thread.setDaemon(True)
         thread.start()
      except Exception as e:
         if self.config['debug']==1:
            print ('def process_starter error: %s' % str(e))




   def process(self, cmd=[], cwd='', pnum='', p_database={}):

      if self.config['debug']==1:
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
         if self.config['debug']==1:
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

                  if self.config['debug']==1:
                     print ('def process - break')
                  break


         wait_erg=process.wait()
         if wait_erg==0:
            p_database[pnum]['result']=True
         else:
            p_database[pnum]['result']=False

      except Exception as e:
         if self.config['debug']==1:
            print ('def process error: %s job: %s' % (str(e),p_database[pnum]['job']))


      if self.config['debug']==1:
         print ('def process job %s done' % p_database[pnum]['job'])
      p_database[pnum]['todo']='result'



      
   def ipc_server(self):

      if self.config['debug']==1:
         print ('def ipc_server - thread start')

      if not os.path.exists(self.settings['config_path']):
         os.mkdir(self.settings['config_path'], 0o755)

      for num in range(0,10):

         self.settings['ipc_port'] = self.settings['ipc_port'] + num

         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', self.settings['ipc_port']))
            sock.listen(1)
            with open('%s/%s' % (self.settings['config_path'],self.settings['filename_ipcport']),'w') as f:
               f.write(str(self.settings['ipc_port']))
               f.close()
               if self.config['debug']==1:
                  print ('def ipc_server - write %s/%s' % (self.settings['config_path'],self.settings['filename_ipcport']))
            break
         except:
            if self.config['debug']==1:
               print ('def ipc_server - thread port is probably blocked -> try next port')



      if self.config['debug']==1:
         print ('def ipc_server - thread listen on port: %s' % self.settings['ipc_port'])



      try:

         while True:

            (connection, client_address) = sock.accept()
            
            receive_data=True

            while receive_data:
               data = connection.recv(130)
               if data:
                  data = data.decode()

                  if self.config['debug']==1:
                     print ('def ipc_server - thread received "%s"' % data)

                  if data=='play_timer_end':
                     self.settings['interrupt']='play_timer_end'
                     self.notebook_tab_audioplayer.player.post_message(Gst.Message.new_application(self.notebook_tab_audioplayer.player,Gst.Structure.new_empty("song-changed")))

                  elif data.startswith('play_new_file='):
                     self.settings['interrupt']='play_new_file'
                     data=data.replace('play_new_file=','',1)
                     self.config['play_num'] = 0
                     self.notebook_tab_audioplayer.playlist = [data]
                     self.notebook_tab_audioplayer.player.post_message(Gst.Message.new_application(self.notebook_tab_audioplayer.player,Gst.Structure.new_empty("song-changed")))

               else:
                  if self.config['debug']==1:
                     print ('def ipc_server - received data')
                  receive_data=False

            if self.config['debug']==1:
               print ('def ipc_server - thread wait...')


      finally:
         if self.config['debug']==1:
            print ('def ipc_server - close')
         connection.close()


