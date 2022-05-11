import os
import re
import gi
import subprocess
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from shutil import which


class TabSettings:

   def __init__(self, madmin, log, config, settings):

      self.madmin = madmin
      self.log = log
      self.config = config
      self.settings = settings


      grid = Gtk.Grid()
      grid.set_column_homogeneous(True)
      #grid.set_row_homogeneous(True)
      grid.set_row_spacing(spacing=5)
      grid.set_margin_top(5)


      hbox_music_new = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox_music_new.set_hexpand(True)


      image1 = Gtk.Image()
      image1.set_from_file('%s/newdir_small.png' % self.config['app_path'])
      image1.set_margin_start(5)
      image1.set_pixel_size(30)

      label1 = Gtk.Label(label='Music Directory New:')
      label1.set_margin_start(5)
      label1.set_size_request(205, -1)
      label1.set_xalign(0)



      label2 = Gtk.Label(label='%s/' % self.config['music_path'])
      label2.set_margin_start(5)
      label2.set_size_request(130, -1)
      label2.set_xalign(0)

      entry1 = Gtk.Entry()
      entry1.set_text(self.settings['directory_new'])
      entry1.connect('changed', self.change_directory_new)


      hbox_music_new.append(image1)
      hbox_music_new.append(label1)
      hbox_music_new.append(label2)
      hbox_music_new.append(entry1)

      grid.attach(hbox_music_new, 1, 1, 1, 1)


      hbox_music_old = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox_music_old.set_hexpand(True)

      image1 = Gtk.Image()
      image1.set_from_file('%s/olddir_small.png' % self.config['app_path'])
      image1.set_margin_start(5)
      image1.set_pixel_size(30)

      label1 = Gtk.Label(label='Music Directory Old:')
      label1.set_size_request(205, -1)
      label1.set_margin_start(5)
      label1.set_xalign(0)

      label2 = Gtk.Label(label='%s/' % self.config['music_path'])
      label2.set_size_request(130, -1)
      label2.set_margin_start(5)
      label2.set_xalign(0)


      entry1 = Gtk.Entry()
      entry1.set_text(self.settings['directory_old'])
      entry1.connect('changed', self.change_directory_old)


      hbox_music_old.append(image1)
      hbox_music_old.append(label1)
      hbox_music_old.append(label2)
      hbox_music_old.append(entry1)


      grid.attach_next_to(hbox_music_old, hbox_music_new, Gtk.PositionType.BOTTOM, 1, 1)


      hbox_streamripper = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/streamripperdir_small.png' % self.config['app_path'])
      image1.set_margin_start(5)
      image1.set_pixel_size(30)

      label1 = Gtk.Label(label='Streamripper Directory:')
      label1.set_size_request(205, -1)
      label1.set_margin_start(5)
      label1.set_xalign(0)

      label2 = Gtk.Label(label='%s/' % self.config['music_path'])
      label2.set_size_request(130, -1)
      label2.set_margin_start(5)
      label2.set_xalign(0)


      entry1 = Gtk.Entry()
      entry1.set_text(self.settings['directory_str'])
      entry1.connect('changed', self.change_directory_streamripper)



      hbox_streamripper.append(image1)
      hbox_streamripper.append(label1)
      hbox_streamripper.append(label2)
      hbox_streamripper.append(entry1)



      grid.attach_next_to(hbox_streamripper, hbox_music_old, Gtk.PositionType.BOTTOM, 1, 1)


      hbox_playlist = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/playlist_small.png' % self.config['app_path'])
      image1.set_margin_start(5)
      image1.set_pixel_size(30)

      label1 = Gtk.Label(label='Playlist Directory:')
      label1.set_size_request(205, -1)
      label1.set_margin_start(5)
      label1.set_xalign(0)

      label2 = Gtk.Label(label='%s/' % self.config['music_path'])
      label2.set_size_request(130, -1)
      label2.set_margin_start(5)
      label2.set_xalign(0)


      entry1 = Gtk.Entry()
      entry1.set_size_request(300, -1)
      entry1.set_text(self.settings['directory_playlist'])
      entry1.connect('changed', self.change_directory_playlist)

      label3 = Gtk.Label(label='Filename:')
      label3.set_size_request(100, -1)
      label3.set_xalign(0.5)

      entry2 = Gtk.Entry()
      entry2.set_text(self.settings['filename_playlist'])
      entry2.connect('changed', self.change_filename_playlist)

      hbox_playlist.append(image1)
      hbox_playlist.append(label1)
      hbox_playlist.append(label2)
      hbox_playlist.append(entry1)
      hbox_playlist.append(label3)
      hbox_playlist.append(entry2)

      grid.attach_next_to(hbox_playlist, hbox_streamripper, Gtk.PositionType.BOTTOM, 1, 1)


      hbox_converter_dir = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/empty_small.png' % self.config['app_path'])
      image1.set_margin_start(5)
      image1.set_pixel_size(30)

      label1 = Gtk.Label(label='Converter Directory:')
      label1.set_size_request(205, -1)
      label1.set_margin_start(5)
      label1.set_xalign(0)

      label2 = Gtk.Label(label='%s/' % self.config['music_path'])
      label2.set_size_request(130, -1)
      label2.set_margin_start(5)
      label2.set_xalign(0)

      entry1 = Gtk.Entry()
      entry1.set_text(self.settings['directory_converter'])
      entry1.connect('changed', self.change_directory_converter)


      hbox_converter_dir.append(image1)
      hbox_converter_dir.append(label1)
      hbox_converter_dir.append(label2)
      hbox_converter_dir.append(entry1)


      grid.attach_next_to(hbox_converter_dir, hbox_playlist, Gtk.PositionType.BOTTOM, 1, 1)


      hbox_filename_record = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/empty_small.png' % self.config['app_path'])
      image1.set_margin_start(5)
      image1.set_pixel_size(30)

      label1 = Gtk.Label(label='Record Directory:')
      label1.set_size_request(205, -1)
      label1.set_margin_start(5)
      label1.set_xalign(0)

      label2 = Gtk.Label(label='%s/' % self.config['music_path'])
      label2.set_size_request(130, -1)
      label2.set_margin_start(5)
      label2.set_xalign(0)

      entry1 = Gtk.Entry()
      entry1.set_size_request(300, -1)
      entry1.set_text(self.settings['directory_record'])
      entry1.connect('changed', self.change_directory_record)


      label3 = Gtk.Label(label='Filename:')
      label3.set_size_request(100, -1)
      label3.set_xalign(0.5)

      entry2 = Gtk.Entry()
      entry2.set_text(self.settings['filename_record'])
      entry2.connect('changed', self.change_filename_record)


      hbox_filename_record.append(image1)
      hbox_filename_record.append(label1)
      hbox_filename_record.append(label2)
      hbox_filename_record.append(entry1)
      hbox_filename_record.append(label3)
      hbox_filename_record.append(entry2)


      grid.attach_next_to(hbox_filename_record, hbox_converter_dir, Gtk.PositionType.BOTTOM, 1, 1)



      hbox_record_bitrate = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/empty_small.png' % self.config['app_path'])
      image1.set_margin_start(5)
      image1.set_pixel_size(30)


      label1 = Gtk.Label(label='Record Bitrate:')
      label1.set_size_request(205, -1)
      label1.set_margin_start(5)
      label1.set_xalign(0)

      combo1 = Gtk.ComboBoxText()
      choice_bitrate=self.settings['choice_bitrate']
      choice_active=0
      for i,item in enumerate(choice_bitrate):
         if item==self.settings['bitrate']:
            choice_active=i
         combo1.insert(i, str(i), ' ' + item + ' ')

      combo1.set_active(choice_active)
      combo1.connect('changed', self.combobox_bitrate_changed)
 

      hbox_record_bitrate.append(image1)
      hbox_record_bitrate.append(label1)
      hbox_record_bitrate.append(combo1)


      grid.attach_next_to(hbox_record_bitrate, hbox_filename_record, Gtk.PositionType.BOTTOM, 1, 1)


      hbox_device_record = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image1 = Gtk.Image()
      image1.set_from_file('%s/empty_small.png' % self.config['app_path'])
      image1.set_margin_start(5)
      image1.set_pixel_size(30)

      label1 = Gtk.Label(label='Record Device:')
      label1.set_size_request(205, -1)
      label1.set_margin_start(5)
      label1.set_xalign(0)

      active_dev=0
      self.combo_liststore = Gtk.ListStore(int, str)
      for i,dev in enumerate(self.settings['device_record_list']):
         self.combo_liststore.insert_with_values(i, (0, 1), (i+1, dev))
         if dev==self.settings['device_record']:
            active_dev=i


      self.combo_record = Gtk.ComboBox.new_with_model_and_entry(self.combo_liststore)
      self.combo_record.set_entry_text_column(1)
      self.combo_record.set_active(active_dev)
      self.combo_record.connect('changed', self.combobox_record_changed)


      self.button_device_record_scan = Gtk.Button(label='Scan')
      self.button_device_record_scan.connect('clicked', self.button_scan_clicked)


      entry1 = Gtk.Entry()
      entry1.set_size_request(-1, 10)
      entry1.set_text(self.settings['directory_converter'])
      entry1.connect('changed', self.change_directory_converter)


      hbox_device_record.append(image1)
      hbox_device_record.append(label1)
      hbox_device_record.append(self.combo_record)
      hbox_device_record.append(self.button_device_record_scan)


      grid.attach_next_to(hbox_device_record, hbox_record_bitrate, Gtk.PositionType.BOTTOM, 1, 1)

      button_reset = Gtk.Button(label='Reset')
      button_reset.connect('clicked', self.button_reset_clicked)
      button_reset.set_size_request(100, -1)


      hbox_reset = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=40)
      hbox_reset.append(button_reset)



      self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
      self.vbox.append(grid)
      self.vbox.append(hbox_reset)




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



   def change_filename_record(self, event):
      self.log.debug('start')
      self.settings['filename_record'] = event.get_text().strip()
      self.madmin.notebook_tab_converter.button_record_update_tooltip(filename=self.settings['filename_record'], directory=self.settings['directory_record'])



   def change_directory_record(self, event):
      self.log.debug('start')
      self.settings['directory_record'] = event.get_text().strip()
      self.madmin.notebook_tab_converter.button_record_update_tooltip(filename=self.settings['filename_record'], directory=self.settings['directory_record'])



   def combobox_bitrate_changed(self, event):
      self.log.debug('start')
      self.settings['bitrate'] = event.get_active_text()



   def combobox_record_changed(self, event):
      self.log.debug('start')

      self.madmin.notebook_tab_converter.button_record_update_tooltip(filename=self.settings['filename_record'], directory=self.settings['directory_record'])

      tree_iter = event.get_active_iter()
      if tree_iter is not None:
         model = event.get_model()
         row, name = model[tree_iter]
         self.settings['device_record']=name



   def button_scan_clicked(self, event):

      self.log.debug('start')

      audio_devices = []

      if which(self.config['bin_pwcli']):

         out = subprocess.check_output([self.config['bin_pwcli'], 'list-objects'])
         if out:
            output=out.decode('utf-8').split('\n')

            idnum=0
            node=''
            media=''

            for item in output:

               x = re.search('^\s+id (\d+),', item)
               if x and x.group(1):
                  idnum=x.group(1)
                  node=''
                  media=''

               x = re.search('node\.name\ \=\ "(.*)"\s*$', item)
               if x and x.group(1):
                  node=x.group(1)

               x = re.search('media\.class\ \=\ "(.*)"\s*$', item)
               if x and x.group(1):
                  if 'audio' in x.group(1).lower():
                     media=x.group(1)

               if node and idnum and media:
                  # pw  alsa_output.pci-0000_00_1f.3.analog-stereo   Audio/Sink   44
                  audio_devices.extend([['pw', idnum, media, node]])
                  node=''
                  idnum=0
                  media=''



      if which(self.config['bin_pactl']):

         out = subprocess.check_output([self.config['bin_pactl'],'list'])
         if out:
            output=out.decode('utf-8').split('\n')

            idnum=0
            node=''
            media=''

            for item in output:

               x = re.search('^([a-zA-Z0-9]*)\s+#(\d+)\s*$', item)
               if x and x.group(1) and x.group(2):
                  idnum=x.group(2)
                  node=''

               x = re.search('^\s+Name:\s*(.*)\s*$', item)
               if x and x.group(1):
                  node=x.group(1)

               x = re.search('^\s+device\.class\ =\ "(.*)"\s*$', item)
               if x and x.group(1):
                  media=x.group(1)

               if node and idnum and media:
                  # pa   alsa_input.pci-0000_00_1b.0.analog-stereo   Quelle   1
                  audio_devices.extend([['pa', idnum, media, node]])
                  node=''
                  idnum=0
                  media=''


      self.combo_liststore.clear()
      self.settings['device_record_list']=[]

      i=0
      for audio, idnum, media, node in audio_devices:
         dev = audio + ':' + idnum + ':' + media + ':' + node
         self.settings['device_record_list'].extend([dev])
         self.combo_liststore.insert_with_values(i, (0, 1), (i+1, dev))
         i+=1

      if len(self.settings['device_record_list'])>0:
         self.combo_record.set_active(0)






   def button_reset_clicked(self, event):
      self.log.debug('start')

      settings_file = self.settings['config_path'] + '/' + self.settings['filename_settings']

      self.log.debug('settings_file: %s' % settings_file)

      if os.path.exists(settings_file):
         os.remove(settings_file)

      self.madmin.on_reset_close()


