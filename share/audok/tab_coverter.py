import os
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GObject


class TabConverter:

   def __init__(self, main, settings):
      self.main = main
      self.settings = settings

      self.box = Gtk.Box()
      self.box.set_border_width(10)


      self.file_database = {}

      #############################
      box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

      row1 = Gtk.ListBoxRow()
      hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox1.set_hexpand(True)
      row1.add(hbox1)

      label1 = Gtk.Label("Audio", xalign=0)
      label1.set_size_request(50, -1)


      self.button_you2mp3 = Gtk.Button(label="you2mp3")
      self.button_you2mp3.connect("clicked", self.START_YOU2MP3_BUTTON)


      self.button_pwrecord = Gtk.Button(label="pwrecord")
      self.button_pwrecord.connect("clicked", self.START_PWRECORD_BUTTON)


      self.button_file2mp3 = Gtk.Button(label="file2mp3")
      self.button_file2mp3.connect("clicked", self.START_FILE2MP3_BUTTON)


      self.button_wav2flac = Gtk.Button(label="wav2flac")
      self.button_wav2flac.connect("clicked", self.START_WAV2FLAC_BUTTON)


      self.button_stop = Gtk.Button(label="stop")
      self.button_stop.connect("clicked", self.STOP_BUTTON)
      self.button_stop.set_sensitive(False)


      hbox1.pack_start(label1, False, True, 10)
      hbox1.pack_start(self.button_you2mp3, True, True, 0)
      hbox1.pack_start(self.button_pwrecord, True, True, 0)
      hbox1.pack_start(self.button_file2mp3, True, True, 0)
      hbox1.pack_start(self.button_wav2flac, True, True, 0)
      hbox1.pack_start(self.button_stop, True, True, 0)

      #############################

      row2 = Gtk.ListBoxRow()
      hbox2= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox2.set_hexpand(True)
      row2.add(hbox2)


      label2 = Gtk.Label("Input", xalign=0)
      #label2.set_line_wrap(True)
      label2.set_size_request(50, -1)

      self.textbuffer_input = Gtk.Entry()

      self.textbuffer_input.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      

      hbox2.pack_start(label2, False, True, 10)
      hbox2.pack_start(self.textbuffer_input, True, True, 0)


      #############################

      row3 = Gtk.ListBoxRow()
      hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox3.set_hexpand(True)
      row3.add(hbox3)

      label3 = Gtk.Label("Ouput", xalign=0)
      label3.set_size_request(50, -1)


      self.scrolledwindow3 = Gtk.ScrolledWindow()
      textview = Gtk.TextView()
      textview.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      textview.set_editable(False)
      self.textbuffer_output = textview.get_buffer()
      self.scrolledwindow3.add(textview)



      hbox3.pack_start(label3, False, True, 10)
      hbox3.pack_start(self.scrolledwindow3, True, True, 0)



      box_outer.pack_start(row1, False, False, 2)
      box_outer.pack_start(row2, False, False, 2)
      box_outer.pack_start(row3, True, True, 2)
      self.box.add(box_outer)

      ###################################################################################




   def get_database_files(self, value):
      files = []
      for k in self.file_database:
         if self.file_database[k][0]==value:
            files.extend([k])
      return files



   def get_destination_filename(self, destination_dir, pathfile, newprefix):
      if self.settings['Debug']==1:
         print ('def get_destination_filename destination_dir: %s pathfile: %s newprefix: %s' % (destination_dir, pathfile, newprefix))

      # destination_dir: /MyDisc/Audio/Neu filename: /MyDisc/Audio/Neu/pw-record-20.wav oldprefix: .wav newprefix: .mp3

      self.filescan(destination_dir)

      # ('pw-record-24','.wav')
      (newpart1,newpart2) = os.path.splitext(os.path.basename(pathfile))

      num=0
      newpart1pre = newpart1
      x = re.search('^(.*)-(\d+)$', newpart1pre)
      if x and x.group(1) and x.group(2):
         newpart1pre = x.group(1)
         num = int(x.group(2))

      # pw-record
      if self.settings['Debug']==1:
         print ('def get_destination_filename newpart1pre: %s num: %s' % (newpart1pre,str(num)))

      for item in self.all_files_in_dir:
         x = re.search('^(%s)-(\d+)%s' % (newpart1pre, newprefix), item)
         if x and x.group(1) and x.group(2):
            if self.settings['Debug']==1:
               print ('def get_destination_filename found file %s -> increase num' % item)
            if int(x.group(2))>=num:
               num=int(x.group(2))

      num+=1
      dest_filename='%s-%s%s' % (newpart1pre,num,newprefix)

      if self.settings['Debug']==1:
         print ('def get_destination_filename dest_filename: %s' % dest_filename)

      return dest_filename





   def filescan(self, path):
      if self.settings['Debug']==1:
         print ('def filescan - part: %s' % path)


      # reset
      self.file_database = {}
      self.all_files_in_dir = []

      for root, dirs, files in os.walk(path):

         for item in files:

            if root==path:
               self.all_files_in_dir.extend([item])

            if 'incomplete' in root:
               pass
            elif root==(self.settings['Music_Path'] + '/' + self.settings['Directory_Old']):
               pass
            else:

               m1 = re.search('\.ts$', item, re.IGNORECASE)
               if m1:
                  f = {'%s/%s' % (root,item) : ['.ts', item]}
                  self.file_database.update(f)

               m2 = re.search('\.flv$', item, re.IGNORECASE)
               if m2:
                  f = {'%s/%s' % (root,item) : ['.flv', item]}
                  self.file_database.update(f)

               m3 = re.search('\.flac$', item, re.IGNORECASE)
               if m3:
                  f = {'%s/%s' % (root,item) : ['.flac', item]}
                  self.file_database.update(f)

               m4 = re.search('\.m4a$', item, re.IGNORECASE)
               if m4:
                  f = {'%s/%s' % (root,item) : ['.m4a', item]}
                  self.file_database.update(f)

               m5 = re.search('\.mp3$', item, re.IGNORECASE)
               if m5:
                  f = {'%s/%s' % (root,item) : ['.mp3', item]}
                  self.file_database.update(f)

               m6 = re.search('\.wav$', item, re.IGNORECASE)
               if m6:
                  f = {'%s/%s' % (root,item) : ['.wav', item]}
                  self.file_database.update(f)

               m7 = re.search('\.mp4$' , item, re.IGNORECASE)
               if m7:
                  f = {'%s/%s' % (root,item) : ['.mp4', item]}
                  self.file_database.update(f)

               m8 = re.search('\.webm$' , item, re.IGNORECASE)
               if m8:
                  f = {'%s/%s' % (root,item) : ['.webm', item]}
                  self.file_database.update(f)

               m9 = re.search('\.mkv$' , item, re.IGNORECASE)
               if m9:
                  f = {'%s/%s' % (root,item) : ['.mkv', item]}
                  self.file_database.update(f)






   def refresh_output_textctrl_timer(self):

      if self.settings['Debug']==1:
         print ('\ndef refresh_output_textctrl_timer start')


      inactive_processes=0

      # copy dict to prevent ->  RuntimeError: dictionary changed size during iteration
      loop_process_database = dict(self.main.process_database)

      for item in loop_process_database:

         if self.settings['Debug']==1:
            print ('\ndef refresh_output_textctrl_timer process_database: %s' % str(self.main.process_database[item]))


         if self.main.process_database[item]['status']=='inactive':
            inactive_processes+=1


         if self.main.process_database[item]['status']=='active' or self.main.process_database[item]['status']=='killed':

            if self.main.process_database[item]['status']=='killed':
               self.main.process_database[item]['status']='inactive'


            ############
            ### show ###
            ############
            if self.main.process_database[item]['todo']=='show':

               if self.main.process_database[item]['job']=='you2mp3':
                  if self.main.process_database[item]['output']:
                     self.textbuffer_output.set_text('%s\n' % '\n'.join(self.main.process_database[item]['output']))
                     self.main.process_database[item]['output']=[]


               if self.main.process_database[item]['job']=='pwrecord':
                  if self.main.process_database[item]['output']:
                     self.textbuffer_output.set_text('%s\n' % self.main.process_database[item]['output'])
                     self.main.process_database[item]['output']=[]


               if self.main.process_database[item]['job']=='file2mp3':
                  if self.main.process_database[item]['output']:
                     self.textbuffer_output.set_text('%s\n' % '\n'.join(self.main.process_database[item]['output']))
                     self.main.process_database[item]['output']=[]


               if self.main.process_database[item]['job']=='wav2flac':
                  if self.main.process_database[item]['output']:
                     self.textbuffer_output.set_text('%s\n' % '\n'.join(self.main.process_database[item]['output']))
                     self.main.process_database[item]['output']=[]


            ##############
            ### result ###
            ##############
            if self.main.process_database[item]['todo']=='result':

               # enable buttons, stop refreh timer
               self.button_you2mp3.set_sensitive(True)
               self.button_pwrecord.set_sensitive(True)
               self.button_file2mp3.set_sensitive(True)
               self.button_wav2flac.set_sensitive(True)
               self.button_stop.set_sensitive(False)



               if self.main.process_database[item]['job']=='you2mp3':
                  self.main.process_database[item]['status']='inactive'
                  if self.main.process_database[item]['result']==True:
                     self.textbuffer_output.set_text('-- job: %s successfully done\n' % self.main.process_database[item]['job'])
                     self.textbuffer_input.set_text('')
                  else:
                     self.textbuffer_output.set_text('-- job: %s error\n' % self.main.process_database[item]['job'])



               if self.main.process_database[item]['job']=='pwrecord':
                  self.main.process_database[item]['status']='inactive'
                  if self.main.process_database[item]['result']==True:
                     self.textbuffer_output.set_text('-- job: %s successfully done\n' % self.main.process_database[item]['job'])
                     self.textbuffer_input.set_text('')
                  else:
                     self.textbuffer_output.set_text('-- job: %s error: %s\n' % (self.main.process_database[item]['job'],self.main.process_database[item]['output']))



               if self.main.process_database[item]['job']=='file2mp3':
                  self.main.process_database[item]['status']='inactive'
                  if self.main.process_database[item]['result']==True:
                     self.textbuffer_output.set_text('-- job: %s filename: %s successfully converted\n' % (self.main.process_database[item]['job'],self.main.process_database[item]['source']))
                     if (os.path.exists(self.settings['Music_Path'] + '/' + self.settings['Directory_Old']))==False:
                        os.mkdir(self.settings['Music_Path'] + '/' + self.settings['Directory_Old'])
                     oldfilename = os.path.basename(self.main.process_database[item]['source'])
                     os.rename(self.main.process_database[item]['source'],'%s/%s/%s' % (self.settings['Music_Path'],self.settings['Directory_Old'],oldfilename))
                  else:
                     self.textbuffer_output.set_text('-- job: %s filename: %s output: %s\n' % (self.main.process_database[item]['job'],self.main.process_database[item]['source'], ', '.join(self.main.process_database[item]['output'])))



               if self.main.process_database[item]['job']=='wav2flac':
                  self.main.process_database[item]['status']='inactive'
                  if self.main.process_database[item]['result']==True:
                     self.textbuffer_output.set_text('-- job: %s filename: %s successfully converted\n' % (self.main.process_database[item]['job'],self.main.process_database[item]['source']))
                     if (os.path.exists(self.settings['Music_Path'] + '/' + self.settings['Directory_Old']))==False:
                        os.mkdir(self.settings['Music_Path'] + '/' + self.settings['Directory_Old'])
                     oldfilename = os.path.basename(self.main.process_database[item]['source'])
                     os.rename(self.main.process_database[item]['source'],'%s/%s/%s' % (self.settings['Music_Path'],self.settings['Directory_Old'],oldfilename))
                  else:
                     self.textbuffer_output.set_text('-- job: %s filename: %s output: %s\n' % (self.main.process_database[item]['job'],self.main.process_database[item]['source'], ', '.join(self.main.process_database[item]['output'])))



      if len(self.main.process_database)==inactive_processes:
			# timer stop
         return False
      else:
         return True





   ###### BUTTONS ######

   def START_YOU2MP3_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def START_YOU2MP3_BUTTON - start')


      self.button_you2mp3.set_sensitive(False)
      self.button_pwrecord.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_wav2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)


      self.textbuffer_output.set_text('')

      # youtube-dl --help
      # youtube-dl --no-warnings --no-call-home --audio-quality=4 --extract-audio --audio-format=mp3 --title https://www.youtube.com/watch?v=w7BE3inS-NM


      source = self.textbuffer_input.get_text()
      #start_iter = self.textbuffer_input.get_start_iter()
      #end_iter = self.textbuffer_input.get_end_iter()
      #source = self.textbuffer_input.get_text(start_iter, end_iter, True)   

      source=source.strip()

      if not source:

         self.textbuffer_output.set_text('please insert a input URL')

         self.button_you2mp3.set_sensitive(True)
         self.button_pwrecord.set_sensitive(True)
         self.button_file2mp3.set_sensitive(True)
         self.button_wav2flac.set_sensitive(True)
         self.button_stop.set_sensitive(False)


      else:

         self.textbuffer_output.set_text('-- job you2mp3 source: %s\n' % source)


         self.timer_you2mp3 = GObject.timeout_add(1000, self.refresh_output_textctrl_timer)

         cmd=[self.settings['Bin_Youtubedl'],'--audio-quality=4','--no-warnings','--no-call-home','--extract-audio','--audio-format=mp3','--exec','exit 0','--title',source]
         cwd=self.settings['Music_Path'] + '/' + self.settings['Directory_New']
         self.main.process_starter(cmd=cmd, cwd=cwd, job='you2mp3', identifier='', source='')





   def START_PWRECORD_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def START_PWRECORD_BUTTON - start')


      self.button_you2mp3.set_sensitive(False)
      self.button_pwrecord.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_wav2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)


      self.filescan(self.settings['Music_Path'] + '/' + self.settings['Directory_New'])

      wavfiles = self.get_database_files('.wav')
      num=0
      for item in wavfiles:
         x = re.search('%s-(\d+).wav' % self.settings['Pwrecord_Default_Filename'], os.path.basename(item))
         if x and x.group(1):
            if int(x.group(1))>num:
               num=int(x.group(1))
      newfilename='%s-%d.wav' % (self.settings['Pwrecord_Default_Filename'], (num+1))

      if not os.path.exists(self.settings['Music_Path'] + '/' + self.settings['Directory_New']):
         os.mkdir(self.settings['Music_Path'] + '/' + self.settings['Directory_New'])


      self.textbuffer_output.set_text('')

      self.timer_pwrecord = GObject.timeout_add(1000, self.refresh_output_textctrl_timer)


      # pw-record --verbose --record --channels=2 --format=s32 --rate=48000 --volume=0.99 --target=41  /MyDisc/Audio/Neu/test.wav

      cmd=[self.settings['Bin_Pwrecord'],'--verbose','--record','--channels=2', '--format=s32', '--rate=48000', '--volume=0.99',\
      '--target=%s' % self.settings['Pwrecord_Target'], '%s/%s/%s' % (self.settings['Music_Path'],self.settings['Directory_New'],newfilename)]
      cwd=self.settings['Music_Path'] + '/' + self.settings['Directory_New']
      self.main.process_starter(cmd=cmd, cwd=cwd, job='pwrecord', identifier='', source='')







   def START_FILE2MP3_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def START_FILE2MP3_BUTTON - start')


      self.button_you2mp3.set_sensitive(False)
      self.button_pwrecord.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_wav2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)




      self.filescan(self.settings['Music_Path'] + '/' + self.settings['Directory_New'])

      self.textbuffer_output.set_text('')


      allfiles = ([])

      tsfiles = self.get_database_files('.ts')
      allfiles.extend([['.ts', tsfiles]])

      mp4files = self.get_database_files('.mp4')
      allfiles.extend([['.mp4', mp4files]])

      flvfiles = self.get_database_files('.flv')
      allfiles.extend([['.flv', flvfiles]])

      webmfiles = self.get_database_files('.webm')
      allfiles.extend([['.webm', webmfiles]])

      flacfiles = self.get_database_files('.flac')
      allfiles.extend([['.flac', flacfiles]])

      m4afiles = self.get_database_files('.m4a')
      allfiles.extend([['.m4a', m4afiles]])

      mkvfiles = self.get_database_files('.mkv')
      allfiles.extend([['.mkv', mkvfiles]])

      wavfiles = self.get_database_files('.wav')
      allfiles.extend([['.wav', wavfiles]])



      files_to_change = len(tsfiles) + len(mp4files) + len(flvfiles) + len(webmfiles) + len(flacfiles) + len(m4afiles) + len(mkvfiles) + len(wavfiles)

      self.textbuffer_output.set_text('number of files to change: %s\n' % files_to_change)

      if files_to_change==0:

         if self.settings['Debug']==1:
            print ('def START_FILE2MP3_BUTTON - no files to change')
         

         self.button_you2mp3.set_sensitive(True)
         self.button_pwrecord.set_sensitive(True)
         self.button_file2mp3.set_sensitive(True)
         self.button_wav2flac.set_sensitive(True)
         self.button_stop.set_sensitive(False)


      else:

         if self.settings['Debug']==1:
            print ('def START_FILE2MP3_BUTTON - try start_popen_thread')


         self.timer_file2mp3 = GObject.timeout_add(1000, self.refresh_output_textctrl_timer)

         #self.refresh_timer = wx.Timer(self)
         #self.Bind(wx.EVT_TIMER, self.refresh_output_textctrl_timer, self.refresh_timer)
         #self.refresh_timer.Start(1000)

         for oldprefix,files in allfiles:

            for pathfile in files:

               # destination_dir  pathfile  newprefix
               dest_filename = self.get_destination_filename((self.settings['Music_Path'] + '/' + self.settings['Directory_New']), pathfile, '.mp3')

               cwd=self.settings['Music_Path'] + '/' + self.settings['Directory_New']
               cmd=[self.settings['Bin_Nice'],'-n','19',self.settings['Bin_Ffmpeg'],'-v','error','-i',pathfile,'-ab', '%s' % str(self.settings['File2mp3_Bitrate']),'-n',dest_filename]
               self.main.process_starter(cmd=cmd, cwd=cwd, job='file2mp3', identifier='', source=pathfile)




   def START_WAV2FLAC_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def START_WAV2FLAC_BUTTON - start')

      self.button_you2mp3.set_sensitive(False)
      self.button_pwrecord.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_wav2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)


      self.filescan(self.settings['Music_Path'] + '/' + self.settings['Directory_New'])

      self.textbuffer_output.set_text('')

      allfiles = []

      wavfiles = self.get_database_files('.wav')
      allfiles.extend([['.wav', wavfiles]])

      files_to_change = len(wavfiles)

      self.textbuffer_output.set_text('number of files to change: %s\n' % files_to_change)

      if files_to_change==0:

         if self.settings['Debug']==1:
            print ('def START_WAV2FLAC_BUTTON - no files to change')

         self.button_you2mp3.set_sensitive(True)
         self.button_pwrecord.set_sensitive(True)
         self.button_file2mp3.set_sensitive(True)
         self.button_wav2flac.set_sensitive(True)
         self.button_stop.set_sensitive(False)

      else:

         if self.settings['Debug']==1:
            print ('def START_WAV2FLAC_BUTTON - try start_popen_thread')

         self.timer_wav2flac = GObject.timeout_add(1000, self.refresh_output_textctrl_timer)


         for oldprefix,files in allfiles:

            for pathfile in files:

               # destination_dir  pathfile  newprefix
               dest_filename = self.get_destination_filename((self.settings['Music_Path'] + '/' + self.settings['Directory_New']), pathfile, '.flac')

               # flac --compression-level-8 --replay-gain -s /MyDisc/Audio/Neu/pw-record-4.mp3 --output-name  /MyDisc/Audio/Neu/test.flac
               cwd=self.settings['Music_Path'] + '/' + self.settings['Directory_New']
               cmd=['nice','-n','19',self.settings['Bin_Flac'], '--no-delete-input-file', '--compression-level-8','--replay-gain','-s', pathfile, '--output-name',dest_filename]
               self.main.process_starter(cmd=cmd, cwd=cwd, job='wav2flac', identifier='', source=pathfile)



   def STOP_BUTTON(self, event):

      if self.settings['Debug']==1:
         print ('def STOP_BUTTON - start')


      if hasattr(self, 'timer_wav2flac'):
         GObject.source_remove(self.timer_wav2flac)
      if hasattr(self, 'timer_pwrecord'):
         GObject.source_remove(self.timer_pwrecord)
      if hasattr(self, 'timer_file2mp3'):
         GObject.source_remove(self.timer_file2mp3)
      if hasattr(self, 'timer_you2mp3'):
         GObject.source_remove(self.timer_you2mp3)



      self.main.process_job_killer(job='you2mp3')
      self.main.process_job_killer(job='pwrecord')
      self.main.process_job_killer(job='file2mp3')
      self.main.process_job_killer(job='wav2flac')


      self.button_you2mp3.set_sensitive(True)
      self.button_pwrecord.set_sensitive(True)
      self.button_file2mp3.set_sensitive(True)
      self.button_wav2flac.set_sensitive(True)
      self.button_stop.set_sensitive(False)
