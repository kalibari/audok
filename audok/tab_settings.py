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

   def __init__(self, main, settings):
      self.main = main
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
      image1.set_from_file('%s/newdir_small.png' % self.settings['Share_Path'])
      label1 = Gtk.Label("New:", xalign=0)
      label1.set_size_request(140, -1)

      label2 = Gtk.Label("%s/" % self.settings['Music_Path'], xalign=0)
      label2.set_size_request(140, -1)

      self.entry_input_dir_new = Gtk.Entry()
      self.entry_input_dir_new.set_size_request(-1, 10)
      self.entry_input_dir_new.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      self.entry_input_dir_new.set_text(self.settings['Directory_New'])



      hbox_dir_new.pack_start(image1, False, False, 0)
      hbox_dir_new.pack_start(label1, False, True, 0)
      hbox_dir_new.pack_start(label2, False, True, 0)
      hbox_dir_new.pack_start(self.entry_input_dir_new, True, True, 0)


      grid.attach_next_to(hbox_dir_new, hbox_directories_ad, Gtk.PositionType.BOTTOM, 1, 1)

      #############################


      hbox_dir_old= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox_dir_old.set_hexpand(True)

      image1 = Gtk.Image()
      image1.set_from_file('%s/olddir_small.png' % self.settings['Share_Path'])
      label1 = Gtk.Label("Old:", xalign=0)
      label1.set_size_request(140, -1)

      label2 = Gtk.Label("%s/" % self.settings['Music_Path'], xalign=0)
      label2.set_size_request(140, -1)


      self.entry_input_dir_old = Gtk.Entry()
      self.entry_input_dir_old.set_size_request(-1, 10)
      self.entry_input_dir_old.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      self.entry_input_dir_old.set_text(self.settings['Directory_Old'])


      hbox_dir_old.pack_start(image1, False, False, 0)
      hbox_dir_old.pack_start(label1, False, True, 0)
      hbox_dir_old.pack_start(label2, False, True, 0)
      hbox_dir_old.pack_start(self.entry_input_dir_old, True, True, 0)

      grid.attach_next_to(hbox_dir_old, hbox_dir_new, Gtk.PositionType.BOTTOM, 1, 1)


      #############################


      hbox_directory_st = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_directory_st = Gtk.Label("Streamripper Directory:", xalign=0)

      hbox_directory_st.pack_start(label_directory_st, False, False, 0)

      grid.attach_next_to(hbox_directory_st, hbox_dir_old, Gtk.PositionType.BOTTOM, 1, 1)


      #############################

      hbox_dir_st= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/streamripperdir_small.png' % self.settings['Share_Path'])
      label1 = Gtk.Label("Streamripper:", xalign=0)
      label1.set_size_request(140, -1)

      label2 = Gtk.Label("%s/" % self.settings['Music_Path'], xalign=0)
      label2.set_size_request(140, -1)

      self.entry_input_dir_st = Gtk.Entry()
      self.entry_input_dir_st.set_size_request(-1, 10)
      self.entry_input_dir_st.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      self.entry_input_dir_st.set_text(self.settings['Directory_Streamripper'])


      hbox_dir_st.pack_start(image1, False, False, 0)
      hbox_dir_st.pack_start(label1, False, True, 0)
      hbox_dir_st.pack_start(label2, False, True, 0)
      hbox_dir_st.pack_start(self.entry_input_dir_st, True, True, 0)

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
      choice_pwrecord_device=self.settings['Choice_Pwrecord_Device']
      choice_active=0
      for i,item in enumerate(choice_pwrecord_device):
         if item==self.settings['Pwrecord_Device']:
            choice_active=i
         self.combo_pwrecord.insert(i, str(i), item)
      self.combo_pwrecord.set_active(choice_active)
      self.combo_pwrecord.connect("changed", self.PWRECORD_COMBOBOX)



      self.button_pwrecord_device_scan = Gtk.Button(label="Scan")
      self.button_pwrecord_device_scan.connect("clicked", self.PWRECORD_DEVICE_SCAN_BUTTON)
      self.button_pwrecord_device_scan.set_size_request(100, -1)


      label_empty = Gtk.Label("", xalign=0)
      label_empty.set_size_request(165, -1)

      label_pwrecord = Gtk.Label("PWrecord Device:", xalign=0)
      label_pwrecord.set_size_request(160, -1)

      label_bitrate = Gtk.Label("Bitrate:", xalign=0)
      label_bitrate.set_size_request(80, -1)

      combo_bitrate = Gtk.ComboBoxText()
      choice_bitrate=self.settings['Choice_Bitrate']
      choice_active=0
      for i,item in enumerate(choice_bitrate):
         if item==self.settings['Bitrate']:
            choice_active=i
         combo_bitrate.insert(i, str(i), item)
      combo_bitrate.set_active(choice_active)
      combo_bitrate.connect("changed", self.BITRATE_COMBOBOX)
 
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

      hbox_window = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_window = Gtk.Label("Window:", xalign=0)

      hbox_window.pack_start(label_window, False, False, 0)

      grid.attach_next_to(hbox_window, hbox_converter, Gtk.PositionType.BOTTOM, 1, 1)

      #############################

      hbox_window_sp = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)


      self.checkbutton_window_size = Gtk.CheckButton('Save Size')
      self.checkbutton_window_size.set_active(1)


      self.checkbutton_window_position = Gtk.CheckButton('Save Position')
      self.checkbutton_window_position.set_active(1)

      hbox_window_sp.pack_start(self.checkbutton_window_size, False, True, 0)
      hbox_window_sp.pack_start(self.checkbutton_window_position, True, True, 0)

      grid.attach_next_to(hbox_window_sp, hbox_window, Gtk.PositionType.BOTTOM, 1, 1)

      #############################


      # empty box for space
      hbox_space = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      grid.attach_next_to(hbox_space, hbox_window, Gtk.PositionType.BOTTOM, 1, 2)


      #############################

      hbox_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      
      self.button_save = Gtk.Button(label="Save")
      self.button_save.connect("clicked", self.SAVE_BUTTON)

      self.button_reset = Gtk.Button(label="Reset")
      self.button_reset.connect("clicked", self.RESET_BUTTON)

      hbox_buttons.pack_start(self.button_save, False, True, 0)
      hbox_buttons.pack_start(self.button_reset, False, True, 0)


      grid.attach_next_to(hbox_buttons, hbox_space, Gtk.PositionType.BOTTOM, 1, 1)


      #############################

      self.box.add(grid)




   def BITRATE_COMBOBOX(self, event):
      if self.settings['Debug']==1:
         print ('def BITRATE_COMBOBOX - start')

      self.settings['Bitrate'] = event.get_active_text()



   def PWRECORD_COMBOBOX(self, event):
      if self.settings['Debug']==1:
         print ('def PWRECORD_COMBOBOX - start')

      self.settings['Pwrecord_Device'] = event.get_active_text()



   def PWRECORD_DEVICE_SCAN_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def PWRECORD_DEVICE_SCAN_BUTTON - start')

      audio_devices = set()

      out = subprocess.check_output([self.settings['Bin_Pwcli'],'list-objects'])
      if out:
         output=out.decode('utf-8').split('\n')

         for item in output:
            x = re.search('^\s*node\.name\ \=\ "(.*)"\s*$', str(item))
            if x and x.group(1):
               if 'alsa' in x.group(1):
                  audio_devices.add(x.group(1))


      self.settings['Choice_Pwrecord_Device'] = []
      self.combo_pwrecord.remove_all()

      choice_active=0
      for i,item in enumerate(list(audio_devices)):
         if item==self.settings['Pwrecord_Device']:
            choice_active=i
         self.settings['Choice_Pwrecord_Device'].extend([item])
         self.combo_pwrecord.insert(i, str(i), item)
      self.combo_pwrecord.set_active(choice_active)




   def SAVE_BUTTON(self, event):
      
      if self.settings['Debug']==1:
         print ('def SAVE_BUTTON - start')

      files = main.Files()
      file_settings = files.get_default_file_settings(self.settings)

      file_settings['Pwrecord_Device'] = self.settings['Pwrecord_Device']
      file_settings['Bitrate'] = self.settings['Bitrate']
      file_settings['Choice_Pwrecord_Device'] = self.settings['Choice_Pwrecord_Device']


      file_settings['Directory_New'] = self.entry_input_dir_new.get_text()
      file_settings['Directory_Old'] = self.entry_input_dir_old.get_text()
      file_settings['Directory_Streamripper'] = self.entry_input_dir_st.get_text()

      self.settings['Directory_New'] = file_settings['Directory_New']
      self.settings['Directory_Old'] = file_settings['Directory_Old']
      self.settings['Directory_Streamripper'] = file_settings['Directory_Streamripper']


      if self.checkbutton_window_position.get_active()==True:
         file_settings['Position_X'] = self.settings['Position_X']
         file_settings['Position_Y'] = self.settings['Position_Y']

      if self.checkbutton_window_size.get_active()==True:
         file_settings['Size_X'] = self.settings['Size_X']
         file_settings['Size_Y'] = self.settings['Size_Y']


      files.update_file_settings(self.settings, file_settings)





   def RESET_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def RESET_BUTTON - start')

      if os.path.exists('%s/%s' % (self.settings['Config_Path'],self.settings['Filename_Settings'])):
         os.remove('%s/%s' % (self.settings['Config_Path'],self.settings['Filename_Settings']))

      self.main.on_reset_close()

