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
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('Gdk', '4.0')
gi.require_version('GstPbutils', '1.0')
from gi.repository import Gst, Gtk, GLib, Gdk, GstPbutils


class TabMusicPlayer:


   def __init__(self, madmin, log, config, settings, playlist):

      self.madmin = madmin
      self.log = log
      self.config = config
      self.settings = settings
      self.playlist = playlist

      self.select_column=''

      # initialize GStreamer
      Gst.init(None)


      self.play_time_counter = 0

      self.obj_timer_slider=None
      self.obj_timer_play_time=None
      self.obj_timer_auto_play_scan=None



      self.slider_position = 0
      self.slider_range = 300
      self.unmute = 0

      self.disable_treeview_cursor_changed=False


      self.player = Gst.ElementFactory.make('playbin3', self.config['application_id'])
      if not self.player:
         self.log.debug('ERROR: Could not create a gst player')
         self.madmin.clean_shutdown()
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
      #bus.connect('message::tag', self.bus_message_tag)


      if int(self.settings['random_time_min'])==0 and int(self.settings['random_time_max'])==0:
         self.mute(False)


      self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
      self.box.set_margin_top(5)




      self.auto_play=False

      self.selected_num = 0
      self.selected_filename = ''

      hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      # init auto_play_scan before function combobox_playtime_changed starts
      interval = self.get_auto_timer_interval()

      self.image_auto_play_scan = Gtk.Image()
      self.image_auto_play_scan.set_from_file('%s/auto_play_small.png' % self.config['app_path'])
      self.image_auto_play_scan.set_pixel_size(30)
      self.image_auto_play_scan_update_tooltip(interval=interval)

      self.checkbutton_auto_play_scan = Gtk.CheckButton()
      self.checkbutton_auto_play_scan.set_active(False)
      self.checkbutton_auto_play_scan.connect('toggled', self.checkbutton_auto_play_scan_toggled)
      self.checkbutton_auto_play_scan_update_tooltip(interval=interval)




      label1 = Gtk.Label(label='Play Time')
      label1.set_margin_start(5)
      label1.set_xalign(0)
      self.combo_play_time = Gtk.ComboBoxText()
      choice_active=0
      choice_play_time = self.settings['choice_play_time']
      for i,item in enumerate(choice_play_time):
         if item==self.settings['play_time']:
            choice_active=i
         self.combo_play_time.insert(i, str(i), item)
      self.combo_play_time.connect('changed', self.combobox_playtime_changed)
      self.combo_play_time.set_active(choice_active)


      label2 = Gtk.Label(label='Random Start')
      label2.set_margin_start(5)
      label2.set_xalign(0)
      self.combo_random = Gtk.ComboBoxText()
      choice_active=0
      choice_random_time = self.settings['choice_random_time']
      for i,item in enumerate(choice_random_time):
         if item==self.settings['random_time_min'] and item==self.settings['random_time_max']:
            choice_active=i
         elif item==self.settings['random_time_min'] + '-' + self.settings['random_time_max']:
            choice_active=i
         self.combo_random.insert(i, str(i), item) 
      self.combo_random.connect('changed', self.combobox_random_changed)
      self.combo_random.set_active(choice_active)


      self.image_auto_move = Gtk.Image()
      self.image_auto_move.set_from_file('%s/auto_olddir_small.png' % self.config['app_path'])
      self.image_auto_move.set_pixel_size(30)
      self.image_auto_move_update_tooltip(directory=self.settings['directory_old'])
      self.image_auto_move.set_margin_start(5)


      self.checkbutton_auto_move = Gtk.CheckButton()
      self.checkbutton_auto_move.set_active(False)
      self.checkbutton_auto_move.connect('toggled', self.checkbutton_auto_move_toggled)
      self.checkbutton_auto_move_update_tooltip(directory=self.settings['directory_old'])
      self.checkbutton_auto_move.set_margin_start(5)

      button_scan = Gtk.Button(label='Scan')
      button_scan.connect('clicked', self.button_scan_clicked)
      button_scan.set_tooltip_text('Scan Directories')
      button_scan.set_margin_start(5)

      button_clear = Gtk.Button(label='Clear')
      button_clear.connect('clicked', self.button_clear_all_clicked)
      button_clear.set_tooltip_text('Clear Playlist')
      button_clear.set_margin_start(5)

      self.image_str = Gtk.Image()
      self.image_str.set_pixel_size(30)
      self.image_str.set_from_file('%s/streamripperdir_small.png' % self.config['app_path'])
      self.image_str.set_margin_start(5)
      self.image_str_update_tooltip(directory=self.settings['directory_str'])


      self.checkbutton_str = Gtk.CheckButton()
      if self.settings['checkbutton_str']=='True':
         self.checkbutton_str.set_active(True)
      else:
         self.checkbutton_str.set_active(False)
      self.checkbutton_str.connect('toggled', self.checkbutton_str_toggled)
      self.checkbutton_str_update_tooltip(directory=self.settings['directory_str'])

      self.image_new = Gtk.Image()
      self.image_new.set_pixel_size(30)
      self.image_new.set_from_file('%s/newdir_small.png' % self.config['app_path'])
      self.image_new.set_margin_start(5)
      self.image_new_update_tooltip(directory=self.settings['directory_new'])

      self.checkbutton_new = Gtk.CheckButton()
      if self.settings['checkbutton_new']=='True':
         self.checkbutton_new.set_active(True)
      else:
         self.checkbutton_new.set_active(False)
      self.checkbutton_new.connect('toggled', self.checkbutton_new_toggled)
      self.checkbutton_new.set_margin_start(5)
      self.checkbutton_new_update_tooltip(directory=self.settings['directory_new'])

      self.image_old = Gtk.Image()
      self.image_old.set_pixel_size(30)
      self.image_old.set_from_file('%s/olddir_small.png' % self.config['app_path'])
      self.image_old.set_margin_start(5)
      self.image_old_update_tooltip(directory=self.settings['directory_old'])

      self.checkbutton_old = Gtk.CheckButton()
      if self.settings['checkbutton_old']=='True':
         self.checkbutton_old.set_active(True)
      else:
         self.checkbutton_old.set_active(False)
      self.checkbutton_old.connect('toggled', self.checkbutton_old_toggled)
      self.checkbutton_old_update_tooltip(directory=self.settings['directory_old'])


      self.entry_file_sum = Gtk.Entry()
      self.entry_file_sum.set_width_chars(8)
      self.entry_file_sum.set_margin_start(5)


      hbox1.append(label1)
      hbox1.append(self.combo_play_time)
      hbox1.append(label2)
      hbox1.append(self.combo_random)
      hbox1.append(self.image_auto_move)
      hbox1.append(self.checkbutton_auto_move)
      hbox1.append(self.image_auto_play_scan)
      hbox1.append(self.checkbutton_auto_play_scan)
      hbox1.append(button_scan)
      hbox1.append(self.image_str)
      hbox1.append(self.checkbutton_str)
      hbox1.append(self.image_new)
      hbox1.append(self.checkbutton_new)
      hbox1.append(self.image_old)
      hbox1.append(self.checkbutton_old)
      hbox1.append(button_clear)
      hbox1.append(self.entry_file_sum)




      hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image = Gtk.Image()
      image.set_from_file('%s/back_white.png' % self.config['app_path'])
      image.set_pixel_size(50)
      self.button_back = Gtk.Button()
      self.button_back.connect('clicked', self.button_back_clicked)
      self.button_back.set_child(image)
      self.button_back.set_tooltip_text('Back')
      self.button_back.set_margin_start(5)
      self.button_back.set_margin_bottom(15)


      image = Gtk.Image()
      image.set_from_file('%s/play_white.png' % self.config['app_path'])
      image.set_pixel_size(50)
      self.button_play = Gtk.Button()
      self.button_play.connect('clicked', self.button_play_clicked)
      self.button_play.set_child(image)
      self.button_play.set_tooltip_text('Play')
      self.button_play.set_margin_start(5)
      self.button_play.set_margin_bottom(15)


      image = Gtk.Image()
      image.set_from_file('%s/pause_white.png' % self.config['app_path'])
      image.set_pixel_size(50)
      self.button_pause = Gtk.Button()
      self.button_pause.connect('clicked', self.button_pause_clicked)
      self.button_pause.set_child(image)
      self.button_pause.set_tooltip_text('Pause')
      self.button_pause.set_margin_start(5)
      self.button_pause.set_margin_bottom(15)


      image = Gtk.Image()
      image.set_from_file('%s/stop_white.png' % self.config['app_path'])
      image.set_pixel_size(50)
      self.button_stop = Gtk.Button()
      self.button_stop.connect('clicked', self.button_stop_clicked)
      self.button_stop.set_child(image)
      self.button_stop.set_tooltip_text('Stop')
      self.button_stop.set_margin_start(5)
      self.button_stop.set_margin_bottom(15)



      image = Gtk.Image()
      image.set_from_file('%s/next_white.png' % self.config['app_path'])
      image.set_pixel_size(50)
      self.button_next = Gtk.Button()
      self.button_next.connect('clicked', self.button_next_clicked)
      self.button_next.set_child(image)
      self.button_next.set_tooltip_text('Next')
      self.button_next.set_margin_start(5)
      self.button_next.set_margin_bottom(15)


      image = Gtk.Image()
      image.set_from_file('%s/olddir.png' % self.config['app_path'])
      image.set_pixel_size(50)
      self.button_move_old = Gtk.Button()
      self.button_move_old.connect('clicked', self.button_move_old_clicked)
      self.button_move_old.set_child(image)
      self.button_move_old.set_margin_start(20)
      self.button_move_old.set_margin_bottom(15)
      self.button_move_old_update_tooltip(directory=self.settings['directory_old'])


      image = Gtk.Image()
      image.set_from_file('%s/newdir.png' % self.config['app_path'])
      image.set_pixel_size(50)
      self.button_move_new = Gtk.Button()
      self.button_move_new.connect('clicked', self.button_move_new_clicked)
      self.button_move_new.set_child(image)
      self.button_move_new.set_margin_start(5)
      self.button_move_new.set_margin_bottom(15)
      self.button_move_new.new_from_icon_name('%s/newdir.png' % self.config['app_path'])
      self.button_move_new_update_tooltip(directory=self.settings['directory_new'])


      image = Gtk.Image()
      image.set_from_file('%s/playlist.png' % self.config['app_path'])
      image.set_pixel_size(50)
      self.button_create_playlist = Gtk.Button()
      self.button_create_playlist.set_child(image)
      self.button_create_playlist.connect('clicked', self.button_playlist_clicked)
      self.button_create_playlist.set_margin_start(20)
      self.button_create_playlist.set_margin_bottom(15)
      self.button_playlist_new_update_tooltip(filename=self.settings['filename_playlist'], directory=self.settings['directory_playlist'])


      hbox2.append(self.button_back)
      hbox2.append(self.button_play)
      hbox2.append(self.button_pause)
      hbox2.append(self.button_stop)
      hbox2.append(self.button_next)
      hbox2.append(self.button_move_old)
      hbox2.append(self.button_move_new)
      hbox2.append(self.button_create_playlist)





      hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      adjustment = Gtk.Adjustment()
      #adjustment.set_lower(0)
      #adjustment.set_step_increment(10)
      adjustment.set_page_increment(10)
      #adjustment.set_page_size(10)

      self.h_scale1 = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)

      self.h_scale1.set_digits(0)
      self.h_scale1.set_hexpand(True)
      #self.h_scale1.set_has_origin(True)
      #self.h_scale1.set_show_fill_level(True)
      #self.h_scale1.set_restrict_to_fill_level(False)
      #self.h_scale1.set_draw_value(True)
      #self.h_scale1.set_sensitive(True)
      self.h_scale1.set_margin_bottom(15)
      self.h_scale1_update = self.h_scale1.connect('change-value', self.slider_change)

      hbox3.append(self.h_scale1)




      hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image = Gtk.Image()
      image.set_from_file('%s/empty_small2.png' % self.config['app_path'])

      button_filename_tag = Gtk.Button()
      button_filename_tag.connect('clicked', self.on_link_play_file_clicked)
      button_filename_tag.set_child(image)
      button_filename_tag.set_tooltip_text('Filename / Tag')
      button_filename_tag.set_margin_start(5)
      button_filename_tag.set_margin_bottom(10)
      button_filename_tag.set_margin_end(20)
      context_button_filename_tag = button_filename_tag.get_style_context()
      context_button_filename_tag.add_class("circular")
      #context_button_filename_tag.add_class("whitebutton")

      hbox4.append(button_filename_tag)


      self.label_play_file = Gtk.Label()
      self.label_play_file.set_use_markup(True)
      self.label_play_file.set_margin_start(10)
      self.label_play_file.set_margin_bottom(10)
      self.label_play_file.set_margin_end(20)

      hbox4.append(self.label_play_file)



      self.label_file_info = Gtk.Label()
      self.label_file_info.set_use_markup(True)
      self.label_file_info.set_margin_bottom(10)

      hbox4.append(self.label_file_info)



      self.liststore = Gtk.ListStore(str, str, str)

      self.treeview = Gtk.TreeView(model=self.liststore)


      renderer_num = Gtk.CellRendererText()
      self.column_num = Gtk.TreeViewColumn('Num', renderer_num, text=0)
      self.treeview.append_column(self.column_num)


      render_filename = Gtk.CellRendererText()
      render_filename.set_fixed_size(800, 30)
      self.column_filename = Gtk.TreeViewColumn('Filename', render_filename, text=1)
      self.column_filename.set_expand(True)
      self.treeview.append_column(self.column_filename)


      renderer_pixbuf = Gtk.CellRendererPixbuf()
      self.column_clear = Gtk.TreeViewColumn('Clear', renderer_pixbuf, icon_name=2)
      self.treeview.append_column(self.column_clear)


      self.treeview.connect('row-activated', self.treeview_row_activated)
      self.treeview.connect('cursor-changed', self.treeview_cursor_changed)

      #self.treeview.enable_model_drag_source(start_button_mask, targets, actions)
      #self.treeview.enable_model_drag_dest(self.treeview_drag, gtk.gdk.ACTION_LINK)

      self.treeview.set_headers_clickable(False)
      #self.treeview.set_activate_on_single_click(True)
      self.treeview.set_margin_start(5)

      scrolledwindow = Gtk.ScrolledWindow()
      scrolledwindow.set_vexpand(True)
      scrolledwindow.set_hexpand(True)
      scrolledwindow.set_child(self.treeview)


      self.box.append(hbox1)
      self.box.append(hbox2)
      self.box.append(hbox3)
      self.box.append(hbox4)
      self.box.append(scrolledwindow)


      if self.config['check_new_file']:
         filename = self.config['check_new_file']
         if filename.endswith('.m3u'):
            self.update_playlist_listmodel(do='prepend', filename=filename, fm='m3u')
         else:
            self.update_playlist_listmodel(do='prepend', filename=filename)


      if self.selected_num<len(self.playlist):
         self.selected_filename = self.playlist[self.selected_num]
         self.play_file(num=self.selected_num, filename=self.selected_filename)
         self.update_playlist_listmodel(do='cursor', num=0)


      self.entry_file_sum.set_text('%s' % len(self.playlist))
      self.update_control_play_buttons()
      self.update_move_buttons()




   def update_label_play(self, clear=False):

      num, filename, tag = self.config['play_num_filename_tag']
      text=''
      if clear==False:

         if self.settings['label_play_show_tag']=='1':
            text='%s - %s' % ((num+1),tag)
         else:
            fn = os.path.basename(filename)
            text='%s - %s' % ((num+1),fn)

      fontsize=12500
      self.label_play_file.set_markup('<span font_size="{}">{}</span>'.format(fontsize,GLib.markup_escape_text(text)))


      duration, bitrate, codec = self.config['play_duration_bitrate_codec']
      text=''
      if clear==False:

         if duration>1000000000 and codec:

            match = re.findall(r'\((.*?)\)', codec)
            if match:
               codec=', '.join(match)


            if bitrate>1000:
               text='[%s / %sk / %ss]' % (codec,int(bitrate/1000),int(duration/1000000000))
            else:
               text='[%s / %ss]' % (codec,int(duration/1000000000))

      fontsize=9000
      self.label_file_info.set_markup('<span font_size="{}">{}</span>'.format(fontsize,GLib.markup_escape_text(text)))




   def slider_change(self, scroll, value, user_data):
      self.log.debug('start user_data: %s' % user_data)
      self.player_seek(slider_value=user_data)




   def bus_message_check(self, bus, message):
      self.log.debug('start %s' % message.type)



   def bus_player_error(self, bus, msg):
      self.log.debug('start')

      err, dbg = msg.parse_error()

      self.log.debug('error: %s' % err.message)

      self.player.set_state(Gst.State.NULL)



   def bus_player_eos(self, bus, msg):
      self.log.debug('start')
      self.next_song()



   def bus_message_tag(self, bus, message):
      self.log.debug('start')



   def bus_application_message(self, bus, message):

      message_name = message.get_structure().get_name()

      self.log.debug('start %s' % message_name)

      if message_name == 'next-song':
         self.next_song()

      elif message_name == 'new-file':
         filename = self.config['check_new_file']

         # reset
         self.config['check_new_file']=''

         if filename.endswith('.m3u'):
            self.update_playlist_listmodel(do='prepend', filename=filename, fm='m3u')
         else:
            self.update_playlist_listmodel(do='prepend', filename=filename)

         if len(self.playlist)>0:
            self.play_file(num=0, filename=self.playlist[0])

            self.update_playlist_listmodel(do='cursor', num=0)
            self.entry_file_sum.set_text('%s' % len(self.playlist))
            self.update_control_play_buttons()
            self.update_move_buttons()





   def update_playlist_listmodel(self, do='extend', num=0, filename='', fm='mp3'):
      self.log.debug('start do: %s num: %s filename: %s fm: %s' % (do,num,filename,fm))

      ########
      if do=='extend' and fm=='mp3':
         self.playlist.extend([filename])
         n = len(self.playlist)
         self.disable_treeview_cursor_changed=True
         self.liststore.insert_with_values(n-1, (0, 1, 2), (n, filename, 'list-remove'))
         self.disable_treeview_cursor_changed=False


      ########
      elif do=='prepend' and fm=='mp3':
         self.playlist.insert(0, filename)
         self.disable_treeview_cursor_changed=True
         for row in self.liststore:
            row[0]=str(int(row[0])+1)
         self.liststore.insert_with_values(num, (0, 1, 2), (num+1, filename, 'list-remove'))
         self.disable_treeview_cursor_changed=False


      ########
      elif do=='prepend' and fm=='m3u':

         m3u_playlist = []
         with open(filename,'r') as f:
            m3u_playlist = f.readlines()

         prepend_playlist = []
         for item in m3u_playlist:
            item=item.strip()
            if os.path.isfile(item):
               prepend_playlist.extend([item])

         len_prepend_playlist = len(prepend_playlist)

         prepend_playlist.extend(self.playlist)
         self.playlist = prepend_playlist


         self.disable_treeview_cursor_changed=True
         for row in self.liststore:
            row[0]=str(int(row[0])+len_prepend_playlist)

         for n,f in enumerate(prepend_playlist):
            self.liststore.insert_with_values(n, (0, 1, 2), (n+1, f, 'list-remove'))
         self.disable_treeview_cursor_changed=False



      ########
      elif do=='remove' and fm=='mp3':

         self.playlist.remove(filename)

         self.disable_treeview_cursor_changed=True

         i=0
         for row in self.liststore:
            if i>=num:
               row[0]=str(int(row[0])-1)
            i+=1

         TreeIter = self.liststore.get_iter(num)
         self.liststore.remove (TreeIter)

         self.disable_treeview_cursor_changed=False



      ########
      elif do=='clear':
         self.disable_treeview_cursor_changed=True
         self.liststore.clear()
         self.disable_treeview_cursor_changed=False



      ########
      elif do=='cursor':
         self.disable_treeview_cursor_changed=True
         self.treeview.set_cursor(num)
         self.disable_treeview_cursor_changed=False






   def timer_play_time_start(self):
      self.log.debug('start play_time: %s' % self.settings['play_time'])

      self.play_time_counter=0

      self.timer_play_time_stop(debug=False)

      self.obj_timer_play_time = GLib.timeout_add(1000, self.timer_play_time_function)



   def timer_play_time_stop(self, debug=True):
      if debug==True:
         self.log.debug('start')

      if self.obj_timer_play_time is not None:
         GLib.source_remove(self.obj_timer_play_time)
         self.obj_timer_play_time=None



   def timer_play_time_function(self):

      if self.play_time_counter>=int(self.settings['play_time']):

         try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', int(self.settings['ipc_port'])))
            sock.sendall('next-song'.encode())
         except Exception as e:
            self.log.debug('error: %s' % str(e))
         finally:
            sock.close()
            self.play_time_counter=0


      self.play_time_counter+=1

      return True



   def timer_slider_start(self):
      self.log.debug('start')

      self.timer_slider_stop(debug=False)

      self.obj_timer_slider = GLib.timeout_add(1000, self.timer_slider_function)



   def timer_slider_stop(self, debug=True):
      if debug==True:
         self.log.debug('start')

      if self.obj_timer_slider is not None:
         GLib.source_remove(self.obj_timer_slider)
         self.obj_timer_slider=None



   def timer_slider_function(self):

      state = self.player.get_state(0).state

      if state == Gst.State.PLAYING or state == Gst.State.READY:

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




   def timer_auto_play_scan_stop(self, debug=True):
      if debug==True:
         self.log.debug('start')

      if self.obj_timer_auto_play_scan is not None:
         GLib.source_remove(self.obj_timer_auto_play_scan)
         self.obj_timer_auto_play_scan=None



   def timer_auto_play_scan_start(self):
      self.log.debug('start')

      self.play_time_counter=0
      interval = self.get_auto_timer_interval() * 990

      self.timer_auto_play_scan_stop(debug=False)

      self.obj_timer_auto_play_scan = GLib.timeout_add(interval, self.timer_auto_play_scan_function)



   def get_auto_timer_interval(self):
      interval = int(self.settings['play_time'])
      if interval<10:
         interval=60
      return interval



   def timer_auto_play_scan_function(self):

      state = self.player.get_state(0).state

      self.log.debug('start state: %s' % state)

      self.playlist_scan(add_only_new=True)

      if state == Gst.State.PLAYING or state == Gst.State.READY:
         num, filename, tag = self.config['play_num_filename_tag']
         self.update_playlist_listmodel(do='cursor', num=num, filename=filename)

      else:
         if self.auto_play==True and len(self.playlist)>0:

            self.selected_num=0

            if self.selected_num<len(self.playlist):
               self.selected_filename=self.playlist[self.selected_num]
               self.play_file(num=self.selected_num, filename=self.selected_filename)
               self.update_playlist_listmodel(do='cursor', num=self.selected_num, filename=self.selected_filename)

      self.update_control_play_buttons()
      self.update_move_buttons()

      return True



   def update_move_buttons(self):

      self.selected_filename=''
      if self.selected_num < len(self.playlist):
         self.selected_filename=self.playlist[self.selected_num]

      self.log.debug('start selected_num: %s len(self.playlist): %s' % (self.selected_num,len(self.playlist)))


      if len(self.playlist)==0:
         self.button_move_old.set_sensitive(False)
         self.button_move_new.set_sensitive(False)

      else:

         start_dir_new=0
         start_dir_old=0
         start_dir_str=0


         dir_new = self.config['music_path'] + '/' + self.settings['directory_new']
         dir_old = self.config['music_path'] + '/' + self.settings['directory_old']
         dir_str = self.config['music_path'] + '/' + self.settings['directory_str']


         if self.selected_filename.startswith(dir_new):
            start_dir_new=len(dir_new)

         if self.selected_filename.startswith(dir_old):
            start_dir_old=len(dir_old)

         if self.selected_filename.startswith(dir_str):
            start_dir_str=len(dir_str)


         self.log.debug('start_dir_new: %s start_dir_old: %s start_dir_str: %s' % (start_dir_new,start_dir_old,start_dir_str))


         if start_dir_new and start_dir_old and start_dir_str:
            if start_dir_new>start_dir_old and start_dir_new>start_dir_str:
               self.button_move_new.set_sensitive(False)
               self.button_move_old.set_sensitive(True)

            elif start_dir_old>start_dir_new and start_dir_old>start_dir_str:
               self.button_move_old.set_sensitive(False)
               self.button_move_new.set_sensitive(True)

            elif start_dir_str>start_dir_old and start_dir_str>start_dir_new:
               self.button_move_old.set_sensitive(True)
               self.button_move_new.set_sensitive(True)

         elif start_dir_new and start_dir_old:
            if start_dir_new>start_dir_old:
               self.button_move_new.set_sensitive(False)
               self.button_move_old.set_sensitive(True)

            elif start_dir_old>start_dir_new:
               self.button_move_old.set_sensitive(False)
               self.button_move_new.set_sensitive(True)

         elif start_dir_new and start_dir_str:
            if start_dir_new>start_dir_str:
               self.button_move_new.set_sensitive(False)
               self.button_move_old.set_sensitive(True)

            elif start_dir_str>start_dir_new:
               self.button_move_old.set_sensitive(True)
               self.button_move_new.set_sensitive(True)


         elif start_dir_old and start_dir_str:
            if start_dir_old>start_dir_str:
               self.button_move_old.set_sensitive(False)
               self.button_move_new.set_sensitive(True)

            elif start_dir_str>start_dir_old:
               self.button_move_new.set_sensitive(True)
               self.button_move_old.set_sensitive(True)


         elif start_dir_new:
            self.button_move_new.set_sensitive(False)
            self.button_move_old.set_sensitive(True)

         elif start_dir_old:
            self.button_move_old.set_sensitive(False)
            self.button_move_new.set_sensitive(True)

         elif start_dir_str:
            self.button_move_new.set_sensitive(True)
            self.button_move_old.set_sensitive(True)



   def update_control_play_buttons(self):

      state = self.player.get_state(0).state

      self.log.debug('start state: %s len(self.playlist): %s' % (state,len(self.playlist)))

      if state == Gst.State.PLAYING or state == Gst.State.READY:

         self.button_pause.set_sensitive(True)
         self.button_stop.set_sensitive(True)
         self.button_play.set_sensitive(False)

         if len(self.playlist)==1:
            self.button_back.set_sensitive(False)
            self.button_next.set_sensitive(False)
            self.button_create_playlist.set_sensitive(True)

         elif len(self.playlist)>=1:
            self.button_back.set_sensitive(True)
            self.button_next.set_sensitive(True)
            self.button_create_playlist.set_sensitive(True)

         else:
            self.button_back.set_sensitive(False)
            self.button_next.set_sensitive(False)
            self.button_pause.set_sensitive(False)
            self.button_create_playlist.set_sensitive(False)


      elif state == Gst.State.PAUSED:
         self.button_pause.set_sensitive(False)
         self.button_stop.set_sensitive(False)
         self.button_back.set_sensitive(False)
         self.button_next.set_sensitive(False)

         if len(self.playlist)==1:
            self.button_play.set_sensitive(True)
            self.button_create_playlist.set_sensitive(True)

         elif len(self.playlist)>=1:
            self.button_play.set_sensitive(True)
            self.button_create_playlist.set_sensitive(True)

         else:
            self.button_play.set_sensitive(False)
            self.button_create_playlist.set_sensitive(False)


      else:
         self.button_pause.set_sensitive(False)
         self.button_stop.set_sensitive(False)

         if len(self.playlist)==1:
            self.button_back.set_sensitive(False)
            self.button_next.set_sensitive(False)
            self.button_play.set_sensitive(True)
            self.button_create_playlist.set_sensitive(True)

         elif len(self.playlist)>=1:
            self.button_back.set_sensitive(True)
            self.button_next.set_sensitive(True)
            self.button_play.set_sensitive(True)
            self.button_create_playlist.set_sensitive(True)

         else:
            self.button_play.set_sensitive(False)
            self.button_back.set_sensitive(False)
            self.button_next.set_sensitive(False)
            self.button_create_playlist.set_sensitive(False)




   def playlist_scan(self, add_only_new=False):

      self.log.debug('start add_only_new: %s' % add_only_new)

      directories = []

      # New
      if self.checkbutton_new.get_active()==True:
         d = self.config['music_path'] + '/' + self.settings['directory_new']
         if os.path.isdir(d):
            directories.extend([d])

      # Old
      if self.checkbutton_old.get_active()==True:
         d = self.config['music_path'] + '/' + self.settings['directory_old']
         if os.path.isdir(d):
            directories.extend([d])

      # Streamripper
      if self.checkbutton_str.get_active()==True:
         d = self.config['music_path'] + '/' + self.settings['directory_str']
         if os.path.isdir(d):
            directories.extend([d])
            for o in os.listdir(d):
               directories.extend([d + '/' + o])


      extensions = self.config['supported_audio_files']

      allfiles = self.madmin.file_scan(directories, extensions)



      if add_only_new==True:
         for item in allfiles:
            if not item in self.playlist:
               self.update_playlist_listmodel(do='extend', filename=item)

      else:
         for item in allfiles:
            self.update_playlist_listmodel(do='extend', filename=item)



      # check playlist
      for i,item in enumerate(self.playlist):
         if not os.path.exists(item):
            self.update_playlist_listmodel(do='remove', num=i, filename=item)


      self.entry_file_sum.set_text('%s' % len(self.playlist))




   def analyze_stream(self):

      artist=''
      title=''
      duration=0
      bitrate=0
      codec=''

      uri = self.player.get_property('uri')         
      self.discoverer = GstPbutils.Discoverer()

      info = self.discoverer.discover_uri(uri)

      duration = info.get_duration()

      audio_streams = info.get_audio_streams()
      for stream in audio_streams:

         bitrate = stream.get_bitrate()
         taglist =  stream.get_tags()

         for x in range(taglist.n_tags()):
            name = taglist.nth_tag_name(x)
            if name=='artist' or name=='title' or name=='audio-codec':
               res, value = taglist.get_string(name)
               if res==True:
                  if name=='artist':
                     artist=value
                  elif name=='title':
                     title=value
                  elif name=='audio-codec':
                     codec=value

      self.log.debug('artist: %s title: %s duration: %s bitrate: %s codec: %s' % (artist,title,duration,bitrate,codec))

      return (artist,title,duration,bitrate,codec)



   def mute(self, value):
      self.log.debug('value: %s' % value)
      self.player.set_property('mute', value)



   def bus_async_done_message(self, bus, message):

      """
      successful query duration once the pipeline is prerolled (so state >= PAUSED) -> async done message
      """

      if int(self.settings['random_time_min'])>0 and int(self.settings['random_time_max'])>0:
         self.mute(True)


      for x in range(0,50):
         ret1, pos = self.player.query_position(Gst.Format.TIME)
         sleep(0.02)
         if ret1==True:
            ret2, drt = self.player.query_duration(Gst.Format.TIME)
            self.log.debug('loop: %s ret1: %s ret2: %s' % (x,ret1,ret2))
            if ret2==True:
               self.slider_position = pos / Gst.SECOND
               self.slider_range = drt / Gst.SECOND
               break
            else:
               sleep(0.02)
         else:
            self.log.debug('loop: %s ret1: %s' % (x,ret1))


      self.h_scale1.set_range(0, self.slider_range)
      self.h_scale1.set_value(self.slider_position)

      if int(self.settings['random_time_min'])>0 and int(self.settings['random_time_max'])>0:
         slider_random_value = random.randint(int(self.settings['random_time_min']),int(self.settings['random_time_max']))
         self.player_seek(slider_value=float(slider_random_value))
         self.unmute=2

      self.log.debug('slider range: %s slider position: %s' % (self.slider_range,self.slider_position))



   def player_seek(self, slider_value=0):

      self.log.debug('slider_value: %s' % slider_value)

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
      #flags = Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT | Gst.SeekFlags.SEGMENTz
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



   def play_file(self, num=0, filename=''):

      self.log.debug('start num: %s filename: %s' % (num,filename))

      self.timer_slider_start()

      state = self.player.get_state(0).state

      # set player to ready state
      if state == Gst.State.NULL:
         self.player.set_state(Gst.State.READY)

      elif state == Gst.State.PLAYING:
         self.player.set_state(Gst.State.PAUSED)
         self.player.set_state(Gst.State.READY)


      if int(self.settings['play_time'])>0:
         self.timer_play_time_start()


      if len(self.playlist)==0:
         self.slider_position=0
         self.h_scale1.set_value(self.slider_position)

      elif len(self.playlist)>=1:

         self.player.set_property('uri', 'file://%s' % filename)

         tag='-'
         duration=0
         bitrate=0
         codec='-'

         try:
            (artist,title,duration,bitrate,codec) = self.analyze_stream()
            if artist and title:
               tag = '%s - %s' % (artist,title)
            elif artist:
               tag = '%s' % artist
            elif title:
               tag = '%s' % title
         except:
            pass

         self.config['play_num_filename_tag']=(num,filename,tag)
         self.config['play_duration_bitrate_codec']=(duration,bitrate,codec)
         self.update_label_play()


      if len(self.playlist)>=1:
         self.player.set_state(Gst.State.PLAYING)






   def on_link_play_file_clicked(self, event):
      if self.settings['label_play_show_tag']=='1':
         self.settings['label_play_show_tag']='0'
      else:
         self.settings['label_play_show_tag']='1'
      self.update_label_play()



   def pause(self):
      self.log.debug('start')
      self.timer_play_time_stop()
      self.timer_slider_stop()
      self.player.set_state(Gst.State.PAUSED)
      self.update_control_play_buttons()



   def stop(self):
      self.log.debug('start')
      self.timer_play_time_stop()
      self.timer_slider_stop()
      self.slider_position=0
      self.h_scale1.set_value(self.slider_position)
      self.player.set_state(Gst.State.NULL)
      self.config['play_num_filename_tag'] = (0,'','')
      self.config['play_duration_bitrate_codec'] = (0,'','')
      self.update_control_play_buttons()
      self.update_label_play(clear=True)



   def move(self, num, filename, dir):

      self.log.debug('num: %s filename: %s dir: %s' % (num,filename,dir))


      path=self.config['music_path'] + '/' + self.settings['directory_new']
      if dir=='old':
         path=self.config['music_path'] + '/' + self.settings['directory_old']


      if filename and os.path.exists(filename):
         try:
            head, fn = os.path.split(filename)
            if not os.path.exists(path):
               os.mkdir(path)
            self.log.debug('rename filename: %s to %s/%s' % (filename,path,fn))
            os.rename(filename,'%s/%s' % (path,fn))
         except Exception as e:
            self.log.debug('error: %s' % str(e))


      self.update_playlist_listmodel(do='remove', num=num, filename=filename)

      self.entry_file_sum.set_text('%s' % len(self.playlist))





   def treeview_row_activated(self, tree, path, column):

      if column is self.column_filename:
         self.select_column='filename'

      elif column is self.column_clear:
         self.select_column='clear'

      elif column is self.column_num:
         self.select_column='num'

      self.log.debug('select_column: %s' % self.select_column)

      path, focus_column = tree.get_cursor()
      if path and focus_column and (focus_column.get_title()=='Filename' or focus_column.get_title()=='Num'):

         item1, item2 = tree.get_selection().get_selected()
         if item1 and item2:

            self.selected_num = int(item1.get_value(item2, 0))-1
            self.selected_filename = item1.get_value(item2, 1)

            if self.selected_num<len(self.playlist):
               self.selected_filename = self.playlist[self.selected_num]
               self.play_file(num=self.selected_num, filename=self.selected_filename)

            self.update_control_play_buttons()
            self.update_move_buttons()





   def treeview_cursor_changed(self, treeview):

      if self.disable_treeview_cursor_changed==False:

         path, focus_column = treeview.get_cursor()
         if path and focus_column:

            TreeIter = self.liststore.get_iter(path)

            self.selected_num = int(self.liststore.get_value(TreeIter, 0))-1
            self.selected_filename = self.liststore.get_value(TreeIter, 1)
            button_clear = focus_column.get_title()

            self.log.debug('selected_num: %s selected_filename: %s ' % (self.selected_num,self.selected_filename))


            if button_clear=='Clear':

               if not self.selected_filename in self.playlist:
                  self.log.debug('selected_filename not in playlist')

               else:

                  self.log.debug('len playlist: %s selected_num: %s' % (len(self.playlist),self.selected_num))
                  self.update_playlist_listmodel(do='remove', num=self.selected_num, filename=self.selected_filename)

                  num, filename, tag = self.config['play_num_filename_tag']

                  if self.selected_num>num:
                     pass

                  elif self.selected_num<num:
                     num-=1
                     if num<0:
                        num=0
                     self.config['play_num_filename_tag']=(num, filename, tag)
                     self.update_label_play()

                  elif self.selected_num==num:

                     state = self.player.get_state(0).state

                     if state == Gst.State.PLAYING or state == Gst.State.READY:

                        if self.selected_num>=len(self.playlist):
                           self.selected_num-=1

                        if self.selected_num<0:
                           self.selected_num=0

                        if self.selected_num<len(self.playlist):
                           self.selected_filename = self.playlist[self.selected_num]
                           self.play_file(num=self.selected_num, filename=self.selected_filename)


                  self.update_playlist_listmodel(do='cursor', num=self.selected_num)


            if len(self.playlist)==0:
               self.update_control_play_buttons()
               self.update_move_buttons()
            self.entry_file_sum.set_text('%s' % len(self.playlist))



   def checkbutton_str_toggled(self, event):
      self.log.debug('start')
      self.settings['checkbutton_str']=str(event.get_active())



   def checkbutton_old_toggled(self, event):
      self.log.debug('start')
      self.settings['checkbutton_old']=str(event.get_active())



   def checkbutton_new_toggled(self, event):
      self.log.debug('start')
      self.settings['checkbutton_new']=str(event.get_active())



   def checkbutton_auto_move_toggled(self, event):
      self.log.debug('start')



   def checkbutton_auto_play_scan_toggled(self, event):
      self.log.debug('start')
      if event.get_active():
         self.timer_auto_play_scan_start()
         self.auto_play=True
      else:
         self.timer_auto_play_scan_stop()
         self.auto_play=False




   def combobox_playtime_changed(self, event):
      self.settings['play_time'] = event.get_active_text()

      self.log.debug('start play_time: %s' % self.settings['play_time'])

      interval = self.get_auto_timer_interval()
      self.checkbutton_auto_play_scan_update_tooltip(interval=interval)
      self.image_auto_play_scan_update_tooltip(interval=interval)

      state = self.player.get_state(0).state

      if state == Gst.State.PLAYING or state == Gst.State.READY:
         if int(self.settings['play_time'])==0:
            self.timer_play_time_stop()
         else:
            self.timer_play_time_start()

      else:
         self.timer_play_time_stop()




   def combobox_random_changed(self, event):
      self.log.debug('start active_text: %s' % event.get_active_text())

      random_min='0'
      random_max='0'
      if '-' in event.get_active_text():
         random_min, random_max = event.get_active_text().split('-')

      self.settings['random_time_min'] = random_min
      self.settings['random_time_max'] = random_max




   def button_scan_clicked(self, event):
      self.log.debug('start')

      self.playlist_scan()

      if len(self.playlist)>0:

         if self.selected_num>=len(self.playlist):
            self.selected_num=0
            self.selected_filename=self.playlist[0]

         self.update_playlist_listmodel(do='cursor', num=self.selected_num)

      self.update_control_play_buttons()
      self.update_move_buttons()



   def button_clear_all_clicked(self, event):
      self.log.debug('start')

      self.playlist = []

      self.update_playlist_listmodel(do='clear')

      self.entry_file_sum.set_text(str(len(self.playlist)))

      self.update_control_play_buttons()
      self.update_move_buttons()




   def button_play_clicked(self, event):
      self.log.debug('start selected_num: %s' % self.selected_num)

      self.auto_play=True

      if self.selected_num<len(self.playlist):
         self.selected_filename = self.playlist[self.selected_num]
         self.play_file(num=self.selected_num, filename=self.selected_filename)
         self.update_control_play_buttons()



   def next_song(self, check_move=True):

      self.log.debug('start')

      song_move=False

      if check_move==True and self.checkbutton_auto_move.get_active():
         num, filename, tag = self.config['play_num_filename_tag']
         if len(self.playlist)>0:
            self.move(num=num, filename=filename, dir='old')
            song_move=True

      if len(self.playlist)==0:
         self.timer_slider_stop()
         self.slider_position=0
         self.h_scale1.set_value(self.slider_position)
         self.player.set_state(Gst.State.NULL)
         self.config['play_num_filename_tag'] = (0,'','')
         self.config['play_duration_bitrate_codec'] = (0,'','')
         self.update_control_play_buttons()
         self.update_move_buttons()
         self.update_label_play(clear=True)

      else:
         if song_move==False:
            self.selected_num+=1
         else:
            if self.selected_num>num:
               self.selected_num-=1


         if self.selected_num>=len(self.playlist):
            self.selected_num=0

         if self.selected_num<len(self.playlist):
            self.selected_filename = self.playlist[self.selected_num]
            self.play_file(num=self.selected_num, filename=self.selected_filename)

            self.update_playlist_listmodel(do='cursor', num=self.selected_num)
            self.update_control_play_buttons()



   def button_next_clicked(self, event):
      self.log.debug('start selected_num: %s' % self.selected_num)
      self.next_song(check_move=False)



   def button_back_clicked(self, event):
      self.log.debug('start')
      if self.checkbutton_auto_move.get_active():
         self.playlist_scan()

      if len(self.playlist)>0:

         self.selected_num-=1
         if self.selected_num<0:
            self.selected_num=len(self.playlist)-1

         if self.selected_num<len(self.playlist):
            self.selected_filename = self.playlist[self.selected_num]
            self.play_file(num=self.selected_num, filename=self.selected_filename)

            self.update_playlist_listmodel(do='cursor', num=self.selected_num)
            self.update_control_play_buttons()






   def button_pause_clicked(self, event):
      self.log.debug('start')
      self.auto_play=False
      self.pause()


   def button_stop_clicked(self, event):
      self.log.debug('start')
      self.auto_play=False
      self.stop()



   def button_move_old_clicked(self, event):
      self.log.debug('start')

      num, filename, tag = self.config['play_num_filename_tag']

      self.log.debug('selected_num: %s num: %s' % (self.selected_num,num))

      change_song=False
      if self.selected_num==num:
         change_song=True

      self.log.debug('change_song: %s' % change_song)


      if self.selected_num<len(self.playlist):

         self.selected_filename = self.playlist[self.selected_num]
         self.move(num=self.selected_num, filename=self.selected_filename, dir='old')

         if self.selected_num < num:
            if num<0:
               num=0
            self.config['play_num_filename_tag']=((num-1), filename, tag)
            self.log.debug('decrease num to: %s' % (num-1))
            self.update_label_play()


      if change_song==True:
         if self.selected_num>=len(self.playlist):
            if len(self.playlist)==0:
               self.selected_num=0
            else:
               self.selected_num=len(self.playlist)-1

         if self.selected_num<len(self.playlist):
            self.selected_filename = self.playlist[self.selected_num]
            self.play_file(num=self.selected_num, filename=self.selected_filename)


      if len(self.playlist)>=1:
         self.update_playlist_listmodel(do='cursor', num=self.selected_num)

      self.update_control_play_buttons()
      self.update_move_buttons()



   def button_move_new_clicked(self, event):
      self.log.debug('start selected_num: %s' % self.selected_num)

      num, filename, tag = self.config['play_num_filename_tag']

      change_song=False
      if self.selected_num==num:
         change_song=True


      self.log.debug('change_song: %s len(self.playlist): %s' % (change_song,len(self.playlist)))


      if self.selected_num<len(self.playlist):
         self.selected_filename = self.playlist[self.selected_num]
         self.move(num=self.selected_num, filename=self.selected_filename, dir='new')


      if change_song==True:
         if self.selected_num>=len(self.playlist):
            if len(self.playlist)==0:
               self.selected_num=0
            else:
               self.selected_num=len(self.playlist)-1

         if self.selected_num<len(self.playlist):
            self.selected_filename = self.playlist[self.selected_num]
            self.play_file(num=self.selected_num, filename=self.selected_filename)


      if len(self.playlist)>=1:
         self.update_playlist_listmodel(do='cursor', num=self.selected_num)

      self.update_control_play_buttons()
      self.update_move_buttons()




   def button_playlist_clicked(self, event):
      self.log.debug('start')

      path=self.config['music_path'] + '/' + self.settings['directory_new']

      f = open(path + '/' + self.settings['filename_playlist'], 'w')
      for item in self.playlist:
         f.write('%s\n' % item)
      f.close()



   def checkbutton_auto_move_update_tooltip(self, directory):
      self.checkbutton_auto_move.set_tooltip_text('If file is finished, move to Directory: %s/%s' % (self.config['music_path'],directory))



   def image_auto_move_update_tooltip(self, directory):
      self.image_auto_move.set_tooltip_text('If file is finished, move to Directory: %s/%s' % (self.config['music_path'],directory))



   def checkbutton_old_update_tooltip(self, directory):
      self.checkbutton_old.set_tooltip_text('Scan Directory: %s/%s' % (self.config['music_path'],directory))



   def checkbutton_str_update_tooltip(self, directory):
      self.checkbutton_str.set_tooltip_text('Scan Directory: %s/%s' % (self.config['music_path'],directory))



   def image_str_update_tooltip(self, directory):
      self.image_str.set_tooltip_text('Scan Directory: %s/%s' % (self.config['music_path'],directory))



   def checkbutton_new_update_tooltip(self, directory):
      self.checkbutton_new.set_tooltip_text('Scan Directory: %s/%s' % (self.config['music_path'],directory))



   def checkbutton_auto_play_scan_update_tooltip(self, interval):
      self.checkbutton_auto_play_scan.set_tooltip_text('Auto Play, Clear and Scan Directories every: %s' % interval)



   def image_auto_play_scan_update_tooltip(self, interval):
      self.image_auto_play_scan.set_tooltip_text('Auto Play, Clear and Scan Directories every: %s' % interval)



   def image_new_update_tooltip(self, directory):
      self.image_new.set_tooltip_text('Scan Directory: %s/%s' % (self.config['music_path'],directory))



   def image_old_update_tooltip(self, directory):
      self.image_old.set_tooltip_text('Scan Directory: %s/%s' % (self.config['music_path'],directory))



   def button_move_old_update_tooltip(self, directory):
      self.button_move_old.set_tooltip_text('Move Current Music File to Directory: %s/%s' % (self.config['music_path'],directory))



   def button_move_new_update_tooltip(self, directory):
      self.button_move_new.set_tooltip_text('Move Current Music File to Directory: %s/%s' % (self.config['music_path'],directory))



   def button_playlist_new_update_tooltip(self, filename, directory):
      self.button_create_playlist.set_tooltip_text('Create a Playlist: %s in Directory: %s/%s' % (filename,self.config['music_path'],directory))
