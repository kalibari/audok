import os
import re
import sys
import random
import threading
import socket
import signal
import time
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GLib', '2.0')
from gi.repository import GLib


class TabAudioPlayer:


   def __init__(self, main, config, settings, playlist):

      self.main = main
      self.config = config
      self.settings = settings
      self.playlist = playlist


      ##################
      # initialize GStreamer
      Gst.init(None)

      self.state = Gst.State.NULL
      self.drt_queue = []
      self.duration = None
      self.start_time_s = 0

      self.player = Gst.ElementFactory.make('playbin3', self.config['name'])
      if not self.player:
         print('ERROR: Could not create a gst player')
         self.main.clean_shutdown()
         sys.exit()


      # play only audio files
      fakesink = Gst.ElementFactory.make('fakesink', 'fakesink')
      self.player.set_property('video-sink', fakesink)

      bus = self.player.get_bus()
      bus.add_signal_watch()

      bus.connect('message::error', self.bus_player_error)
      bus.connect('message::eos', self.bus_player_eos)
      bus.connect('message::state-changed', self.bus_player_state_changed)
      #bus.connect('message', self.bus_message_check)
      bus.connect("message::application", self.bus_application_message)

      self.box = Gtk.Box()
      self.box.set_border_width(10)


      #############################
      box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)


      row1 = Gtk.ListBoxRow()
      hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row1.add(hbox1)


      label1 = Gtk.Label('Play Time', xalign=0)
      self.combo_play_time = Gtk.ComboBoxText()
      choice_active=0
      choice_play_time = self.settings['choice_play_time']
      for i,item in enumerate(choice_play_time):
         if item==str(self.settings['play_time']):
            choice_active=i
         self.combo_play_time.insert(i, str(i), item)
      self.combo_play_time.connect('changed', self.combobox_playtime_changed)
      self.combo_play_time.set_active(choice_active)


      label2 = Gtk.Label('Random Start', xalign=0)
      self.combo_random = Gtk.ComboBoxText()
      choice_active=0
      choice_random_time = self.settings['choice_random_time']
      for i,item in enumerate(choice_random_time):
         if item==str(self.settings['random_time']):
            choice_active=i
         self.combo_random.insert(i, str(i), item) 
      self.combo_random.connect('changed', self.combobox_random_changed)
      self.combo_random.set_active(choice_active)


      image4 = Gtk.Image()
      image4.set_from_file('%s/auto_olddir_small.png' % self.config['app_path'])
      image4.set_tooltip_text('If file is finished, move to Directory: %s' % self.settings['directory_old'])
      self.checkbutton_auto_move = Gtk.CheckButton()
      self.checkbutton_auto_move.set_tooltip_text('If file is finished, move to Directory: %s' % self.settings['directory_old'])


      label_empty = Gtk.Label('', xalign=0)


      button5 = Gtk.Button(label='Scan')
      button5.connect('clicked', self.button_scan_clicked)
      button5.set_tooltip_text('Scan Directories')


      image6 = Gtk.Image()
      image6.set_from_file('%s/streamripperdir_small.png' % self.config['app_path'])
      image6.set_tooltip_text('Scan Directory Streamripper')
      self.checkbutton_str = Gtk.CheckButton()
      if 'checkbutton_str' in self.settings:
         self.checkbutton_str.set_active(self.settings['checkbutton_str'])
      self.checkbutton_str.set_tooltip_text('Scan Directory Streamripper')
      self.checkbutton_str.connect('toggled', self.checkbutton_str_toggled)


      image7 = Gtk.Image()
      image7.set_from_file('%s/newdir_small.png' % self.config['app_path'])
      image7.set_tooltip_text('Scan Directory New')
      self.checkbutton_new = Gtk.CheckButton()
      if 'checkbutton_new' in self.settings:
         self.checkbutton_new.set_active(self.settings['checkbutton_new'])
      self.checkbutton_new.set_tooltip_text('Scan Directory New')
      self.checkbutton_new.connect('toggled', self.checkbutton_new_toggled)


      image8 = Gtk.Image()
      image8.set_from_file('%s/olddir_small.png' % self.config['app_path'])
      image8.set_tooltip_text('Scan Directory Old')
      self.checkbutton_old = Gtk.CheckButton()
      if 'checkbutton_old' in self.settings:
         self.checkbutton_old.set_active(self.settings['heckbutton_Old'])
      self.checkbutton_old.set_tooltip_text('Scan Directory Old')
      self.checkbutton_old.connect('toggled', self.checkbutton_old_toggled)


      self.entry_file_sum = Gtk.Entry()
      self.entry_file_sum.set_text('')


      hbox1.pack_start(label1, False, False, 0)
      hbox1.pack_start(self.combo_play_time, False, False, 0)
      hbox1.pack_start(label2, False, False, 0)
      hbox1.pack_start(self.combo_random, False, False, 0)
      hbox1.pack_start(image4, False, False, 0)
      hbox1.pack_start(self.checkbutton_auto_move, False, False, 0)
      hbox1.pack_start(label_empty, False, False, 0)
      hbox1.pack_start(button5, False, False, 0)
      hbox1.pack_start(image6, False, False, 0)
      hbox1.pack_start(self.checkbutton_str, False, False, 0)
      hbox1.pack_start(image7, False, False, 0)
      hbox1.pack_start(self.checkbutton_new, False, False, 0)
      hbox1.pack_start(image8, False, False, 0)
      hbox1.pack_start(self.checkbutton_old, False, False, 0)
      hbox1.pack_start(self.entry_file_sum, False, False, 0)


      #############################
      row2 = Gtk.ListBoxRow()
      hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row2.add(hbox2)


      image = Gtk.Image()
      image.set_from_file('%s/back_white.png' % self.config['app_path'])
      self.button_back = Gtk.Button()
      self.button_back.connect('clicked', self.button_back_clicked)
      self.button_back.set_image(image)
      self.button_back.set_tooltip_text('Back')

      image = Gtk.Image()
      image.set_from_file('%s/play_white.png' % self.config['app_path'])
      self.button_play = Gtk.Button()
      self.button_play.connect('clicked', self.button_play_clicked)
      self.button_play.set_image(image)
      self.button_play.set_tooltip_text('Play')

      image = Gtk.Image()
      image.set_from_file('%s/pause_white.png' % self.config['app_path'])
      self.button_pause = Gtk.Button()
      self.button_pause.connect('clicked', self.button_pause_clicked)
      self.button_pause.set_image(image)
      self.button_pause.set_tooltip_text('Pause')

      image = Gtk.Image()
      image.set_from_file('%s/next_white.png' % self.config['app_path'])
      self.button_next = Gtk.Button()
      self.button_next.connect('clicked', self.button_next_clicked)
      self.button_next.set_image(image)
      self.button_next.set_tooltip_text('Next')

      image = Gtk.Image()
      image.set_from_file('%s/olddir.png' % self.config['app_path'])
      self.button_move_old = Gtk.Button()
      self.button_move_old.connect('clicked', self.button_moveold_clicked)
      self.button_move_old.set_image(image)
      self.button_move_old.set_tooltip_text('Move File to Directory: %s' % self.settings['directory_old'])

      image = Gtk.Image()
      image.set_from_file('%s/newdir.png' % self.config['app_path'])
      self.button_move_new = Gtk.Button()
      self.button_move_new.connect('clicked', self.button_movenew_clicked)
      self.button_move_new.set_image(image)
      self.button_move_new.set_tooltip_text('Move File to Directory: %s' % self.settings['directory_new'])


      hbox2.pack_start(self.button_back, False, False, 0)
      hbox2.pack_start(self.button_play, False, False, 0)
      hbox2.pack_start(self.button_pause, False, False, 0)
      hbox2.pack_start(self.button_next, False, False, 0)
      hbox2.pack_start(self.button_move_old, False, False, 0)
      hbox2.pack_start(self.button_move_new, False, False, 0)



      #############################
      row3 = Gtk.ListBoxRow()
      hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row3.add(hbox3)

      self.h_scale1 = Gtk.HScale.new_with_range(0, 300, 1)
      self.h_scale1.set_digits(0)
      self.h_scale1.set_hexpand(True)
      self.h_scale1_update = self.h_scale1.connect('value-changed', self.slider_change)



      hbox3.pack_start(self.h_scale1, True, True, 0)


      #############################
      row4 = Gtk.ListBoxRow()
      hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row4.add(hbox4)

      label1 = Gtk.Label('Play File')
      self.label_play_file = Gtk.Label('')

      self.infobar_play_file = Gtk.InfoBar()
      self.infobar_play_file.add(self.label_play_file)
 

      hbox4.pack_start(label1, False, False, 0)
      hbox4.pack_start(self.infobar_play_file, False, False, 0)


      #############################
      row5 = Gtk.ListBoxRow()
      hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row5.add(hbox5)




      columns = ['Num', 'Filename']

      self.scrolledwindow1 = Gtk.ScrolledWindow()
      self.listmodel1 = Gtk.ListStore(str, str)

      treeview1 = Gtk.TreeView(model=self.listmodel1)

      for i, column in enumerate(columns):
         cell = Gtk.CellRendererText()
         col = Gtk.TreeViewColumn(column, cell, text=i)
         treeview1.append_column(col)


      treeview1.connect('size-allocate', self.treeview_size_changed)
      treeview1.set_property('rules-hint', True) 
      self.scrolledwindow1.add(treeview1)


      hbox5.pack_start(self.scrolledwindow1, True, True, 0)

      box_outer.pack_start(row1, False, False, 2)
      box_outer.pack_start(row2, False, False, 2)
      box_outer.pack_start(row3, True, True, 0)
      box_outer.pack_start(row4, False, False, 0)
      box_outer.pack_start(row5, True, True, 2)
      self.box.add(box_outer)

      ###################################################################################


      if len(self.playlist)==0:
         self.button_next.set_sensitive(False)
         self.button_back.set_sensitive(False)
         self.button_play.set_sensitive(False)
         self.button_pause.set_sensitive(False)
         self.button_move_old.set_sensitive(False)
         self.button_move_new.set_sensitive(False)




   def slider_change(self, range):
      value = self.h_scale1.get_value()

      if self.config['debug']==1:
         print('def slider_change - value: %s' % value)

      #pos = self.player.query_position(Gst.Format.TIME)[1]
      pos = value * Gst.SECOND
      self.player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, pos)




   def bus_player_song_changed(self, bus, message):
      if self.config['debug']==1:
         print('def bus_player_song_changed - start %s' % message.type)



   def bus_application_message(self, bus, message):
      if self.config['debug']==1:
         print('def bus_application_message - start %s' % message.type)
      self.interrupt()



   def bus_message_check(self, bus, message):
      if self.config['debug']==1:
         print('def bus_message_check - start %s' % message.type)
      #if t == Gst.MessageType.EOS:
      #   print ('Received EOS')



   def refresh_slider(self):

      if self.state == Gst.State.NULL or self.state == Gst.State.READY or self.state == Gst.State.PAUSED:
         return True

      else:

         if self.duration is None:

            ret, drt = self.player.query_duration(Gst.Format.TIME)
            if ret:
               self.duration=drt
               set_range = self.duration / Gst.SECOND
               if self.config['debug']==1:
                  print('def refresh_slider - set range: %s' % set_range)

               self.h_scale1.set_range(0, set_range)
            else:
               self.h_scale1.set_range(0, 300)
               self.h_scale1.set_value(self.start_time_s)


         else:

            ret, drt = self.player.query_position(Gst.Format.TIME)
            if ret:

               set_slider = drt / Gst.SECOND
               self.h_scale1.handler_block(self.h_scale1_update)
               self.h_scale1.set_value(set_slider)
               self.h_scale1.handler_unblock(self.h_scale1_update)


               # eos fix
               if len(self.drt_queue)>1:
                  self.drt_queue.pop(0)
               self.drt_queue.extend([drt])

               if len(self.drt_queue)==2 and self.drt_queue[0]==self.drt_queue[1]:

                  if self.config['debug']==1:
                     print ('eos fix')

                  if self.checkbutton_auto_move.get_active():
                     self.move('old')

                  self.player.set_state(Gst.State.READY)

                  if len(self.playlist)>=2:
                     self.choose_song(choose='next')
                  elif len(self.playlist)>=1:
                     self.button_play.set_sensitive(True)


         return True




   def bus_player_error(self, bus, msg):
      if self.config['debug']==1:
         print('def bus_player_error - start')

      err, dbg = msg.parse_error()
      if self.config['debug']==1:
         print("def bus_player_error - error:", msg.src.get_name(), ":", err.message)

      self.player.set_state(Gst.State.READY)




   def bus_player_eos(self, bus, msg):
      if self.config['debug']==1:
         print('bus_player_eos - start')

      if self.checkbutton_auto_move.get_active():
         self.move('old')

      self.player.set_state(Gst.State.READY)

      if len(self.playlist)>=2:
         self.choose_song(choose='next')

      elif len(self.playlist)>=1:
         self.button_play.set_sensitive(True)



   def bus_player_state_changed(self, bus, msg):

      (old, new, pending) = msg.parse_state_changed()

      if msg.src == self.player:

         if self.config['debug']==1:
            print('def bus_player_state_changed start - new: %s old: %s' % (new,old))

         self.state = new

         if new==Gst.State.PLAYING and old==Gst.State.PAUSED:
            # refresh slider as soons as possible
            self.refresh_slider()

         elif new==Gst.State.READY and old==Gst.State.PAUSED:
            if self.config['debug']==1:
               print('def bus_player_state_changed - warning')



   def interrupt(self):

      if self.config['debug']==1:
         print ('def interrupt - start Interrupt: %s' % self.settings['Interrupt'])

      if self.settings['Interrupt']=='play_new_file':
         if self.playlist:
            self.choose_song(choose='keep')

      elif self.settings['Interrupt']=='play_timer_end':
         if self.checkbutton_auto_move.get_active():
            self.move('old')
            self.choose_song(choose='keep')
         else:
            self.choose_song(choose='next')



   def play_timer_stop(self):
      if hasattr(self, 't'):
         if self.t.is_alive():
            if self.config['debug']==1:
               print ('def play_timer_stop - cancel')
            self.t.cancel()




   def play_timer_end(self):
      if self.config['debug']==1:
         print ('def play_timer_end - start')

      try:
         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         sock.connect(('localhost', self.settings['ipc_port']))
         sock.sendall('play_timer_end'.encode())
      except Exception as e:
         if self.config['debug']==1:
            print ('def play_timer_end error: %s' % str(e))
      finally:
         sock.close()




   def play_timer_start(self):
      if self.config['debug']==1:
         print ('def play_timer_start - start with play_time: %s' % self.settings['play_time'])

      self.play_timer_stop()
      self.t = threading.Timer(int(self.settings['play_time']), self.play_timer_end)
      self.t.start()




   def playlist_scan(self):

      if self.config['debug']==1:
         print ('def playlist_scan - start')

      directories = []

      # New
      if self.checkbutton_new.get_active()==True:
         directories.extend([self.settings['music_path'] + '/' + self.settings['directory_new']])

      # Old
      if self.checkbutton_old.get_active()==True:
         directories.extend([self.settings['music_path'] + '/' + self.settings['directory_old']])

      # Streamripper
      if self.checkbutton_str.get_active()==True:
         directories.extend([self.settings['music_path'] + '/' + self.settings['directory_streamripper']])
         directories.extend([self.settings['music_path'] + '/' + self.settings['directory_streamripper'] + '/*'])


      extensions = ['mp3','wav','aac','flac']
      allfiles = self.main.file_scan(directories, extensions)

      # reset
      self.playlist = []

      for item in allfiles:
         self.playlist.extend([item])


      self.button_next.set_sensitive(False)
      self.button_back.set_sensitive(False)

      if len(self.playlist)>=1:
         filename = os.path.basename(self.playlist[self.config['play_num']])
         self.label_play_file.set_text('%s - %s' % ((self.config['play_num']+1),filename))
      else:
         self.label_play_file.set_text('')

      if self.config['debug']==1:
         print ('def playlist_scan - len(playlist): %s' % len(self.playlist))

      self.entry_file_sum.set_text(str(len(self.playlist)))




   def choose_song(self, choose='next'):

      self.duration=None

      len_playlist = len(self.playlist)


      if self.config['debug']==1:
         print ('def choose_song - start choose %s len_playlist: %s play_num: %s' % (choose,len_playlist,self.config['play_num']))


      if choose=='next' and (self.config['play_num']+1)>=len_playlist:
         if self.config['debug']==1:
            print ('def choose_song last file -> rescan')
         self.playlist_scan()
         self.config['play_num']=0

      elif choose=='back' and self.config['play_num']<=0:
         if self.config['debug']==1:
            print ('def choose_song - goto last file')
         self.playlist_scan()
         self.config['play_num']=(len_playlist-1)

      elif choose=='next':
         self.config['play_num']+=1

      elif choose=='back':
         self.config['play_num']-=1



      # change scrolled window
      if len_playlist>0:
         adj = self.scrolledwindow1.get_vadjustment()
         upper_size = adj.get_upper()
         page_size = adj.get_page_size()
         set_size = (upper_size / len_playlist) * self.config['play_num']
         if self.config['debug']==1:
            print ('def choose_song set_size: %s play_num: %s upper_size: %s page_size: %s' % (set_size,self.config['play_num'],upper_size,page_size))
         adj.set_value(set_size)


      self.play_file()



   def play_file(self, newplaylist=[]):

      if self.config['debug']==1:
         print ('def play_file start - newplaylist: %s' % newplaylist)


      if not hasattr(self, 'glib_timer_refresh_slider'):
         self.glib_timer_refresh_slider = GLib.timeout_add_seconds(1, self.refresh_slider)


      if int(self.settings['play_time'])>0:
         self.play_timer_start()


      if newplaylist:
         self.config['play_num'] = 0
         self.playlist = list(newplaylist)
         self.listmodel1.clear()


      if len(self.playlist)==0:
         self.button_move_old.set_sensitive(False)
         self.button_move_new.set_sensitive(False)

      elif len(self.playlist)==1:
         self.button_play.set_sensitive(False)
         self.button_next.set_sensitive(False)
         self.button_back.set_sensitive(False)
         self.button_move_old.set_sensitive(True)
         self.button_move_new.set_sensitive(True)

      elif len(self.playlist)>1:
         self.button_play.set_sensitive(False)
         self.button_next.set_sensitive(True)
         self.button_back.set_sensitive(True)
         self.button_move_old.set_sensitive(True)
         self.button_move_new.set_sensitive(True)





      if self.config['debug']==1:
         print ('def play_file play_num: %s state: %s len(self.playlist): %s' % (self.config['play_num'],self.state,len(self.playlist)))


      if self.state == Gst.State.PAUSED:
         pass
      else:

         self.entry_file_sum.set_text('%s' % len(self.playlist))

         self.player.set_state(Gst.State.READY)


         if self.config['debug']==1:
            print ('def play_file set state null')

         if len(self.playlist)==0:
            self.label_play_file.set_text('')
            self.button_pause.set_sensitive(False)


         elif len(self.playlist)>=1:
            filepath = os.path.realpath(self.playlist[self.config['play_num']])
            self.player.set_property("uri", "file://%s" % self.playlist[self.config['play_num']])
            filename = os.path.basename(self.playlist[self.config['play_num']])
            self.label_play_file.set_text('%s - %s' % ((self.config['play_num']+1),filename))


      if len(self.playlist)>=1:

         if self.config['debug']==1:
            print ('def play_file start playing')


         self.button_pause.set_sensitive(True)

         self.start_time_s = 0

         if self.settings['random_time']!='0':
            self.player.set_state(Gst.State.PAUSED)

            (random_t1,random_t2) = self.settings['random_time'].split('-')
            if self.config['debug']==1:
               print ('def play_file random_t1: %s random_t1: %s' % (random_t1,random_t2))
            self.start_time_s=random.randint(int(random_t1),int(random_t2))
            if self.config['debug']==1:
               print ('def play_file - start-time: %s s' % self.start_time_s)

            time.sleep(0.3)
            pos = self.start_time_s * Gst.SECOND
            self.player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, pos)


         self.player.set_state(Gst.State.PLAYING)

         if self.config['debug']==1:
            print ('def play_file set state: Gst.State.PLAYING')





   def pause(self):
      if self.config['debug']==1:
         print ('def pause start')

      self.play_timer_stop()
      self.player.set_state(Gst.State.PAUSED)




   def move(self, dir):

      play_num = self.config['play_num']
      path_filename = self.playlist[self.config['play_num']]

      if self.config['debug']==1:
         print ('def move - start - dir: %s play_num: %s path_filename: %s' % (dir,(self.config['play_num']+1),path_filename))

      path=self.settings['music_path'] + '/' + self.settings['directory_new']
      if dir=='old':
         path=self.settings['music_path'] + '/' + self.settings['directory_old']

      try:
         head, filename = os.path.split(path_filename)
         if not os.path.exists(path):
            os.mkdir(path)
         os.rename(path_filename,'%s/%s' % (path,filename))
         self.playlist_scan()
      except Exception as e:
         if self.config['debug']==1:
            print ('def move_old error: %s' % str(e))


      self.listmodel1.clear()
      for i,item in enumerate(self.playlist):
         i+=1
         self.listmodel1.append([str(i),str(item)])



   def treeview_size_changed(self, event1, event2):
      #if self.config['debug']==1:
      #   print ('def treeview_size_changed start')
      pass



   def checkbutton_str_toggled(self, event):
      if self.config['debug']==1:
         print ('def checkbutton_str_toggled - start')
      self.settings['checkbutton_str']=event.get_active()



   def checkbutton_old_toggled(self, event):
      if self.config['debug']==1:
         print ('def checkbutton_old_toggled - start')
      self.settings['checkbutton_old']=event.get_active()



   def checkbutton_new_toggled(self, event):
      if self.config['debug']==1:
         print ('def checkbutton_new_toggled - start')
      self.settings['checkbutton_new']=event.get_active()



   def combobox_playtime_changed(self, event):
      self.settings['play_time'] = event.get_active_text()

      if self.config['debug']==1:
         print ('def combobox_playtime_changed - start - play_time: %s' % self.settings['play_time'])

      if int(self.settings['play_time'])==0:
         self.play_timer_stop()
      elif self.state==Gst.State.PLAYING:
         self.play_timer_start()



   def combobox_random_changed(self, event):
      if self.config['debug']==1:
         print ('def combobox_random_changed - start - active_text: %s' % event.get_active_text())
      self.settings['random_time'] = event.get_active_text()



   def button_scan_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_scan_clicked - start')

      self.config['play_num'] = 0

      self.listmodel1.clear()

      self.play_timer_stop()

      if self.state == Gst.State.PLAYING or self.state == Gst.State.PAUSED:
         if self.config['debug']==1:
            print ('def button_scan_clicked - try to set state: %s' % Gst.State.READY)
         self.player.set_state(Gst.State.READY)

      self.playlist_scan()

      if len(self.playlist)>=1:
         self.checkbutton_auto_move.set_sensitive(True)
         self.button_play.set_sensitive(True)

         for i,item in enumerate(self.playlist):
            i+=1
            self.listmodel1.append([str(i),str(item)])



   def button_play_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_play_clicked - start')
      self.button_play.set_sensitive(False)
      self.play_file()



   def button_next_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_next_clicked - start')
      self.choose_song(choose='next')



   def button_back_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_back_clicked - start')
      self.choose_song(choose='back')



   def button_pause_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_pause_clicked - start')
      self.pause()

      self.button_pause.set_sensitive(False)
      self.button_play.set_sensitive(True)
      self.button_back.set_sensitive(False)
      self.button_next.set_sensitive(False)



   def button_moveold_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_moveold_clicked start')
      self.move('old')
      self.choose_song(choose='keep')



   def button_movenew_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_movenew_clicked start')
      self.move('new')
      self.choose_song(choose='keep')

