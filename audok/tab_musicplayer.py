import os
import re
import sys
import random
import threading
import socket
import signal
import gi
from time import sleep
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GLib', '2.0')
from gi.repository import GLib
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


class TabMusicPlayer:


   def __init__(self, main, config, settings, playlist):

      self.main = main
      self.config = config
      self.settings = settings
      self.playlist = playlist


      ######################
      # initialize GStreamer
      Gst.init(None)

      self.audio_info = ''
      self.audio_rate = ''

      self.play_time_counter = 0

      self.obj_timer_refresh_slider=None
      self.obj_timer_play_time_check=None


      self.slider_position = 0
      self.slider_range = 300
      self.unmute = 0


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
      #bus.connect('message', self.bus_message_check)
      bus.connect('message::application', self.bus_application_message)
      bus.connect('message::async-done', self.bus_async_done_message)


      if self.settings['random_time_min']==0 and self.settings['random_time_max']==0:
         self.mute(False)


      self.box = Gtk.Box()
      self.box.set_border_width(10)

      box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)


      row1 = Gtk.ListBoxRow()
      hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row1.add(hbox1)


      label1 = Gtk.Label(label='Play Time', xalign=0)
      self.combo_play_time = Gtk.ComboBoxText()
      choice_active=0
      choice_play_time = self.settings['choice_play_time']
      for i,item in enumerate(choice_play_time):
         if item==str(self.settings['play_time']):
            choice_active=i
         self.combo_play_time.insert(i, str(i), item)
      self.combo_play_time.connect('changed', self.combobox_playtime_changed)
      self.combo_play_time.set_active(choice_active)


      label2 = Gtk.Label(label='Random Start', xalign=0)
      self.combo_random = Gtk.ComboBoxText()
      choice_active=0
      choice_random_time = self.settings['choice_random_time']
      for i,item in enumerate(choice_random_time):
         if item==str(self.settings['random_time_min']) and item==str(self.settings['random_time_max']):
            choice_active=i
         elif item==str(self.settings['random_time_min']) + '-' + str(self.settings['random_time_max']):
            choice_active=i
         self.combo_random.insert(i, str(i), item) 
      self.combo_random.connect('changed', self.combobox_random_changed)
      self.combo_random.set_active(choice_active)


      self.image_auto_move = Gtk.Image()
      self.image_auto_move.set_from_file('%s/auto_olddir_small.png' % self.config['app_path'])
      self.image_auto_move_update_tooltip(directory=self.settings['directory_old'])

      self.checkbutton_auto_move = Gtk.CheckButton()
      self.checkbutton_auto_move_update_tooltip(directory=self.settings['directory_old'])


      space_label3 = Gtk.Label(label='', xalign=0)


      button_scan = Gtk.Button(label='Scan')
      button_scan.connect('clicked', self.button_scan_clicked)
      button_scan.set_tooltip_text('Scan Directories')


      self.image_str = Gtk.Image()
      self.image_str.set_from_file('%s/streamripperdir_small.png' % self.config['app_path'])
      self.image_str_update_tooltip(directory=self.settings['directory_str'])

      self.checkbutton_str = Gtk.CheckButton()
      self.checkbutton_str.set_active(self.settings['checkbutton_str'])
      self.checkbutton_str.connect('toggled', self.checkbutton_str_toggled)
      self.checkbutton_str_update_tooltip(directory=self.settings['directory_str'])

      self.image_new = Gtk.Image()
      self.image_new.set_from_file('%s/newdir_small.png' % self.config['app_path'])
      self.image_new_update_tooltip(directory=self.settings['directory_new'])

      self.checkbutton_new = Gtk.CheckButton()
      self.checkbutton_new.set_active(self.settings['checkbutton_new'])
      self.checkbutton_new.connect('toggled', self.checkbutton_new_toggled)
      self.checkbutton_new_update_tooltip(directory=self.settings['directory_new'])

      self.image_old = Gtk.Image()
      self.image_old.set_from_file('%s/olddir_small.png' % self.config['app_path'])
      self.image_old_update_tooltip(directory=self.settings['directory_old'])

      self.checkbutton_old = Gtk.CheckButton()
      self.checkbutton_old.set_active(self.settings['checkbutton_old'])
      self.checkbutton_old.connect('toggled', self.checkbutton_old_toggled)
      self.checkbutton_old_update_tooltip(directory=self.settings['directory_old'])


      self.entry_file_sum = Gtk.Entry()
      self.entry_file_sum.set_text('')


      hbox1.pack_start(label1, False, False, 0)
      hbox1.pack_start(self.combo_play_time, False, False, 0)
      hbox1.pack_start(label2, False, False, 0)
      hbox1.pack_start(self.combo_random, False, False, 0)
      hbox1.pack_start(self.image_auto_move, False, False, 0)
      hbox1.pack_start(self.checkbutton_auto_move, False, False, 0)
      hbox1.pack_start(space_label3, False, False, 0)
      hbox1.pack_start(button_scan, False, False, 0)
      hbox1.pack_start(self.image_str, False, False, 0)
      hbox1.pack_start(self.checkbutton_str, False, False, 0)
      hbox1.pack_start(self.image_new, False, False, 0)
      hbox1.pack_start(self.checkbutton_new, False, False, 0)
      hbox1.pack_start(self.image_old, False, False, 0)
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
      image.set_from_file('%s/stop_white.png' % self.config['app_path'])
      self.button_stop = Gtk.Button()
      self.button_stop.connect('clicked', self.button_stop_clicked)
      self.button_stop.set_image(image)
      self.button_stop.set_tooltip_text('Stop')


      image = Gtk.Image()
      image.set_from_file('%s/next_white.png' % self.config['app_path'])
      self.button_next = Gtk.Button()
      self.button_next.connect('clicked', self.button_next_clicked)
      self.button_next.set_image(image)
      self.button_next.set_tooltip_text('Next')

      space_label1 = Gtk.Label(label='')

      image = Gtk.Image()
      image.set_from_file('%s/olddir.png' % self.config['app_path'])
      self.button_move_old = Gtk.Button()
      self.button_move_old.connect('clicked', self.button_move_old_clicked)
      self.button_move_old.set_image(image)
      self.button_move_old_update_tooltip(directory=self.settings['directory_old'])


      image = Gtk.Image()
      image.set_from_file('%s/newdir.png' % self.config['app_path'])
      self.button_move_new = Gtk.Button()
      self.button_move_new.connect('clicked', self.button_move_new_clicked)
      self.button_move_new.set_image(image)
      self.button_move_new_update_tooltip(directory=self.settings['directory_new'])


      space_label2 = Gtk.Label(label='')

      image = Gtk.Image()
      image.set_from_file('%s/playlist.png' % self.config['app_path'])
      self.button_playlist = Gtk.Button()
      self.button_playlist.connect('clicked', self.button_playlist_clicked)
      self.button_playlist.set_image(image)
      self.button_playlist_new_update_tooltip(filename=self.settings['filename_playlist'], directory=self.settings['directory_playlist'])


      hbox2.pack_start(self.button_back, False, False, 0)
      hbox2.pack_start(self.button_play, False, False, 0)
      hbox2.pack_start(self.button_pause, False, False, 0)
      hbox2.pack_start(self.button_stop, False, False, 0)
      hbox2.pack_start(self.button_next, False, False, 0)
      hbox2.pack_start(space_label1, False, False, 10)
      hbox2.pack_start(self.button_move_old, False, False, 0)
      hbox2.pack_start(self.button_move_new, False, False, 0)
      hbox2.pack_start(space_label2, False, False, 10)
      hbox2.pack_start(self.button_playlist, False, False, 0)



      #############################

      row3 = Gtk.ListBoxRow()
      hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row3.add(hbox3)

      self.h_scale1 = Gtk.HScale()
      self.h_scale1.set_digits(0)
      self.h_scale1.set_hexpand(True)
      self.h_scale1_update = self.h_scale1.connect('change-value', self.slider_change)

      hbox3.pack_start(self.h_scale1, True, True, 0)

      #############################

      row4 = Gtk.ListBoxRow()
      hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row4.add(hbox4)

      self.label_play_file = Gtk.Label()
      self.label_play_file.set_use_markup(True)
      self.set_label_play_file('')

      hbox4.pack_start(self.label_play_file, True, True, 0)


      #############################

      row5 = Gtk.ListBoxRow()
      hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row5.add(hbox5)

      self.scrolledwindow1 = Gtk.ScrolledWindow()
      self.listmodel1 = Gtk.ListStore(str, str)

      self.treeview1 = Gtk.TreeView(model=self.listmodel1)

      columns = ['Num', 'Filename']

      for i, column in enumerate(columns):
         cell = Gtk.CellRendererText()
         col = Gtk.TreeViewColumn(column, cell, text=i)
         self.treeview1.append_column(col)


      #self.treeview1.connect('button-release-event', self.treeview_release_event)
      self.treeview1.connect('button-press-event', self.treeview_press_event)
      #self.treeview1.connect('size-allocate', self.treeview_size_changed)
      self.treeview1.set_property('rules-hint', True)
      self.scrolledwindow1.add(self.treeview1)


      hbox5.pack_start(self.scrolledwindow1, True, True, 0)

      box_outer.pack_start(row1, False, False, 2)
      box_outer.pack_start(row2, False, False, 2)
      box_outer.pack_start(row3, False, False, 0)
      box_outer.pack_start(row4, False, False, 0)
      box_outer.pack_start(row5, True, True, 2)
      self.box.add(box_outer)


      if len(self.playlist)>=1:
         self.update_playlist()

      else:
         self.button_next.set_sensitive(False)
         self.button_back.set_sensitive(False)
         self.button_play.set_sensitive(False)
         self.button_pause.set_sensitive(False)
         self.button_stop.set_sensitive(False)
         self.button_move_old.set_sensitive(False)
         self.button_move_new.set_sensitive(False)




   def set_label_play_file(self, text):
      fontsize=12000
      self.label_play_file.set_markup('<span font_size="{}">{}</span>'.format(fontsize,GLib.markup_escape_text(text)))



   def slider_change(self, scroll, value, user_data):
      if self.config['debug']==1:
         print('def slider_change - user_data: %s' % user_data)
      self.player_seek(slider_value=user_data)




   def bus_application_message(self, bus, message):
      if self.config['debug']==1:
         print('def bus_application_message - start %s' % message.type)
      self.interrupt()



   def bus_message_check(self, bus, message):
      if self.config['debug']==1:
         print('def bus_message_check - start %s' % message.type)



   def bus_player_error(self, bus, msg):
      if self.config['debug']==1:
         print('def bus_player_error - start')

      err, dbg = msg.parse_error()
      if self.config['debug']==1:
         print('def bus_player_error - error:', msg.src.get_name(), ':', err.message)

      self.player.set_state(Gst.State.NULL)
      self.player.set_state(Gst.State.READY)



   def bus_player_eos(self, bus, msg):

      if self.config['debug']==1:
         print('bus_player_eos - start')

      if self.checkbutton_auto_move.get_active():
         self.move('old')

      if self.config['debug']==1:
         print('bus_player_eos - state ready')

      self.player.set_state(Gst.State.NULL)
      self.player.set_state(Gst.State.READY)

      if self.config['debug']==1:
         print('bus_player_eos - state ready')


      if len(self.playlist)>=2:
         self.choose_song(choose='next')

      elif len(self.playlist)>=1:
         self.button_play.set_sensitive(True)



   def interrupt(self):

      if self.config['debug']==1:
         print ('def interrupt - start interrupt: %s' % self.settings['interrupt'])

      if self.settings['interrupt']=='play_new_file':
         if self.playlist:
            self.listmodel1.clear()
            self.choose_song(choose='keep')
            self.update_playlist()

      elif self.settings['interrupt']=='play_timer_end':
         if self.checkbutton_auto_move.get_active():
            self.move('old')
            self.choose_song(choose='keep')
         else:
            self.choose_song(choose='next')



   def play_timer_stop(self):

      if self.config['debug']==1:
         print ('def play_timer_stop - start')

      if self.obj_timer_play_time_check is not None:
         GLib.source_remove(self.obj_timer_play_time_check)
         self.obj_timer_play_time_check=None

      if self.obj_timer_refresh_slider is not None:
         GLib.source_remove(self.obj_timer_refresh_slider)
         self.obj_timer_refresh_slider=None



   def play_time_check(self):

      if self.play_time_counter>=self.settings['play_time']:

         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', self.settings['ipc_port']))
            sock.sendall('play_timer_end'.encode())
         except Exception as e:
            if self.config['debug']==1:
               print ('def play_timer_end error: %s' % str(e))
         finally:
            sock.close()

      else:
         self.play_time_counter+=1

      return True




   def play_timer_start(self):
      if self.config['debug']==1:
         print ('def play_timer_start - start with play_time: %s' % self.settings['play_time'])

      self.play_time_counter=0

      if self.obj_timer_play_time_check is None:
         self.obj_timer_play_time_check = GLib.timeout_add(1000, self.play_time_check)




   def playlist_scan(self):

      if self.config['debug']==1:
         print ('def playlist_scan - start')

      directories = []

      # New
      if self.checkbutton_new.get_active()==True:
         d = self.settings['music_path'] + '/' + self.settings['directory_new']
         if os.path.isdir(d):
            directories.extend([d])

      # Old
      if self.checkbutton_old.get_active()==True:
         d = self.settings['music_path'] + '/' + self.settings['directory_old']
         if os.path.isdir(d):
            directories.extend([d])

      # Streamripper
      if self.checkbutton_str.get_active()==True:
         d = self.settings['music_path'] + '/' + self.settings['directory_str']
         if os.path.isdir(d):
            directories.extend([d])
            for o in os.listdir(d):
               directories.extend([d + '/' + o])


      if self.config['debug']==1:
         print ('def playlist_scan - directories: %s' % ', '.join(directories))


      extensions = self.config['supported_audio_files']

      allfiles = self.main.file_scan(directories, extensions)


      # reset
      self.playlist = []

      for item in allfiles:
         self.playlist.extend([item])


      if self.config['debug']==1:
         print ('def playlist_scan - len(self.playlist): %s play_num: %s' % (len(self.playlist),self.config['play_num']))


      if len(self.playlist)>=1:
         filename = os.path.basename(self.playlist[self.config['play_num']])
         self.set_label_play_file('%s - %s' % ((self.config['play_num']+1),filename))
      else:
         self.set_label_play_file('')


      if self.config['debug']==1:
         print ('def playlist_scan - len(playlist): %s' % len(self.playlist))

      self.entry_file_sum.set_text(str(len(self.playlist)))




   def choose_song(self, choose='next'):

      len_playlist = len(self.playlist)

      if self.config['debug']==1:
         print ('def choose_song - play_num: %s len_playlist: %s' % (self.config['play_num'],len_playlist))


      if len_playlist==0:
         self.slider_position=0
         self.h_scale1.set_value(self.slider_position)
         self.player.set_state(Gst.State.NULL)
         self.player.set_state(Gst.State.READY)

      else:

         if choose=='next':

            if (self.config['play_num']+1)>=len_playlist:
               if self.config['debug']==1:
                  print ('def choose_song - choose: %s -> playlist_scan' % choose)
               self.playlist_scan()
               self.config['play_num']=0
            else:
               if self.config['debug']==1:
                  print ('def choose_song - choose: %s' % choose)
               self.config['play_num']+=1


         elif choose=='back':

            if self.config['play_num']==0:
               if self.config['debug']==1:
                  print ('def choose_song - choose: %s -> playlist_scan' % choose)
               self.playlist_scan()
               self.config['play_num']=len_playlist-1
            else:
               if self.config['debug']==1:
                  print ('def choose_song - choose: %s' % choose)
               self.config['play_num']-=1


         # change scrolled window
         adj = self.scrolledwindow1.get_vadjustment()
         upper_size = adj.get_upper()
         page_size = adj.get_page_size()
         set_size = (upper_size / len_playlist) * self.config['play_num']
         if self.config['debug']==1:
            print ('def choose_song - set_size: %s play_num: %s upper_size: %s page_size: %s' % (set_size,self.config['play_num'],upper_size,page_size))
         adj.set_value(set_size)


         state = self.player.get_state(0).state

         if state == Gst.State.PLAYING or state == Gst.State.READY:
            self.play_file()



   def player_start(self):
      self.treeview1.set_cursor(self.config['play_num'])
      self.player.set_state(Gst.State.PLAYING)



   def mute(self, value):
      if self.config['debug']==1:
         print('def mute - value: %s' % value)
      self.player.set_property('mute', value)



   def bus_async_done_message(self, bus, message):

      """
      successful query duration once the pipeline is prerolled (so state >= PAUSED) -> async done message
      """

      if self.settings['random_time_min']>0 and self.settings['random_time_max']>0:
         self.mute(True)


      for x in range(0,50):
         ret1, pos = self.player.query_position(Gst.Format.TIME)
         sleep(0.02)
         if ret1==True:
            ret2, drt = self.player.query_duration(Gst.Format.TIME)
            if self.config['debug']==1:
               print('def bus_async_done_message - loop: %s ret1: %s ret2: %s' % (x,ret1,ret2))
            if ret2==True:
               self.slider_position = pos / Gst.SECOND
               self.slider_range = drt / Gst.SECOND
               break
            else:
               sleep(0.02)
         else:
            if self.config['debug']==1:
               print('def bus_async_done_message - loop: %s ret1: %s' % (x,ret1))


      self.h_scale1.set_range(0, self.slider_range)
      self.h_scale1.set_value(self.slider_position)

      if self.settings['random_time_min']>0 and self.settings['random_time_max']>0:
         slider_random_value = random.randint(self.settings['random_time_min'],self.settings['random_time_max'])
         self.player_seek(slider_value=float(slider_random_value))
         self.unmute=2

      if self.config['debug']==1:
         print('def bus_async_done_message - slider range: %s slider position: %s' % (self.slider_range,self.slider_position))




   def refresh_slider(self):

      if self.player.get_state(0).state == Gst.State.PLAYING:

         self.slider_position+=1
         self.h_scale1.set_value(self.slider_position)

         if self.unmute>0:
            self.unmute-=1
            if self.unmute==0:
               value = self.player.get_property('mute')
               if value==True:
                  self.mute(False)

         return True
      else:
         return False




   def player_seek(self, slider_value=0):

      if self.config['debug']==1:
         print('def player_seek - slider_value: %s' % slider_value)

      # KEY_UNIT (4) – seek to the nearest keyframe. This might be faster but less accurate.
      # TRICKMODE (16) – when doing fast forward or fast reverse playback, allow elements to skip frames instead of generating all frames. (Since: 1.6)
      # TRICKMODE_NO_AUDIO (256) – when doing fast forward or fast reverse playback, request that audio decoder elements skip decoding and output only gap events or silence. (Since: 1.6)
      # NONE (0) – no flag
      # FLUSH (1) – flush pipeline
      # TRICKMODE_KEY_UNITS (128)
      # SEGMENT (8)

      #flags = Gst.SeekFlags.KEY_UNIT
      #flags = Gst.SeekFlags.NONE
      #flags = Gst.SeekFlags.FLUSH 
      #flags = Gst.SeekFlags.KEY_UNIT | Gst.SeekFlags.TRICKMODE
      #flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT
      #flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT | Gst.SeekFlags.SEGMENT
      flags = Gst.SeekFlags.TRICKMODE_KEY_UNITS
      self.player.seek_simple(Gst.Format.TIME, flags, slider_value * Gst.SECOND)


      # GST_SEEK_TYPE_END - relative position to duration is requested
      # GST_SEEK_TYPE_NONE - no change in position is required
      # GST_SEEK_TYPE_SET - absolute position is requested
      #seektype1 = Gst.SeekType.NONE
      #seektype2 = Gst.SeekType.SET
      #seektype3 = Gst.SeekType.END
      #self.player.seek(1.0, Gst.Format.TIME, flags, seektype2, slider_value * Gst.SECOND, seektype2, -1)

      self.slider_position=slider_value




   def play_file(self, newplaylist=[]):

      if self.config['debug']==1:
         print ('def play_file - start newplaylist: %s' % newplaylist)


      if self.obj_timer_refresh_slider is not None:
         GLib.source_remove(self.obj_timer_refresh_slider)
      self.obj_timer_refresh_slider = GLib.timeout_add(1000, self.refresh_slider)


      if self.config['debug']==1:
         print ('def play_file - obj_timer_refresh_slider: %s' % self.obj_timer_refresh_slider)


      if self.settings['play_time']>0:
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


      state = self.player.get_state(0).state


      if self.config['debug']==1:
         print ('def play_file - play_num: %s state: %s len(self.playlist): %s' % (self.config['play_num'],state,len(self.playlist)))


      if state == Gst.State.PAUSED:
         pass

      else:

         if state == Gst.State.PLAYING:
            self.player.set_state(Gst.State.READY)

         self.entry_file_sum.set_text('%s' % len(self.playlist))


         if len(self.playlist)==0:
            self.set_label_play_file('')
            self.button_pause.set_sensitive(False)
            self.button_stop.set_sensitive(False)
            self.slider_position=0
            self.h_scale1.set_value(self.slider_position)


         elif len(self.playlist)>=1:
            filepath = os.path.realpath(self.playlist[self.config['play_num']])
            if self.config['debug']==1:
               print ('def play_file - filepath: %s' % filepath)
            self.player.set_property('uri', 'file://%s' % self.playlist[self.config['play_num']])
            filename = os.path.basename(self.playlist[self.config['play_num']])
            self.set_label_play_file('%s - %s' % ((self.config['play_num']+1),filename))


      if len(self.playlist)>=1:
         self.button_pause.set_sensitive(True)
         self.button_stop.set_sensitive(True)
         if self.config['debug']==1:
            print ('def play_file - start playing')
         self.player_start()



   def pause(self):
      if self.config['debug']==1:
         print ('def pause - start')

      self.play_timer_stop()
      self.player.set_state(Gst.State.PAUSED)



   def stop(self):
      if self.config['debug']==1:
         print ('def stop - start')

      self.play_timer_stop()
      self.slider_position=0
      self.h_scale1.set_value(self.slider_position)
      self.player.set_state(Gst.State.NULL)



   def move(self, dir):

      if self.config['debug']==1:
         print ('def move - dir: %s len(self.playlist): %s play_num: %s' % (dir,len(self.playlist),self.config['play_num']))

      path_filename = self.playlist[self.config['play_num']]

      path=self.settings['music_path'] + '/' + self.settings['directory_new']
      if dir=='old':
         path=self.settings['music_path'] + '/' + self.settings['directory_old']


      try:
         head, filename = os.path.split(path_filename)
         if not os.path.exists(path):
            os.mkdir(path)
         if self.config['debug']==1:
            print ('def move - path_filename: %s' % path_filename)
         os.rename(path_filename,'%s/%s' % (path,filename))
      except Exception as e:
         if self.config['debug']==1:
            print ('def move - error: %s' % str(e))


      if len(self.playlist)==0:
         self.playlist_scan()
      else:
         if (self.config['play_num']+1)==len(self.playlist):
            del self.playlist[self.config['play_num']]
            self.config['play_num']-=1
         else:
            del self.playlist[self.config['play_num']]


      self.listmodel1.clear()
      for i,item in enumerate(self.playlist):
         self.listmodel1.append([str(i+1),str(item)])



   def treeview_size_changed(self, event1, event2):
      if self.config['debug']==1:
         print ('def treeview_size_changed - start')



   def treeview_press_event(self, view, event):
      if self.config['debug']==1:
         print ('def treeview_press_event - start')

      if event.type == Gdk.EventType.BUTTON_PRESS:
         pass

      elif event.type == Gdk.EventType._2BUTTON_PRESS:

         item1, item2 = view.get_selection().get_selected()
         if item2:
            play_num = item1.get_value(item2, 0)
            self.config['play_num'] = int(play_num) -1

         self.button_play.set_sensitive(False)
         self.play_file()



   def treeview_release_event(self, event1, event2):
      if self.config['debug']==1:
         print ('def treeview_release_event - start')



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
      self.settings['play_time'] = int(event.get_active_text())

      if self.config['debug']==1:
         print ('def combobox_playtime_changed - start play_time: %s' % self.settings['play_time'])

      state = self.player.get_state(0).state

      if int(self.settings['play_time'])==0:
         self.play_timer_stop()

      elif state==Gst.State.PLAYING:
         self.play_timer_start()



   def combobox_random_changed(self, event):
      if self.config['debug']==1:
         print ('def combobox_random_changed - start active_text: %s' % event.get_active_text())

      random_min=0
      random_max=0
      if '-' in event.get_active_text():
         random_min, random_max = event.get_active_text().split('-')

      self.settings['random_time_min'] = int(random_min)
      self.settings['random_time_max'] = int(random_max)



   def update_playlist(self):
      for i,item in enumerate(self.playlist):
         self.listmodel1.append([str(i+1),str(item)])



   def button_scan_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_scan_clicked - start')

      self.config['play_num'] = 0

      self.listmodel1.clear()

      self.play_timer_stop()
      self.playlist_scan()

      if len(self.playlist)>=1:
         self.update_playlist()

      state = self.player.get_state(0).state

      if state == Gst.State.PLAYING:
         self.button_play.set_sensitive(True)

      elif state == Gst.State.NULL or state == Gst.State.READY:
         self.button_move_old.set_sensitive(False)
         self.button_move_new.set_sensitive(False)
         self.checkbutton_auto_move.set_sensitive(True)
         self.button_play.set_sensitive(True)
         self.button_next.set_sensitive(False)
         self.button_back.set_sensitive(False)

         if len(self.playlist)>=1:
            self.button_play.set_sensitive(True)
         else:
            self.button_play.set_sensitive(False)



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
      self.button_stop.set_sensitive(False)
      self.button_play.set_sensitive(True)
      self.button_back.set_sensitive(False)
      self.button_next.set_sensitive(False)



   def button_stop_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_stop_clicked - start')
      self.stop()
      self.button_pause.set_sensitive(False)
      self.button_stop.set_sensitive(False)
      self.button_play.set_sensitive(True)
      self.button_back.set_sensitive(False)
      self.button_next.set_sensitive(False)



   def button_move_old_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_move_old_clicked - start')
      self.move('old')
      self.choose_song(choose='keep')
      if len(self.playlist)==0:
         self.button_move_old.set_sensitive(False)
         self.button_move_new.set_sensitive(False)
         self.checkbutton_auto_move.set_sensitive(False)
         self.button_play.set_sensitive(False)
         self.button_next.set_sensitive(False)
         self.button_back.set_sensitive(False)
         self.button_stop.set_sensitive(False)
         self.button_pause.set_sensitive(False)


   def button_move_new_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_move_new_clicked - start')
      self.move('new')
      self.choose_song(choose='keep')
      if len(self.playlist)==0:
         self.button_move_old.set_sensitive(False)
         self.button_move_new.set_sensitive(False)
         self.checkbutton_auto_move.set_sensitive(False)
         self.button_play.set_sensitive(False)
         self.button_next.set_sensitive(False)
         self.button_back.set_sensitive(False)
         self.button_stop.set_sensitive(False)
         self.button_pause.set_sensitive(False)



   def button_playlist_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_playlist_clicked - start')

      path=self.settings['music_path'] + '/' + self.settings['directory_new']

      f = open(path + '/' + self.settings['filename_playlist'], 'w')
      for item in self.playlist:
         f.write('%s\n' % item)
      f.close()



   def checkbutton_auto_move_update_tooltip(self, directory):
      self.checkbutton_auto_move.set_tooltip_text('If file is finished, move to Directory Old: %s' % directory)


   def image_auto_move_update_tooltip(self, directory):
      self.image_auto_move.set_tooltip_text('If file is finished, move to Directory Old: %s' % directory)


   def checkbutton_old_update_tooltip(self, directory):
      self.checkbutton_old.set_tooltip_text('Scan Directory Old: %s' % directory)


   def checkbutton_str_update_tooltip(self, directory):
      self.checkbutton_str.set_tooltip_text('Scan Directory Streamripper: %s' % directory)


   def image_str_update_tooltip(self, directory):
      self.image_str.set_tooltip_text('Scan Directory Streamripper: %s' % directory)


   def checkbutton_new_update_tooltip(self, directory):
      self.checkbutton_new.set_tooltip_text('Scan Directory New: %s' % directory)


   def image_new_update_tooltip(self, directory):
      self.image_new.set_tooltip_text('Scan Directory New: %s' % directory)


   def image_old_update_tooltip(self, directory):
      self.image_old.set_tooltip_text('Scan Directory Old: %s' % directory)


   def button_move_old_update_tooltip(self, directory):
      self.button_move_old.set_tooltip_text('Move Current Music File to Directory Old: %s' % directory)


   def button_move_new_update_tooltip(self, directory):
      self.button_move_new.set_tooltip_text('Move Current Music File to Directory New: %s' % directory)


   def button_playlist_new_update_tooltip(self, filename, directory):
      self.button_playlist.set_tooltip_text('Create a Playlist: %s for Directory: %s' % (filename,directory))
