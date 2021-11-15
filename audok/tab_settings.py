import os
import re
import gi
import subprocess
import main
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GObject


class TabSettings:

   def __init__(self, main, config, settings):

      self.main = main
      self.config = config
      self.settings = settings

      self.box = Gtk.Box()
      self.box.set_border_width(10)

      grid = Gtk.Grid()
      grid.set_column_homogeneous(True)
      grid.set_row_homogeneous(True)

      #############################

      hbox_directories_ad = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_directories_ad = Gtk.Label("Music Directories:", xalign=0)

      hbox_directories_ad.pack_start(label_directories_ad, False, False, 0)

      grid.add(hbox_directories_ad)

      #############################

      hbox_dir_new= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox_dir_new.set_hexpand(True)


      image1 = Gtk.Image()
      image1.set_from_file('%s/newdir_small.png' % self.config['app_path'])
      label1 = Gtk.Label("New:", xalign=0)
      label1.set_size_request(140, -1)

      label2 = Gtk.Label("%s/" % self.settings['music_path'], xalign=0)
      label2.set_size_request(140, -1)

      entry_input_dir_new = Gtk.Entry()
      entry_input_dir_new.set_size_request(-1, 10)
      entry_input_dir_new.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry_input_dir_new.set_text(self.settings['directory_new'])
      entry_input_dir_new.connect('changed', self.change_directory_new)


      hbox_dir_new.pack_start(image1, False, False, 0)
      hbox_dir_new.pack_start(label1, False, True, 0)
      hbox_dir_new.pack_start(label2, False, True, 0)
      hbox_dir_new.pack_start(entry_input_dir_new, True, True, 0)


      grid.attach_next_to(hbox_dir_new, hbox_directories_ad, Gtk.PositionType.BOTTOM, 1, 1)

      #############################


      hbox_dir_old= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox_dir_old.set_hexpand(True)

      image1 = Gtk.Image()
      image1.set_from_file('%s/olddir_small.png' % self.config['app_path'])
      label1 = Gtk.Label("Old:", xalign=0)
      label1.set_size_request(140, -1)

      label2 = Gtk.Label("%s/" % self.settings['music_path'], xalign=0)
      label2.set_size_request(140, -1)


      entry_input_dir_old = Gtk.Entry()
      entry_input_dir_old.set_size_request(-1, 10)
      entry_input_dir_old.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry_input_dir_old.set_text(self.settings['directory_old'])
      entry_input_dir_old.connect('changed', self.change_directory_old)


      hbox_dir_old.pack_start(image1, False, False, 0)
      hbox_dir_old.pack_start(label1, False, True, 0)
      hbox_dir_old.pack_start(label2, False, True, 0)
      hbox_dir_old.pack_start(entry_input_dir_old, True, True, 0)

      grid.attach_next_to(hbox_dir_old, hbox_dir_new, Gtk.PositionType.BOTTOM, 1, 1)


      #############################


      hbox_directory_st = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_directory_st = Gtk.Label("Streamripper Directory:", xalign=0)

      hbox_directory_st.pack_start(label_directory_st, False, False, 0)

      grid.attach_next_to(hbox_directory_st, hbox_dir_old, Gtk.PositionType.BOTTOM, 1, 1)


      #############################

      hbox_dir_st= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/streamripperdir_small.png' % self.config['app_path'])
      label1 = Gtk.Label("Streamripper:", xalign=0)
      label1.set_size_request(140, -1)

      label2 = Gtk.Label("%s/" % self.settings['music_path'], xalign=0)
      label2.set_size_request(140, -1)

      entry_input_dir_st = Gtk.Entry()
      entry_input_dir_st.set_size_request(-1, 10)
      entry_input_dir_st.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry_input_dir_st.set_text(self.settings['directory_str'])
      entry_input_dir_st.connect('changed', self.change_directory_str)


      hbox_dir_st.pack_start(image1, False, False, 0)
      hbox_dir_st.pack_start(label1, False, True, 0)
      hbox_dir_st.pack_start(label2, False, True, 0)
      hbox_dir_st.pack_start(entry_input_dir_st, True, True, 0)

      grid.attach_next_to(hbox_dir_st, hbox_directory_st, Gtk.PositionType.BOTTOM, 1, 1)


      #############################

      hbox_coverter = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_coverter = Gtk.Label("Converter:", xalign=0)

      hbox_coverter.pack_start(label_coverter, False, False, 0)

      grid.attach_next_to(hbox_coverter, hbox_dir_st, Gtk.PositionType.BOTTOM, 1, 1)


      #############################


      hbox_converter= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_pwrecord = Gtk.Label("PWrecord Devices:", xalign=0)
      label_pwrecord.set_size_request(160, -1)


      self.combo_pwrecord = Gtk.ComboBoxText()
      choice_pwrecord_device=self.settings['choice_pwrecord_device']
      choice_active=0
      for i,item in enumerate(choice_pwrecord_device):
         if item==self.settings['pwrecord_default']:
            choice_active=i
         self.combo_pwrecord.insert(i, str(i), item)
      self.combo_pwrecord.set_active(choice_active)
      self.combo_pwrecord.connect("changed", self.combobox_pwrecord_changed)



      self.button_pwrecord_device_scan = Gtk.Button(label="Scan")
      self.button_pwrecord_device_scan.connect("clicked", self.button_scan_clicked)
      self.button_pwrecord_device_scan.set_size_request(100, -1)


      label_empty = Gtk.Label("", xalign=0)
      label_empty.set_size_request(165, -1)

      label_pwrecord = Gtk.Label("PWrecord Device:", xalign=0)
      label_pwrecord.set_size_request(160, -1)

      label_bitrate = Gtk.Label("Bitrate:", xalign=0)
      label_bitrate.set_size_request(80, -1)


      combo_bitrate = Gtk.ComboBoxText()
      choice_bitrate=self.settings['choice_bitrate']
      choice_active=0
      for i,item in enumerate(choice_bitrate):
         if item==self.settings['bitrate']:
            choice_active=i
         combo_bitrate.insert(i, str(i), item)
      combo_bitrate.set_active(choice_active)
      combo_bitrate.connect("changed", self.combobox_bitrate_changed)
 


      label_empty = Gtk.Label("", xalign=0)
      label_empty.set_size_request(60, -1)

      hbox_converter.pack_start(label_pwrecord, False, False, 0)
      hbox_converter.pack_start(self.combo_pwrecord, False, False, 0)
      hbox_converter.pack_start(self.button_pwrecord_device_scan, False, False, 0)
      hbox_converter.pack_start(label_empty, False, False, 0)
      hbox_converter.pack_start(label_bitrate, False, False, 0)
      hbox_converter.pack_start(combo_bitrate, False, False, 0)

      grid.attach_next_to(hbox_converter, hbox_coverter, Gtk.PositionType.BOTTOM, 1, 1)



      #############################

      # empty box for space
      hbox_window = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      grid.attach_next_to(hbox_window, hbox_converter, Gtk.PositionType.BOTTOM, 1, 1)

      #############################

      # empty box for space
      hbox_space = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      grid.attach_next_to(hbox_space, hbox_window, Gtk.PositionType.BOTTOM, 1, 2)


      #############################
      hbox_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      
      self.button_reset = Gtk.Button(label="Reset")
      self.button_reset.connect("clicked", self.button_reset_clicked)

      hbox_buttons.pack_start(self.button_reset, False, True, 0)

      grid.attach_next_to(hbox_buttons, hbox_space, Gtk.PositionType.BOTTOM, 1, 1)

      #############################

      self.box.add(grid)



   def change_directory_new(self, event):
      if self.config['debug']==1:
         print ('def change_directory_new - start')
      self.settings['directory_new'] = event.get_text()



   def change_directory_old(self, event):
      if self.config['debug']==1:
         print ('def change_directory_old - start')
      self.settings['directory_old'] = event.get_text()



   def change_directory_str(self, event):
      if self.config['debug']==1:
         print ('def change_directory_str - start')
      self.settings['directory_str'] = event.get_text()



   def combobox_bitrate_changed(self, event):
      if self.config['debug']==1:
         print ('def combobox_bitrate_changed - start')
      self.settings['bitrate'] = event.get_active_text()



   def combobox_pwrecord_changed(self, event):
      if self.config['debug']==1:
         print ('def combobox_pwrecord_changed - start')
      self.settings['pwrecord_default'] = event.get_active_text()



   def button_scan_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_scan_clicked - start')


      audio_devices = []

      out = subprocess.check_output([self.config['bin_pwcli'],'list-objects'])
      if out:
         output=out.decode('utf-8').split('\n')

         idnum=0
         node_name=''
         media_class=''

         for item in output:

            x = re.search('^\s+id (\d+),', item)
            if x and x.group(1):
               idnum=x.group(1)
               node_name=''
               media_class=''

            x = re.search('node\.name\ \=\ "(.*)"\s*$', item)
            if x and x.group(1):
               node_name=x.group(1)

            x = re.search('media\.class\ \=\ "(.*)"\s*$', item)
            if x and x.group(1):
               if 'audio' in x.group(1).lower():
                  media_class=x.group(1)

            #if idnum and node_name and media_class:
            #   audio_devices.extend([node_name + ':' + media_class + ':' + idnum ])



      self.settings['choice_pwrecord_device'] = []
      self.combo_pwrecord.remove_all()

      choice_active=0
      for i,dev in enumerate(audio_devices):
         if dev==self.settings['pwrecord_default']:
            choice_active=i
         self.settings['choice_pwrecord_device'].extend([dev])
         self.combo_pwrecord.insert(i, str(i), dev)
      self.combo_pwrecord.set_active(choice_active)





   def button_reset_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_reset_clicked - start')

      settings_file = self.settings['config_path'] + '/' + self.settings['filename_settings']

      if self.config['debug']==1:
         print ('def button_reset_clicked - settings_file: %s' % settings_file)

      if os.path.exists(settings_file):
         os.remove(settings_file)

      self.main.on_reset_close()

