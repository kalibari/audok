import os
import re
import sys
import signal
import socket
import subprocess
import tab_musicplayer
import tab_coverter
import tab_streamripper
import tab_settings
import tab_about
import gi
from time import sleep
from threading import Thread
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('GLib', '2.0')
from gi.repository import GLib


class Music_Admin_Start(Gtk.Window):

   def __init__(self, log, config, settings, playlist, stationlist):
      Gtk.Window.__init__(self, title=config['name'].title())

      self.set_border_width(3)

      self.log = log
      self.config = config
      self.settings = settings
      self.playlist = playlist
      self.stationlist = stationlist


      #self.set_default_size(int(settings['size_x']),int(settings['size_y']))
      self.move(int(settings['position_x']), int(settings['position_y']))
      self.set_resizable(True) 


      self.set_icon_from_file('%s/audok_large.png' % config['app_path'])

      self.pnum = 0

      # self.process_database[item]['status'] -> active, inactive, killed
      # self.process_database[item]['todo']   -> show, nooutput, result
      # self.process_database[item]['result'] -> True, False
      self.process_database = {}


      self.notebook = Gtk.Notebook()
      self.add(self.notebook)


      self.notebook_tab_musicplayer = tab_musicplayer.TabMusicPlayer(self, log, config, settings, playlist)
      self.notebook_tab_converter = tab_coverter.TabConverter(self, log, config, settings)
      self.notebook_tab_streamripper = tab_streamripper.TabStreamRipper(self, log, config, settings, stationlist)
      self.notebook_tab_settings = tab_settings.TabSettings(self, log, config, settings)
      self.notebook_tab_about = tab_about.TabAbout(self, log, config, settings)


      self.notebook.append_page(self.notebook_tab_musicplayer.box, Gtk.Label(label='Music Player'))
      self.notebook.append_page(self.notebook_tab_converter.box, Gtk.Label(label='Converter'))
      self.notebook.append_page(self.notebook_tab_streamripper.hbox, Gtk.Label(label='Streamripper'))
      self.notebook.append_page(self.notebook_tab_settings.vbox, Gtk.Label(label='Settings'))
      self.notebook.append_page(self.notebook_tab_about.box, Gtk.Image.new_from_icon_name('help-about',Gtk.IconSize.MENU))


      try:
         thread = Thread(target=self.ipc_server)
         thread.setDaemon(True)
         thread.start()
      except Exception as e:
         self.log.debug('ipc_server error: %s' % str(e))





      GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, self.signal_handler_sigint)

      if self.playlist:
         self.notebook_tab_musicplayer.choose_song(num=self.config['play_num'])
         self.notebook_tab_musicplayer.play_file()



   def signal_handler_sigint(self):
      self.log.debug('start (Ctrl+C)')
      self.clean_shutdown()
      Gtk.main_quit()
      sys.exit()



   def on_destroy(self, data, event):
      self.log.debug('start')
      self.save_settings()
      self.clean_shutdown()
      Gtk.main_quit()
      sys.exit()



   def on_reset_close(self):
      self.log.debug('start')
      self.clean_shutdown()
      Gtk.main_quit()
      sys.exit()



   def save_settings(self):

      # save settings to ~/.config/audok/settings.xml
      self.log.debug('start')

      path = self.settings['config_path']
      filename = self.settings['filename_settings']

      if not os.path.exists(path):
         os.mkdir(path, 0o755)


      f = open(path + '/' + filename, 'w')
      f.write('<?xml version="1.0"?>\n')
      f.write('<data>\n')
      for element in self.settings:
         value = self.settings[element]
         if isinstance(value, list):
            value = '[' + ','.join(value) + ']'
         else:
            value = value.strip()

         f.write('\t<' + str(element) + '>' + str(value) + '</' + str(element) + '>\n')
      f.write('</data>\n')
      f.close()


      if self.config['stations_changed']==True:

         stationlist=self.notebook_tab_streamripper.stationlist

         f = open('%s/%s' % (self.settings['config_path'],self.settings['filename_stations']), 'w')
         f.write('<?xml version="1.0"?>\n')
         f.write('<data>\n')
         for genre,station,url in stationlist:
            #print (genre)
            #print (type(genre))
            #print (station)
            #print (type(station))
            #print (url)
            #print (type(url))
            f.write('\t<stations>\n' + '\t\t<genre>' + genre + '</genre>\n'  + '\t\t<station>' + station + '</station>\n'  + '\t\t<url>' + url +  '</url>\n' +  '\t</stations>\n')
         f.write('</data>\n')
         f.close()



   def clean_shutdown(self):

      self.log.debug('start')

      if hasattr(self, 'notebook_tab_converter'):

         if self.notebook_tab_converter.obj_timer_file2flac is not None:
            GLib.source_remove(self.notebook_tab_converter.obj_timer_file2flac)

         if self.notebook_tab_converter.obj_timer_pwrecord is not None:
            GLib.source_remove(self.notebook_tab_converter.obj_timer_pwrecord)

         if self.notebook_tab_converter.obj_timer_file2mp3 is not None:
            GLib.source_remove(self.notebook_tab_converter.obj_timer_file2mp3)

         if self.notebook_tab_converter.obj_timer_you2mp3 is not None:
            GLib.source_remove(self.notebook_tab_converter.obj_timer_you2mp3)


      if hasattr(self, 'notebook_tab_musicplayer'):

         if self.notebook_tab_musicplayer.player:
            self.notebook_tab_musicplayer.player.set_state(Gst.State.NULL)

         if self.notebook_tab_musicplayer.obj_timer_slider is not None:
            GLib.source_remove(self.notebook_tab_musicplayer.obj_timer_slider)

         if self.notebook_tab_musicplayer.obj_timer_play_time is not None:
            GLib.source_remove(self.notebook_tab_musicplayer.obj_timer_play_time)

         if self.notebook_tab_musicplayer.obj_timer_auto_play is not None:
            GLib.source_remove(self.notebook_tab_musicplayer.obj_timer_auto_play)



      if hasattr(self, 'notebook_tab_streamripper'):

         if self.notebook_tab_streamripper.obj_timer_streamripper is not None:
            GLib.source_remove(self.notebook_tab_streamripper.obj_timer_streamripper)


      self.process_all_killer()

      if os.path.exists('%s/%s' % (self.settings['config_path'],self.settings['filename_ipcport'])):
         os.remove('%s/%s' % (self.settings['config_path'],self.settings['filename_ipcport']))



   def ReSize(self, widget, data):

      (width,height) = self.get_size()
      (position_x, position_y) = self.get_position()

      self.settings['size_x'] = str(width)
      self.settings['size_y'] = str(height)
      self.settings['position_x'] = str(position_x)
      self.settings['position_y'] = str(position_y)



   def process_all_killer(self):
   
      self.log.debug('start')

      for item in self.process_database:
         if self.process_database[item]['status']=='active':
            try:
               os.kill(int(self.process_database[item]['pid']), signal.SIGINT)
               sleep(0.05)
            except:
               pass

      self.log.debug('ends')



   def file_scan(self, directories, extensions):

      allfiles = []

      for item in directories:

         self.log.debug('item: %s' % item)

         for ext in extensions:

            self.log.debug('ext: %s' % ext)

            if os.path.isdir(item):
               for filename in os.listdir(item):

                  self.log.debug('filename: %s' % filename)

                  if filename.endswith('.' + ext):
                     pitem = item + '/' + filename
                     if os.path.isfile(pitem):
                        allfiles.extend([pitem])

      # reverse
      if len(allfiles)>=1:
         allfiles=allfiles[::-1]

      return allfiles




   def process_job_identifier_killer(self, job, identifier):

      self.log.debug('start job: %s identifier: %s' % (job,identifier))

      for pnum in self.process_database:

         self.log.debug('status: %s' % self.process_database[pnum]['status'])
         if self.process_database[pnum]['status']=='active':

            self.log.debug('job: %s' % self.process_database[pnum]['job'])
            if self.process_database[pnum]['job']==job:

               self.log.debug('identifier: %s' % self.process_database[pnum]['identifier'])
               if self.process_database[pnum]['identifier']==identifier:

                  pid=''
                  try:
                     pid=int(self.process_database[pnum]['pid'])
                     os.kill(pid, signal.SIGINT)
                     self.process_database[pnum]['status']='killed'
                     self.log.debug('job: %s pid: %s killed' % (self.process_database[pnum]['job'],pid))
                  except:
                     self.log.debug('job: %s cannot kill pid: %s' % (self.process_database[pnum]['job'],pid))




   def process_job_killer(self, job):

      self.log.debug('start job: %s' % job)

      for pnum in self.process_database:

         self.log.debug('status: %s' % self.process_database[pnum]['status'])
         if self.process_database[pnum]['status']=='active':

            self.log.debug('job: %s' % self.process_database[pnum]['job'])
            if self.process_database[pnum]['job']==job:

               pid=''
               try:
                  pid=int(self.process_database[pnum]['pid'])
                  os.kill(pid, signal.SIGINT)
                  self.process_database[pnum]['status']='killed'
                  self.log.debug('job: %s pid: %s killed' % (self.process_database[pnum]['job'],pid))
               except:
                  self.log.debug('job: %s cannot kill pid: %s' % (self.process_database[pnum]['job'],pid))





   def process_starter(self, cmd=[], cwd='', job='', identifier='', source=''):

      self.log.debug('start')

      self.pnum+=1
      k = {self.pnum: { 'status': 'active',
                        'job': job,
                        'todo': '',
                        'source': source,
                        'identifier': identifier,
                        'output': []}}

      self.process_database.update(k)

      try:
         thread = Thread(target=self.process, args=(cmd, cwd, self.pnum, self.process_database))
         thread.setDaemon(True)
         thread.start()
      except Exception as e:
         self.log.debug('error: %s' % str(e))




   def process(self, cmd=[], cwd='', pnum='', p_database={}):

      self.log.debug('cmd: %s cwd: %s' % (cmd,cwd))

      output_list=[]
      output_str=''
      process_pid=''
      i=0

      # cmd: ['streamripper', 'http://stream.freefm.de:8100/listen.pls', '-u', 'WinampMPEG/5.0', '-d', '/Music/Streamripper']
      # cwd: /Music/Streamripper


      try:
 
         process = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, close_fds=True)

         # add PID
         self.log.debug('pid %s' % process.pid)

         p_database[pnum]['pid']=process.pid


         while True:

            line = process.stdout.readline(20)

            line = line.decode('utf-8', 'ignore')

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

                  self.log.debug('break')
                  break


         wait_erg=process.wait()
         if wait_erg==0:
            p_database[pnum]['result']=True
         else:
            p_database[pnum]['result']=False

      except Exception as e:
         self.log.debug('error: %s job: %s' % (str(e),p_database[pnum]['job']))


      self.log.debug('job %s done' % p_database[pnum]['job'])

      p_database[pnum]['todo']='result'



   def ipc_server(self):

      self.log.debug('start')

      if not os.path.exists(self.settings['config_path']):
         os.mkdir(self.settings['config_path'], 0o755)

      for num in range(0,10):

         self.settings['ipc_port'] = str(int(self.settings['ipc_port']) + num)

         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('localhost', int(self.settings['ipc_port'])))
            sock.listen(1)
            with open('%s/%s' % (self.settings['config_path'],self.settings['filename_ipcport']),'w') as f:
               f.write(self.settings['ipc_port'])
               f.close()
               self.log.debug('write %s/%s' % (self.settings['config_path'],self.settings['filename_ipcport']))
            break
         except:
            self.log.debug('thread port is probably blocked -> try next port')


      self.log.debug('thread listen on port: %s' % self.settings['ipc_port'])


      try:

         while True:

            (connection, client_address) = sock.accept()
            
            receive_data=True

            while receive_data:
               data = connection.recv(130)
               if data:
                  data = data.decode()

                  self.log.debug('thread received "%s"' % data)

                  if data=='play_timer_end':
                     self.log.debug('play_timer_end')

                     self.settings['interrupt']='play_timer_end'
                     self.notebook_tab_musicplayer.player.post_message(Gst.Message.new_application(self.notebook_tab_musicplayer.player,Gst.Structure.new_empty('song-changed')))

                  elif data.startswith('play_new_file='):
                     self.log.debug('play_new_file -> bus_application_message')

                     state = self.notebook_tab_musicplayer.player.get_state(0).state

                     self.settings['interrupt']='play_new_file'
                     data=data.replace('play_new_file=','',1)
                     self.notebook_tab_musicplayer.playlist.insert(0, data)

                     if state==Gst.State.PAUSED or state==Gst.State.NULL:
                        self.notebook_tab_musicplayer.button_play.set_sensitive(False)
                        self.notebook_tab_musicplayer.play_file()


                     self.notebook_tab_musicplayer.player.post_message(Gst.Message.new_application(self.notebook_tab_musicplayer.player,Gst.Structure.new_empty('song-changed')))

               else:
                  self.log.debug('received data')
                  receive_data=False

            self.log.debug('thread wait...')


      finally:
         self.log.debug('close')
         connection.close()
