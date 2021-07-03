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
from gi.repository import GLib


class Music_Admin_Start(Gtk.Window):

   def __init__(self, settings, playlist, stationlist):
      Gtk.Window.__init__(self, title='Audok')

      self.set_border_width(3)
      self.settings = settings
      self.playlist = playlist
      self.stationlist = stationlist


      self.set_default_size(settings['Size_X'],settings['Size_Y'])
      #self.set_size_request(settings['Size_X'],settings['Size_Y'])
      self.move(settings['Position_X'], settings['Position_Y'])
      self.set_resizable(True) 


      self.set_icon_from_file('%s/audok.png' % settings['Path'])

      self.pnum = 0

      self.process_database = {}
      # self.process_database[item]['status'] -> active, inactive, killed
      # self.process_database[item]['todo']   -> show, nooutput, result
      # self.process_database[item]['result'] -> True, False


      self.notebook = Gtk.Notebook()
      self.add(self.notebook)


      self.notebook_tab_audioplayer = tab_audioplayer.TabAudioPlayer(self, settings, playlist)
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
            print ('def init - PanelOne ipc_server error: %s' % str(e))


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

      self.settings['Temp_Size_X']=width
      self.settings['Temp_Size_Y']=height
      self.settings['Temp_Position_X'] = position_x
      self.settings['Temp_Position_Y'] = position_y



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

      for num in range(0,10):

         self.settings['Ipc_Port'] = self.settings['Ipc_Port'] + num

         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', self.settings['Ipc_Port']))
            sock.listen(1)
            #sock.setblocking(0)
            #sock.settimeout(10)
            break
         except:
            if self.settings['Debug']==1:
               print ('def ipc_server - thread port is probably blocked -> try next port')


      if self.settings['Debug']==1:
         print ('def ipc_server - thread listen on port: %s' % self.settings['Ipc_Port'])



      while True:

         os.kill(self.settings['Mainpid'], signal.SIGUSR1)

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
                     print ('def ipc_server - thread send SIGUSR1 to pid: %s type: %s' % (self.settings['Mainpid'],type(self.settings['Mainpid'])))
                  # play one song
                  break

            if self.settings['Debug']==1:
               print ('def ipc_server - thread wait...')

         finally:
            connection.close()


