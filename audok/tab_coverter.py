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


      #############################
      box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

      row1 = Gtk.ListBoxRow()
      hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox1.set_hexpand(True)
      row1.add(hbox1)

      label1 = Gtk.Label('Audio', xalign=0)
      label1.set_size_request(50, -1)


      self.button_you2mp3 = Gtk.Button(label='you2mp3')
      self.button_you2mp3.connect('clicked', self.START_YOU2MP3_BUTTON)
      self.button_you2mp3.set_tooltip_text('Convert a youtube video to mp3 - Directory: %s' % self.settings['Directory_New'])


      self.button_pwrecord = Gtk.Button(label='pwrecord')
      self.button_pwrecord.connect('clicked', self.START_PWRECORD_BUTTON)
      self.button_pwrecord.set_tooltip_text('Convert a youtube video to mp3 - Directory: %s' % self.settings['Directory_New'])


      self.button_file2mp3 = Gtk.Button(label='file2mp3')
      self.button_file2mp3.connect('clicked', self.START_FILE2MP3_BUTTON)
      self.button_file2mp3.set_tooltip_text('Convert all files to mp3 - Directory: %s' % self.settings['Directory_New'])


      self.button_file2flac = Gtk.Button(label='file2flac')
      self.button_file2flac.connect('clicked', self.START_FILE2FLAC_BUTTON)
      self.button_file2flac.set_tooltip_text('Convert all files to flac - Directory: %s' % self.settings['Directory_New'])


      self.button_stop = Gtk.Button(label='stop')
      self.button_stop.connect('clicked', self.STOP_BUTTON)
      self.button_stop.set_sensitive(False)
      self.button_stop.set_tooltip_text('Stop')


      hbox1.pack_start(label1, False, True, 10)
      hbox1.pack_start(self.button_you2mp3, True, True, 0)
      hbox1.pack_start(self.button_pwrecord, True, True, 0)
      hbox1.pack_start(self.button_file2mp3, True, True, 0)
      hbox1.pack_start(self.button_file2flac, True, True, 0)
      hbox1.pack_start(self.button_stop, True, True, 0)

      #############################

      row2 = Gtk.ListBoxRow()
      hbox2= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox2.set_hexpand(True)
      row2.add(hbox2)


      label2 = Gtk.Label('Input', xalign=0)
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

      label3 = Gtk.Label('Ouput', xalign=0)
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
                  if self.main.process_database[item]['identifier']=='pw-cli':
                     self.textbuffer_output.set_text('%s\n' % self.main.process_database[item]['output'])
                  if self.main.process_database[item]['identifier']=='pw-record':
                     if self.main.process_database[item]['output']:
                        self.textbuffer_output.set_text('%s\n' % self.main.process_database[item]['output'])
                        self.main.process_database[item]['output']=[]



               if self.main.process_database[item]['job']=='file2mp3':
                  if self.main.process_database[item]['output']:
                     self.textbuffer_output.set_text('%s\n' % '\n'.join(self.main.process_database[item]['output']))
                     self.main.process_database[item]['output']=[]


               if self.main.process_database[item]['job']=='file2flac':
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
               self.button_file2flac.set_sensitive(True)
               self.button_stop.set_sensitive(False)



               if self.main.process_database[item]['job']=='you2mp3':
                  self.main.process_database[item]['status']='inactive'
                  if self.main.process_database[item]['result']==True:
                     self.textbuffer_output.set_text('-- job: %s successfully done\n' % self.main.process_database[item]['job'])
                     self.textbuffer_input.set_text('')
                  else:
                     self.textbuffer_output.set_text('-- job: %s error\n' % self.main.process_database[item]['job'])


               if self.main.process_database[item]['job']=='pwrecord':
                  if self.main.process_database[item]['identifier']=='pw-cli':
                     self.main.process_database[item]['status']='inactive'
                     if self.main.process_database[item]['result']==True:
                        self.start_record(self.main.process_database[item])
                     else:
                        self.textbuffer_output.set_text('-- job: %s aborted: %s\n' % (self.main.process_database[item]['job'],self.main.process_database[item]['output']))
                  if self.main.process_database[item]['identifier']=='pw-record':
                     self.main.process_database[item]['status']='inactive'



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



               if self.main.process_database[item]['job']=='file2flac':
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
      self.button_file2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)


      self.textbuffer_output.set_text('')

      source = self.textbuffer_input.get_text().strip()

      if not source:

         self.textbuffer_output.set_text('please insert a input URL')

         self.button_you2mp3.set_sensitive(True)
         self.button_pwrecord.set_sensitive(True)
         self.button_file2mp3.set_sensitive(True)
         self.button_file2flac.set_sensitive(True)
         self.button_stop.set_sensitive(False)


      else:

         self.textbuffer_output.set_text('-- job you2mp3 source: %s\n' % source)


         self.timer_you2mp3 = GObject.timeout_add(1000, self.refresh_output_textctrl_timer)

         # youtube-dl --no-warnings --no-call-home --audio-quality=4 --extract-audio --audio-format=mp3 --title https://www.youtube.com/watch?v=w7BE3inS-NM
         cmd=[self.settings['Bin_Youtubedl'],'--audio-quality=4','--no-warnings','--no-call-home','--extract-audio','--audio-format=mp3','--title',source]
         cwd=self.settings['Music_Path'] + '/' + self.settings['Directory_New']
         self.main.process_starter(cmd=cmd, cwd=cwd, job='you2mp3', identifier='', source='')




   def start_record(self, process_database):

      if self.settings['Debug']==1:
         print ('def start_record - start job: %s' % process_database['job'])

      idnum=-1
      device_target=-1
      for item in process_database['output']:
         x = re.search('^\s*id (\d+), type ', item)
         if x and x.group(1):
            idnum=int(x.group(1))
         x = re.search('^\s*node\.name\ \=\ "%s"\s*$' % self.settings['Pwrecord_Device'], item)
         if x:
            device_target=idnum
            break


      if device_target<0:
         self.textbuffer_output.set_text('-- job: %s cannot find a device target' % process_database['job'])
      else:
         self.textbuffer_output.set_text('-- job: %s device target: %s\n' % (process_database['job'],device_target))


         filename = self.settings['Pwrecord_Default_Filename']
         if self.textbuffer_input.get_text():
            filename = self.textbuffer_input.get_text().encode('utf-8').strip()

         if '/' in filename:
            self.textbuffer_output.set_text('-- job: %s / in filename is not allowed' % process_database['job'])
         else:

            directories = [self.settings['Music_Path'] + '/' + self.settings['Directory_New']]
            extensions = ['mp3','wav','aac','flac']

            allfiles = self.main.file_scan(directories, extensions)

            num=0
            for item in allfiles:
               x = re.search('%s-(\d+).wav' % filename, os.path.basename(item))
               if x and x.group(1):
                  if int(x.group(1))>num:
                     num=int(x.group(1))
            newfilename='%s-%d.wav' % (filename, (num+1))



            self.button_you2mp3.set_sensitive(False)
            self.button_pwrecord.set_sensitive(False)
            self.button_file2mp3.set_sensitive(False)
            self.button_file2flac.set_sensitive(False)
            self.button_stop.set_sensitive(True)
   

            if not os.path.exists(self.settings['Music_Path'] + '/' + self.settings['Directory_New']):
               os.mkdir(self.settings['Music_Path'] + '/' + self.settings['Directory_New'])


            # pw-record --verbose --record --channels=2 --format=s32 --rate=48000 --volume=0.99 --target=41  /MyDisc/Audio/Neu/test.wav
            cmd=[self.settings['Bin_Pwrecord'],'--verbose','--record','--channels=2', '--format=s32', '--rate=48000', '--volume=0.99',\
            '--target=%s' % device_target, '%s/%s/%s' % (self.settings['Music_Path'],self.settings['Directory_New'],newfilename)]
            cwd=self.settings['Music_Path'] + '/' + self.settings['Directory_New']
            self.main.process_starter(cmd=cmd, cwd=cwd, job='pwrecord', identifier='', source='')






   def START_PWRECORD_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def START_PWRECORD_BUTTON - start')


      self.button_you2mp3.set_sensitive(False)
      self.button_pwrecord.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_file2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)

      self.textbuffer_output.set_text('')

      self.timer_pwrecord = GObject.timeout_add(1000, self.refresh_output_textctrl_timer)

      cmd=[self.settings['Bin_Pwcli'],'list-objects']
      cwd='/'
      self.main.process_starter(cmd=cmd, cwd=cwd, job='pwrecord', identifier='pw-cli', source='')




   def START_FILE2MP3_BUTTON(self, event):

      if self.settings['Debug']==1:
         print ('def START_FILE2MP3_BUTTON - start')


      self.button_you2mp3.set_sensitive(False)
      self.button_pwrecord.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_file2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)

      self.textbuffer_output.set_text('')

      directories = [self.settings['Music_Path'] + '/' + self.settings['Directory_New']]
      extensions = ['wav','aac','flac','flv','webm']

      allfiles = self.main.file_scan(directories, extensions)
      mp3files = self.main.file_scan(directories, ['mp3'])


      self.textbuffer_output.set_text('number of files to change: %s\n' % len(allfiles))

      if len(allfiles)==0:

         if self.settings['Debug']==1:
            print ('def START_FILE2MP3_BUTTON - no files to change')
         

         self.button_you2mp3.set_sensitive(True)
         self.button_pwrecord.set_sensitive(True)
         self.button_file2mp3.set_sensitive(True)
         self.button_file2flac.set_sensitive(True)
         self.button_stop.set_sensitive(False)


      else:

         if self.settings['Debug']==1:
            print ('def START_FILE2MP3_BUTTON - try start_popen_thread')

         self.timer_file2mp3 = GObject.timeout_add(1000, self.refresh_output_textctrl_timer)

         for item in allfiles:

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

               cwd=self.settings['Music_Path'] + '/' + self.settings['Directory_New']
               cmd=[self.settings['Bin_Nice'],'-n','19',self.settings['Bin_Ffmpeg'],'-v','error','-i',item,'-ab', '%s' % str(self.settings['Bitrate']),'-n',newfilename]
               self.main.process_starter(cmd=cmd, cwd=cwd, job='file2mp3', identifier='', source=item)




   def START_FILE2FLAC_BUTTON(self, event):

      if self.settings['Debug']==1:
         print ('def START_FILE2FLAC_BUTTON - start')

      self.button_you2mp3.set_sensitive(False)
      self.button_pwrecord.set_sensitive(False)
      self.button_file2mp3.set_sensitive(False)
      self.button_file2flac.set_sensitive(False)
      self.button_stop.set_sensitive(True)

      self.textbuffer_output.set_text('')

      directories = [self.settings['Music_Path'] + '/' + self.settings['Directory_New']]
      extensions = ['wav','aac','mp3','flv','webm']

 
      allfiles = self.main.file_scan(directories, extensions)
      flacfiles = self.main.file_scan(directories, ['flac'])


      self.textbuffer_output.set_text('number of files to change: %s\n' % len(allfiles))

      if len(allfiles)==0:

         if self.settings['Debug']==1:
            print ('def START_FILE2FLAC_BUTTON - no files to change')

         self.button_you2mp3.set_sensitive(True)
         self.button_pwrecord.set_sensitive(True)
         self.button_file2mp3.set_sensitive(True)
         self.button_file2flac.set_sensitive(True)
         self.button_stop.set_sensitive(False)

      else:

         if self.settings['Debug']==1:
            print ('def START_FILE2FLAC_BUTTON - try start_popen_thread')

         self.timer_file2flac = GObject.timeout_add(1000, self.refresh_output_textctrl_timer)



         for item in allfiles:

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


               # ffmpeg -y -i /MyDisc/Audio/Neu/New/pwrecord-1.wav -af aformat=s32:48000 /MyDisc/Audio/Neu/test.flac
               cwd=self.settings['Music_Path'] + '/' + self.settings['Directory_New']
               cmd=['nice','-n','19',self.settings['Bin_Ffmpeg'], '-y', '-i',  item, '-af', 'aformat=s32:48000', newfilename]
               self.main.process_starter(cmd=cmd, cwd=cwd, job='file2flac', identifier='', source=item)




   def STOP_BUTTON(self, event):

      if self.settings['Debug']==1:
         print ('def STOP_BUTTON - start')


      if hasattr(self, 'timer_file2flac'):
         GObject.source_remove(self.timer_file2flac)
      if hasattr(self, 'timer_pwrecord'):
         GObject.source_remove(self.timer_pwrecord)
      if hasattr(self, 'timer_file2mp3'):
         GObject.source_remove(self.timer_file2mp3)
      if hasattr(self, 'timer_you2mp3'):
         GObject.source_remove(self.timer_you2mp3)



      self.main.process_job_killer(job='you2mp3')
      self.main.process_job_killer(job='pwrecord')
      self.main.process_job_killer(job='file2mp3')
      self.main.process_job_killer(job='file2flac')


      self.button_you2mp3.set_sensitive(True)
      self.button_pwrecord.set_sensitive(True)
      self.button_file2mp3.set_sensitive(True)
      self.button_file2flac.set_sensitive(True)
      self.button_stop.set_sensitive(False)
