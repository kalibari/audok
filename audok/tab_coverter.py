import os
import re
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
gi.require_version('GLib', '2.0')
from gi.repository import GLib


class TabConverter:

   def __init__(self, madmin, log, config, settings):

      self.madmin = madmin
      self.log = log
      self.config = config
      self.settings = settings

      self.obj_timer_file2flac=None
      self.obj_timer_record=None
      self.obj_timer_file2mp3=None
      self.obj_timer_you2mp3=None


      self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
      self.vbox.set_margin_top(5)


      label1 = Gtk.Label(label='Audio:')
      label1.set_xalign(0)
      label1.set_size_request(80, -1)
      label1.set_margin_start(5)


      self.button_you2mp3 = Gtk.Button(label='you2mp3')
      self.button_you2mp3.connect('clicked', self.button_you2mp3_chlicked)
      self.button_you2mp3_update_tooltip(directory=self.settings['directory_new'])


      self.button_record = Gtk.Button(label='record')
      self.button_record.connect('clicked', self.button_record_chlicked)
      self.button_record_update_tooltip(filename=self.settings['filename_record'], directory=self.settings['directory_record'])


      self.button_file2mp3 = Gtk.Button(label='file2mp3')
      self.button_file2mp3.connect('clicked', self.button_file2mp3_chlicked)
      self.button_file2mp3_update_tooltip(directory=self.settings['directory_new'])


      self.button_file2flac = Gtk.Button(label='file2flac')
      self.button_file2flac.connect('clicked', self.button_file2flac_chlicked)
      self.button_file2flac_update_tooltip(directory=self.settings['directory_new'])


      self.button_stop = Gtk.Button(label='stop')
      self.button_stop.connect('clicked', self.button_stop_chlicked)
      self.button_stop.set_sensitive(False)
      self.button_stop.set_tooltip_text('Stop')


      hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox1.set_hexpand(True)
      hbox1.append(label1)
      hbox1.append(self.button_you2mp3)
      hbox1.append(self.button_record)
      hbox1.append(self.button_file2mp3)
      hbox1.append(self.button_file2flac)
      hbox1.append(self.button_stop)


      label2 = Gtk.Label(label='Url:')
      label2.set_xalign(0)
      label2.set_size_request(80, -1)
      label2.set_margin_start(5)


      self.textbuffer_input = Gtk.Entry()
      self.textbuffer_input.set_hexpand(True)

      hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox2.set_hexpand(True)
      hbox2.append(label2)
      hbox2.append(self.textbuffer_input)


      label3 = Gtk.Label(label='Output:')
      label3.set_xalign(0)
      label3.set_size_request(80, -1)
      label3.set_margin_start(5)
      label3.set_margin_top(5)
      label3.set_margin_bottom(59)

      self.scrolledwindow = Gtk.ScrolledWindow()
      textview = Gtk.TextView()
      textview.set_wrap_mode(True)
      #textview.set_editable(False)
      self.textbuffer_output = textview.get_buffer()
      self.scrolledwindow.set_vexpand(True)
      self.scrolledwindow.set_hexpand(True)
      self.scrolledwindow.set_child(textview)


      hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox3.set_margin_start(5)
      hbox3.set_hexpand(True)
      hbox3.set_vexpand(True)
      hbox3.append(label3)
      hbox3.append(self.scrolledwindow)

      self.vbox.append(hbox1)
      self.vbox.append(hbox2)
      self.vbox.append(hbox3)






   def refresh_output_textctrl_timer(self):

      self.log.debug('\ndef refresh_output_textctrl_timer start')

      inactive_processes=0

      # copy dict to prevent ->  RuntimeError: dictionary changed size during iteration
      loop_process_database = dict(self.madmin.process_database)

      for item in loop_process_database:

         self.log.debug('\ndef refresh_output_textctrl_timer process_database: %s' % str(self.madmin.process_database[item]))


         if self.madmin.process_database[item]['status']=='inactive':
            inactive_processes+=1


         if self.madmin.process_database[item]['status']=='active' or self.madmin.process_database[item]['status']=='killed':

            if self.madmin.process_database[item]['status']=='killed':
               self.madmin.process_database[item]['status']='inactive'


            ############
            ### show ###
            ############
            if self.madmin.process_database[item]['todo']=='show':

               if self.madmin.process_database[item]['job']=='you2mp3':
                  if self.madmin.process_database[item]['output']:
                     self.textbuffer_output.set_text('%s\n' % '\n'.join(self.madmin.process_database[item]['output']))
                     self.madmin.process_database[item]['output']=[]



               if self.madmin.process_database[item]['job']=='record':
                  if self.madmin.process_database[item]['identifier']=='record':
                     if self.madmin.process_database[item]['output']:
                        self.textbuffer_output.set_text('%s\n' % self.madmin.process_database[item]['output'])
                        self.madmin.process_database[item]['output']=[]



               if self.madmin.process_database[item]['job']=='file2mp3':
                  if self.madmin.process_database[item]['output']:
                     self.textbuffer_output.set_text('%s\n' % '\n'.join(self.madmin.process_database[item]['output']))
                     self.madmin.process_database[item]['output']=[]


               if self.madmin.process_database[item]['job']=='file2flac':
                  if self.madmin.process_database[item]['output']:
                     self.textbuffer_output.set_text('%s\n' % '\n'.join(self.madmin.process_database[item]['output']))
                     self.madmin.process_database[item]['output']=[]


            ##############
            ### result ###
            ##############
            if self.madmin.process_database[item]['todo']=='result':

               # enable buttons, stop refreh timer
               self.button_you2mp3.set_sensitive(True)
               self.button_record.set_sensitive(True)
               self.button_file2mp3.set_sensitive(True)
               self.button_file2flac.set_sensitive(True)
               self.button_stop.set_sensitive(False)



               if self.madmin.process_database[item]['job']=='you2mp3':
                  self.madmin.process_database[item]['status']='inactive'
                  if self.madmin.process_database[item]['result']==True:
                     self.textbuffer_output.set_text('-- job: %s successfully done\n' % self.madmin.process_database[item]['job'])
                     self.textbuffer_input.set_text('')
                  else:
                     self.textbuffer_output.set_text('-- job: %s error\n' % self.madmin.process_database[item]['job'])


               if self.madmin.process_database[item]['job']=='record':
                  if self.madmin.process_database[item]['identifier']=='record':
                     self.madmin.process_database[item]['status']='inactive'



               if self.madmin.process_database[item]['job']=='file2mp3':
                  self.madmin.process_database[item]['status']='inactive'
                  if self.madmin.process_database[item]['result']==True:
                     self.textbuffer_output.set_text('-- job: %s filename: %s successfully converted\n' % (self.madmin.process_database[item]['job'],self.madmin.process_database[item]['source']))

                     source_path_filename = self.madmin.process_database[item]['source']
                     filename = os.path.basename(source_path_filename)
                     dest_path = self.config['music_path'] + '/' + self.settings['directory_old']
                     if not os.path.exists(dest_path):
                        os.mkdir(dest_path)

                     os.rename(source_path_filename,'%s/%s' % (dest_path,filename))

                  else:
                     self.textbuffer_output.set_text('-- job: %s filename: %s output: %s\n' % (self.madmin.process_database[item]['job'],self.madmin.process_database[item]['source'], ', '.join(self.madmin.process_database[item]['output'])))



               if self.madmin.process_database[item]['job']=='file2flac':
                  self.madmin.process_database[item]['status']='inactive'
                  if self.madmin.process_database[item]['result']==True:
                     self.textbuffer_output.set_text('-- job: %s filename: %s successfully converted\n' % (self.madmin.process_database[item]['job'],self.madmin.process_database[item]['source']))

                     source_path_filename = self.madmin.process_database[item]['source']
                     filename = os.path.basename(source_path_filename)
                     dest_path = self.config['music_path'] + '/' + self.settings['directory_old']
                     if not os.path.exists(dest_path):
                        os.mkdir(dest_path)

                     os.rename(source_path_filename,'%s/%s' % (dest_path,filename))

                  else:
                     self.textbuffer_output.set_text('-- job: %s filename: %s output: %s\n' % (self.madmin.process_database[item]['job'],self.madmin.process_database[item]['source'], ', '.join(self.madmin.process_database[item]['output'])))



      if len(self.madmin.process_database)==inactive_processes:
			# timer stop
         return False
      else:
         return True



   def button_you2mp3_chlicked(self, event):
      self.log.debug('start')

      self.button_you2mp3.set_sensitive(False)
      self.button_record.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_file2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)


      self.textbuffer_output.set_text('')

      source = self.textbuffer_input.get_text().strip()

      if not source:

         self.textbuffer_output.set_text('please enter an URL')

         self.button_you2mp3.set_sensitive(True)
         self.button_record.set_sensitive(True)
         self.button_file2mp3.set_sensitive(True)
         self.button_file2flac.set_sensitive(True)
         self.button_stop.set_sensitive(False)


      else:

         self.textbuffer_output.set_text('-- job you2mp3 source: %s\n' % source)

         if not os.path.exists(self.config['music_path'] + '/' + self.settings['directory_new']):
            os.mkdir(self.config['music_path'] + '/' + self.settings['directory_new'])

         self.obj_timer_you2mp3 = GLib.timeout_add(1000, self.refresh_output_textctrl_timer)

         # youtube-dl --no-warnings --no-call-home --audio-quality=4 --extract-audio --audio-format=mp3 --title [url]
         cmd=[self.config['bin_youtubedl'],'--audio-quality=4','--no-warnings','--no-call-home','--extract-audio','--audio-format=mp3','--title',source]
         cwd=self.config['music_path'] + '/' + self.settings['directory_new']
         self.madmin.process_starter(cmd=cmd, cwd=cwd, job='you2mp3', identifier='', source='')




   def button_record_chlicked(self, event):
      self.log.debug('start')

      self.textbuffer_output.set_text('')

      self.obj_timer_record = GLib.timeout_add(1000, self.refresh_output_textctrl_timer)


      if not os.path.exists(self.config['music_path'] + '/' + self.settings['directory_record']):
         os.mkdir(self.config['music_path'] + '/' + self.settings['directory_record'])



      source_cmd=[]
      target=0
      node=''

      if self.settings['device_record'] in self.settings['device_record_list']:

         get_target = self.settings['device_record'].split(':')

         if len(get_target)>=4:

            audio=get_target[0]
            get_target.pop(0)

            idnum=get_target[0]
            get_target.pop(0)

            media=get_target[0]
            get_target.pop(0)

            node=''.join(get_target)


            if audio=='pw':

               # pw  alsa_output.pci-0000_00_1f.3.analog-stereo   Audio/Sink   44
               target=int(idnum)
               if target:
                  source_cmd=[self.config['bin_pwrecord'],'--verbose','--record','--channels=2', '--format=s32', '--rate=48000', '--volume=0.99', '--target=%s' % target]


            elif audio=='pa':

               # pa   alsa_input.pci-0000_00_1b.0.analog-stereo   Quelle   1
               if node:
                  source_cmd=[self.config['bin_parecord'],'--verbose','--record','--channels=2', '--format=s32', '--rate=48000', '--volume=0.99', '--file-format=wav', '--device=%s' % node]



      if len(source_cmd)==0:
         self.textbuffer_output.set_text('cannot find a record device, please rescan devices (see Settings)')
      else:

         self.button_you2mp3.set_sensitive(False)
         self.button_record.set_sensitive(False)
         self.button_file2mp3.set_sensitive(False)
         self.button_file2flac.set_sensitive(False)
         self.button_stop.set_sensitive(True)

         filename = self.settings['filename_record']

         if '/' in filename:
            self.textbuffer_output.set_text('"/" in filename is not allowed')
         else:

            pre_filename=filename
            post_filename='wav'
            if '.' in filename:
               pre_filename = filename.rsplit('.',1)[0]

            if not os.path.exists(self.config['music_path'] + '/' + self.settings['directory_record']):
               os.mkdir(self.config['music_path'] + '/' + self.settings['directory_record'])

            directories = [self.config['music_path'] + '/' + self.settings['directory_record']]

            extensions = self.config['supported_audio_files']

            allfiles = self.madmin.file_scan(directories, extensions)


            num=0
            fexist=False
            for item in allfiles:
               x = re.search('%s\.%s\s*$' % (pre_filename,post_filename), os.path.basename(item))
               if x:
                  fexist=True

               x = re.search('%s-(\d+)\.%s\s*$' % (pre_filename,post_filename), os.path.basename(item))
               if x and x.group(1):
                  fexist=True
                  if int(x.group(1))>num:
                     num=int(x.group(1))

            if fexist==False:
               new_filename='%s.%s' % (pre_filename,post_filename)
            else:
               new_filename='%s-%d.%s' % (pre_filename,num+1,post_filename)



            self.textbuffer_output.set_text('record node: %s target: %s filename: %s\n' % (node,target,new_filename))

            self.button_you2mp3.set_sensitive(False)
            self.button_record.set_sensitive(False)
            self.button_file2mp3.set_sensitive(False)
            self.button_file2flac.set_sensitive(False)
            self.button_stop.set_sensitive(True)
   
            # pw-record --verbose --record --channels=2 --format=s32 --rate=48000 --volume=0.99 --target=41  /tmp/test.wav
            # parecord  --verbose --record --channels=2 --format=s32 --rate=48000 --volume=0.99 --file-format=wav --device=alsa_input.pci-0000_00_1b.0.analog-stereo /tmp/test.wav
            cmd=[]
            cmd.extend(source_cmd)
            cmd.extend(['%s/%s/%s' % (self.config['music_path'],self.settings['directory_record'],new_filename)])
            cwd=self.config['music_path'] + '/' + self.settings['directory_record']
            self.madmin.process_starter(cmd=cmd, cwd=cwd, job='record', identifier='', source='')






   def button_file2mp3_chlicked(self, event):
      self.log.debug('start')

      self.button_you2mp3.set_sensitive(False)
      self.button_record.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_file2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)

      self.textbuffer_output.set_text('')

      directories = [self.config['music_path'] + '/' + self.settings['directory_new']]

      if not os.path.exists(self.config['music_path'] + '/' + self.settings['directory_new']):
         os.mkdir(self.config['music_path'] + '/' + self.settings['directory_new'])

      extensions = list(self.config['supported_audio_files'])
      if 'mp3' in extensions:
         extensions.remove('mp3')

      files_to_change = self.madmin.file_scan(directories, extensions)
      mp3files = self.madmin.file_scan(directories, ['mp3'])


      self.textbuffer_output.set_text('number of files to change: %s\n' % len(files_to_change))

      if len(files_to_change)==0:

         self.log.debug('no files to change')

         self.button_you2mp3.set_sensitive(True)
         self.button_record.set_sensitive(True)
         self.button_file2mp3.set_sensitive(True)
         self.button_file2flac.set_sensitive(True)
         self.button_stop.set_sensitive(False)


      else:

         self.log.debug('try start_popen_thread')

         self.obj_timer_file2mp3 = GLib.timeout_add(1000, self.refresh_output_textctrl_timer)

         for item in files_to_change:

            x = re.search('^(.*)(-\d)?\.(%s)' % '|'.join(extensions), item)
            if x and x.group(1) and x.group(3):

               if x.group(2):
                  newfilename='%s%s.mp3' % (x.group(1),x.group(2))
               else:
                  newfilename='%s.mp3' % x.group(1)

               num=1
               while True:
                  if newfilename in mp3files:
                     newfilename='%s-%s.mp3' % (x.group(1),num)
                     num+=1
                  else:
                     break

               cwd=self.config['music_path'] + '/' + self.settings['directory_new']
               cmd=[self.config['bin_nice'],'-n','19',self.config['bin_ffmpeg'],'-v','error','-i',item,'-ab', '%s' % str(self.settings['bitrate']),'-n',newfilename]
               self.madmin.process_starter(cmd=cmd, cwd=cwd, job='file2mp3', identifier='', source=item)



   def button_file2flac_chlicked(self, event):

      self.log.debug('start')

      self.button_you2mp3.set_sensitive(False)
      self.button_record.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_file2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)

      self.textbuffer_output.set_text('')

      directories = [self.config['music_path'] + '/' + self.settings['directory_new']]

      if not os.path.exists(self.config['music_path'] + '/' + self.settings['directory_new']):
         os.mkdir(self.config['music_path'] + '/' + self.settings['directory_new'])

      extensions = list(self.config['supported_audio_files'])
      if 'flac' in extensions:
         extensions.remove('flac')

      files_to_change = self.madmin.file_scan(directories, extensions)
      flacfiles = self.madmin.file_scan(directories, ['flac'])


      self.textbuffer_output.set_text('number of files to change: %s\n' % len(files_to_change))

      if len(files_to_change)==0:

         self.log.debug('no files to change')

         self.button_you2mp3.set_sensitive(True)
         self.button_record.set_sensitive(True)
         self.button_file2mp3.set_sensitive(True)
         self.button_file2flac.set_sensitive(True)
         self.button_stop.set_sensitive(False)

      else:

         self.log.debug('try start_popen_thread')

         self.obj_timer_file2flac = GLib.timeout_add(1000, self.refresh_output_textctrl_timer)


         for item in files_to_change:

            x = re.search('^(.*)(-\d)?\.(%s)' % '|'.join(extensions), item)
            if x and x.group(1) and x.group(3):

               if x.group(2):
                  newfilename='%s%s.flac' % (x.group(1),x.group(2))
               else:
                  newfilename='%s.flac' % x.group(1)

               num=1
               while True:
                  if newfilename in flacfiles:
                     newfilename='%s-%s.flac' % (x.group(1),num)
                     num+=1
                  else:
                     break


               aformat='aformat=s32:48000'

               # ffmpeg -y -i /MyDisc/Audio/Neu/New/record-1.wav -af aformat=s32:48000 /MyDisc/Audio/Neu/test.flac
               cwd=self.config['music_path'] + '/' + self.settings['directory_new']
               cmd=['nice','-n','19',self.config['bin_ffmpeg'], '-y', '-i',  item, '-af', aformat, newfilename]
               self.madmin.process_starter(cmd=cmd, cwd=cwd, job='file2flac', identifier='', source=item)



   def button_stop_chlicked(self, event):

      self.log.debug('start')

      if self.obj_timer_file2flac is not None:
         GLib.source_remove(self.obj_timer_file2flac)
         self.obj_timer_file2flac=None

      if self.obj_timer_record is not None:
         GLib.source_remove(self.obj_timer_record)
         self.obj_timer_record=None

      if self.obj_timer_file2mp3 is not None:
         GLib.source_remove(self.obj_timer_file2mp3)
         self.obj_timer_file2mp3=None

      if self.obj_timer_you2mp3 is not None:
         GLib.source_remove(self.obj_timer_you2mp3)
         self.obj_timer_you2mp3=None


      self.madmin.process_job_killer(job='you2mp3')
      self.madmin.process_job_killer(job='record')
      self.madmin.process_job_killer(job='file2mp3')
      self.madmin.process_job_killer(job='file2flac')

      self.button_you2mp3.set_sensitive(True)
      self.button_record.set_sensitive(True)
      self.button_file2mp3.set_sensitive(True)
      self.button_file2flac.set_sensitive(True)
      self.button_stop.set_sensitive(False)



   def button_you2mp3_update_tooltip(self, directory):
      self.button_you2mp3.set_tooltip_text('Convert a Youtube url to mp3 - Destination Directory: %s' % directory)



   def button_record_update_tooltip(self, filename, directory):
      self.button_record.set_tooltip_text('Record via Pipewire - Destination Filename: %s Directory: %s' % (filename,directory))



   def button_file2mp3_update_tooltip(self, directory):
      self.button_file2mp3.set_tooltip_text('Convert all Files from Directory: %s to mp3' % directory)



   def button_file2flac_update_tooltip(self, directory):
      self.button_file2flac.set_tooltip_text('Convert all Files from Directory: %s to flac' % directory)
