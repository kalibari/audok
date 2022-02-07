import os
import re
import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk


class TabSettings:

   def __init__(self, madmin, log, config, settings):

      self.madmin = madmin
      self.log = log
      self.config = config
      self.settings = settings

      self.box = Gtk.Box()
      self.box.set_border_width(10)


      grid = Gtk.Grid()
      grid.set_column_homogeneous(True)
      #grid.set_row_homogeneous(True)
      grid.set_row_spacing(spacing=5)


      hbox_music_new = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox_music_new.set_hexpand(True)

      image1 = Gtk.Image()
      image1.set_from_file('%s/newdir_small.png' % self.config['app_path'])
      label1 = Gtk.Label(label='Music Directory New:', xalign=0)
      label1.set_size_request(210, -1)

      label2 = Gtk.Label(label='%s/' % self.settings['music_path'], xalign=0)
      label2.set_size_request(140, -1)

      entry1 = Gtk.Entry()
      entry1.set_size_request(300, -1)
      entry1.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry1.set_text(self.settings['directory_new'])
      entry1.connect('changed', self.change_directory_new)


      hbox_music_new.pack_start(image1, False, False, 0)
      hbox_music_new.pack_start(label1, False, False, 0)
      hbox_music_new.pack_start(label2, False, False, 0)
      hbox_music_new.pack_start(entry1, False, False, 0)

      grid.add(hbox_music_new)


      hbox_music_old= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox_music_old.set_hexpand(True)

      image1 = Gtk.Image()
      image1.set_from_file('%s/olddir_small.png' % self.config['app_path'])
      label1 = Gtk.Label(label='Music Directory Old:', xalign=0)
      label1.set_size_request(210, -1)

      label2 = Gtk.Label(label='%s/' % self.settings['music_path'], xalign=0)
      label2.set_size_request(140, -1)


      entry1 = Gtk.Entry()
      entry1.set_size_request(300, -1)
      entry1.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry1.set_text(self.settings['directory_old'])
      entry1.connect('changed', self.change_directory_old)


      hbox_music_old.pack_start(image1, False, False, 0)
      hbox_music_old.pack_start(label1, False, False, 0)
      hbox_music_old.pack_start(label2, False, False, 0)
      hbox_music_old.pack_start(entry1, False, False, 0)

      grid.attach_next_to(hbox_music_old, hbox_music_new, Gtk.PositionType.BOTTOM, 1, 1)



      hbox_streamripper= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/streamripperdir_small.png' % self.config['app_path'])
      label1 = Gtk.Label(label='Streamripper Directory:', xalign=0)
      label1.set_size_request(210, -1)

      label2 = Gtk.Label(label='%s/' % self.settings['music_path'], xalign=0)
      label2.set_size_request(140, -1)

      entry1 = Gtk.Entry()
      entry1.set_size_request(300, -1)
      entry1.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry1.set_text(self.settings['directory_str'])
      entry1.connect('changed', self.change_directory_streamripper)

      hbox_streamripper.pack_start(image1, False, False, 0)
      hbox_streamripper.pack_start(label1, False, False, 0)
      hbox_streamripper.pack_start(label2, False, False, 0)
      hbox_streamripper.pack_start(entry1, False, False, 0)

      grid.attach_next_to(hbox_streamripper, hbox_music_old, Gtk.PositionType.BOTTOM, 1, 1)


      hbox_playlist= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/playlist_small.png' % self.config['app_path'])

      label1 = Gtk.Label(label='Playlist Directory:', xalign=0)
      label1.set_size_request(210, -1)

      label2 = Gtk.Label(label='%s/' % self.settings['music_path'], xalign=0)
      label2.set_size_request(140, -1)

      entry1 = Gtk.Entry()
      entry1.set_size_request(300, -1)
      entry1.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry1.set_text(self.settings['directory_playlist'])
      entry1.connect('changed', self.change_directory_playlist)

      label3 = Gtk.Label(label='Filename:', xalign=0.5)
      label3.set_size_request(100, -1)

      entry2 = Gtk.Entry()
      entry2.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry2.set_text(self.settings['filename_playlist'])
      entry2.connect('changed', self.change_filename_playlist)

      hbox_playlist.pack_start(image1, False, False, 0)
      hbox_playlist.pack_start(label1, False, False, 0)
      hbox_playlist.pack_start(label2, False, False, 0)
      hbox_playlist.pack_start(entry1, False, False, 0)
      hbox_playlist.pack_start(label3, False, False, 0)
      hbox_playlist.pack_start(entry2, True, True, 0)

      grid.attach_next_to(hbox_playlist, hbox_streamripper, Gtk.PositionType.BOTTOM, 1, 1)



      hbox_converter_dir = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/empty_small.png' % self.config['app_path'])

      label1 = Gtk.Label(label='Converter Directory:', xalign=0)
      label1.set_size_request(210, -1)

      label2 = Gtk.Label(label='%s/' % self.settings['music_path'], xalign=0)
      label2.set_size_request(140, -1)

      entry1 = Gtk.Entry()
      entry1.set_size_request(300, -1)
      entry1.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry1.set_text(self.settings['directory_converter'])
      entry1.connect('changed', self.change_directory_converter)

      hbox_converter_dir.pack_start(image1, False, False, 0)
      hbox_converter_dir.pack_start(label1, False, False, 0)
      hbox_converter_dir.pack_start(label2, False, False, 0)
      hbox_converter_dir.pack_start(entry1, False, False, 0)

      grid.attach_next_to(hbox_converter_dir, hbox_playlist, Gtk.PositionType.BOTTOM, 1, 1)



      hbox_filename_pwrecord = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/empty_small.png' % self.config['app_path'])

      label1 = Gtk.Label(label='PWrecord Directory:', xalign=0)
      label1.set_size_request(210, -1)

      label2 = Gtk.Label(label='%s/' % self.settings['music_path'], xalign=0)
      label2.set_size_request(140, -1)

      entry1 = Gtk.Entry()
      entry1.set_size_request(300, -1)
      entry1.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry1.set_text(self.settings['directory_pwrecord'])
      entry1.connect('changed', self.change_directory_pwrecord)


      label3 = Gtk.Label('Filename:', xalign=0.5)
      label3.set_size_request(100, -1)


      entry2 = Gtk.Entry()
      entry2.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry2.set_text(self.settings['filename_pwrecord'])
      entry2.connect('changed', self.change_filename_pwrecord)


      hbox_filename_pwrecord.pack_start(image1, False, False, 0)
      hbox_filename_pwrecord.pack_start(label1, False, False, 0)
      hbox_filename_pwrecord.pack_start(label2, False, False, 0)
      hbox_filename_pwrecord.pack_start(entry1, False, False, 0)
      hbox_filename_pwrecord.pack_start(label3, False, False, 0)
      hbox_filename_pwrecord.pack_start(entry2, True, True, 0)


      grid.attach_next_to(hbox_filename_pwrecord, hbox_converter_dir, Gtk.PositionType.BOTTOM, 1, 1)



      hbox_pwrecord_bitrate = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/empty_small.png' % self.config['app_path'])


      label1 = Gtk.Label(label='PWrecord Bitrate:', xalign=0)
      label1.set_size_request(210, -1)


      combo1 = Gtk.ComboBoxText()
      choice_bitrate=self.settings['choice_bitrate']
      choice_active=0
      for i,item in enumerate(choice_bitrate):
         if item==self.settings['bitrate']:
            choice_active=i
         combo1.insert(i, str(i), ' ' + item + ' ')
      combo1.set_active(choice_active)
      combo1.connect('changed', self.combobox_bitrate_changed)
 

      hbox_pwrecord_bitrate.pack_start(image1, False, False, 0)
      hbox_pwrecord_bitrate.pack_start(label1, False, False, 0)
      hbox_pwrecord_bitrate.pack_start(combo1, False, False, 0)

      grid.attach_next_to(hbox_pwrecord_bitrate, hbox_filename_pwrecord, Gtk.PositionType.BOTTOM, 1, 1)



      hbox_device_pwrecord = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)


      image1 = Gtk.Image()
      image1.set_from_file('%s/empty_small.png' % self.config['app_path'])


      label1 = Gtk.Label(label='PWrecord Device:', xalign=0)
      label1.set_size_request(210, -1)


      self.combo_pwrecord = Gtk.ComboBoxText()
      choice_device_pwrecord=self.settings['choice_device_pwrecord']
      choice_active=0
      for i,item in enumerate(choice_device_pwrecord):
         if item==self.settings['device_pwrecord']:
            choice_active=i
         self.combo_pwrecord.insert(i, str(i), item)
      self.combo_pwrecord.set_active(choice_active)
      self.combo_pwrecord.connect('changed', self.combobox_pwrecord_changed)
      #self.combo_pwrecord.set_size_request(700, 10)


      self.button_device_pwrecord_scan = Gtk.Button(label='Scan')
      self.button_device_pwrecord_scan.connect('clicked', self.button_scan_clicked)


      entry1 = Gtk.Entry()
      entry1.set_size_request(-1, 10)
      entry1.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      entry1.set_text(self.settings['directory_converter'])
      entry1.connect('changed', self.change_directory_converter)



      hbox_device_pwrecord.pack_start(image1, False, False, 0)
      hbox_device_pwrecord.pack_start(label1, False, False, 0)
      hbox_device_pwrecord.pack_start(self.combo_pwrecord, True, True, 0)
      hbox_device_pwrecord.pack_start(self.button_device_pwrecord_scan, False, False, 0)


      grid.attach_next_to(hbox_device_pwrecord, hbox_pwrecord_bitrate, Gtk.PositionType.BOTTOM, 1, 1)

      button_reset = Gtk.Button(label='Reset')
      button_reset.connect('clicked', self.button_reset_clicked)
      button_reset.set_size_request(100, -1)


      hbox_reset = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
      hbox_reset.pack_start(button_reset, False, False, 0)



      self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
      self.vbox.pack_start(grid, False, False, 5)
      self.vbox.pack_start(hbox_reset, False, False, 20)





   def change_directory_new(self, event):
      self.log.debug('start')
      self.settings['directory_new'] = event.get_text().strip()
      self.madmin.notebook_tab_musicplayer.checkbutton_new_update_tooltip(directory=self.settings['directory_new'])
      self.madmin.notebook_tab_musicplayer.image_new_update_tooltip(directory=self.settings['directory_new'])
      self.madmin.notebook_tab_musicplayer.button_move_new_update_tooltip(directory=self.settings['directory_new'])



   def change_directory_old(self, event):
      self.log.debug('start')
      self.settings['directory_old'] = event.get_text().strip()
      self.madmin.notebook_tab_musicplayer.checkbutton_auto_move_update_tooltip(directory=self.settings['directory_old'])
      self.madmin.notebook_tab_musicplayer.checkbutton_old_update_tooltip(directory=self.settings['directory_old'])
      self.madmin.notebook_tab_musicplayer.image_auto_move_update_tooltip(directory=self.settings['directory_old'])
      self.madmin.notebook_tab_musicplayer.image_auto_move_update_tooltip(directory=self.settings['directory_old'])
      self.madmin.notebook_tab_musicplayer.button_move_old_update_tooltip(directory=self.settings['directory_old'])



   def change_directory_streamripper(self, event):
      self.log.debug('start')
      self.settings['directory_str'] = event.get_text().strip()
      self.madmin.notebook_tab_musicplayer.checkbutton_str_update_tooltip(directory=self.settings['directory_str'])
      self.madmin.notebook_tab_musicplayer.image_str_update_tooltip(directory=self.settings['directory_str'])



   def change_directory_playlist(self, event):
      self.log.debug('start')
      self.settings['directory_playlist'] = event.get_text().strip()
      self.madmin.notebook_tab_musicplayer.button_playlist_new_update_tooltip(filename=self.settings['filename_playlist'],directory=self.settings['directory_playlist'])



   def change_filename_playlist(self, event):
      self.log.debug('start')
      self.settings['filename_playlist'] = event.get_text().strip()
      self.madmin.notebook_tab_musicplayer.button_playlist_new_update_tooltip(filename=self.settings['filename_playlist'],directory=self.settings['directory_playlist'])



   def change_directory_converter(self, event):
      self.log.debug('start')
      self.settings['directory_converter'] = event.get_text().strip()
      self.madmin.notebook_tab_converter.button_you2mp3_update_tooltip(directory=self.settings['directory_converter'])
      self.madmin.notebook_tab_converter.button_file2mp3_update_tooltip(directory=self.settings['directory_converter'])
      self.madmin.notebook_tab_converter.button_file2flac_update_tooltip(directory=self.settings['directory_converter'])



   def change_filename_pwrecord(self, event):
      self.log.debug('start')
      self.settings['filename_pwrecord'] = event.get_text().strip()
      self.madmin.notebook_tab_converter.button_pwrecord_update_tooltip(filename=self.settings['filename_pwrecord'], directory=self.settings['directory_pwrecord'])



   def change_directory_pwrecord(self, event):
      self.log.debug('start')
      self.settings['directory_pwrecord'] = event.get_text().strip()
      self.madmin.notebook_tab_converter.button_pwrecord_update_tooltip(filename=self.settings['filename_pwrecord'], directory=self.settings['directory_pwrecord'])



   def combobox_bitrate_changed(self, event):
      self.log.debug('start')
      self.settings['bitrate'] = event.get_active_text()



   def combobox_pwrecord_changed(self, event):
      self.log.debug('start')
      self.settings['device_pwrecord'] = event.get_active_text()
      self.madmin.notebook_tab_converter.button_pwrecord_update_tooltip(filename=self.settings['filename_pwrecord'], directory=self.settings['directory_pwrecord'])



   def button_scan_clicked(self, event):
      self.log.debug('start')

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

            if idnum and node_name and media_class:
               audio_devices.extend([node_name + ':' + media_class + ':' + idnum ])



      self.settings['choice_device_pwrecord'] = []
      self.combo_pwrecord.remove_all()

      choice_active=0
      for i,dev in enumerate(audio_devices):
         if dev==self.settings['device_pwrecord']:
            choice_active=i
         self.settings['choice_device_pwrecord'].extend([dev])
         self.combo_pwrecord.insert(i, str(i), dev)
      self.combo_pwrecord.set_active(choice_active)



   def button_reset_clicked(self, event):
      self.log.debug('start')

      settings_file = self.settings['config_path'] + '/' + self.settings['filename_settings']

      self.log.debug('settings_file: %s' % settings_file)

      if os.path.exists(settings_file):
         os.remove(settings_file)

      self.madmin.on_reset_close()

