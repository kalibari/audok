#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import os
import re


class TabTwo(wx.Panel):

	def __init__(self, p3):

		wx.Panel.__init__(self, parent=p3, id=wx.ID_ANY)

		self.p3 = p3

		self.file_database = {}


		###### BUTTONS ######
		newid = wx.NewId()
		add_AUDIO_STATICTEXT = wx.StaticText(self, id=newid, label='Audio:')
		newid = wx.NewId()
		self.add_START_YOU2MP3_BUTTON = wx.Button(self, id=newid, label='you2mp3', pos=(0, 0), size=(120, 30))
		self.add_START_YOU2MP3_BUTTON.SetToolTip(wx.ToolTip('youtube-dl (mp3) download to Directory New: %s' % self.p3.p2.p1.settings['Directory_New']))
		self.Bind(wx.EVT_BUTTON, self.START_YOU2MP3_BUTTON , id=newid)


		newid = wx.NewId()
		self.add_START_RECORD2WAV_BUTTON = wx.Button(self, id=newid, label='record2wav', pos=(0, 0), size=(120, 30))
		self.add_START_RECORD2WAV_BUTTON.SetToolTip(wx.ToolTip('record file to Directory New: %s' % self.p3.p2.p1.settings['Directory_New']))
		self.Bind(wx.EVT_BUTTON, self.START_RECORD2WAV_BUTTON , id=newid)


		newid = wx.NewId()
		self.add_START_FILE2MP3_BUTTON = wx.Button(self, id=newid, label='file2mp3', pos=(0, 0), size=(120, 30))
		self.add_START_FILE2MP3_BUTTON.SetToolTip(wx.ToolTip('convert all wav,ts,flac,mp4 files in Directory New: %s to mp3' % self.p3.p2.p1.settings['Directory_New']))
		self.Bind(wx.EVT_BUTTON, self.START_FILE2MP3_BUTTON , id=newid)


		newid = wx.NewId()
		self.add_START_WAV2FLAC_BUTTON = wx.Button(self, id=newid, label='wav2flac', pos=(0, 0), size=(120, 30))
		self.add_START_WAV2FLAC_BUTTON.SetToolTip(wx.ToolTip('convert all wav files in Directory New: %s to flac' % self.p3.p2.p1.settings['Directory_New']))
		self.Bind(wx.EVT_BUTTON, self.START_WAV2FLAC_BUTTON , id=newid)


		newid = wx.NewId()
		self.add_STOP_BUTTON = wx.Button(self, id=newid, label='stop', pos=(0, 0), size=(120, 30))
		self.Bind(wx.EVT_BUTTON, self.STOP_BUTTON , id=newid)
		self.add_STOP_BUTTON.Disable()


		###### INPUT ###### 
		newid = wx.NewId()
		add_INPUT_STATICTEXT = wx.StaticText(self, id=newid, label='Input:')

		newid = wx.NewId()
		self.add_INPUT_TEXTCTRL = wx.TextCtrl(self, newid, '', pos=(0, 0), size=(self.p3.p2.p1.settings['Size_X'] - 30, 30), style=wx.SUNKEN_BORDER)
		self.Bind(wx.EVT_TEXT, None, id=newid)



		###### OUTPUT ###### 
		newid = wx.NewId()
		add_OUTPUT_STATICTEXT = wx.StaticText(self, id=newid, label='Output:')

		newid = wx.NewId()
		self.add_OUTPUT_TEXTCTRL = wx.TextCtrl(self, newid, '', (0, wx.ALL), size=(self.p3.p2.p1.settings['Size_X'] - 30, -1), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_DONTWRAP|wx.SUNKEN_BORDER)
		self.Bind(wx.EVT_TEXT, None, id=newid)



		###### BUTTONS ###### 
		add_hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(add_AUDIO_STATICTEXT, 0, wx.ALL, 4)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(self.add_START_YOU2MP3_BUTTON, 0, wx.ALL, 0)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(self.add_START_RECORD2WAV_BUTTON, 0, wx.ALL, 0)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(self.add_START_FILE2MP3_BUTTON, 0, wx.ALL, 0)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(self.add_START_WAV2FLAC_BUTTON, 0, wx.ALL, 0)
		add_hbox1.AddSpacer((20,5))
		add_hbox1.Add(self.add_STOP_BUTTON, 0, wx.ALL, 0)



		###### INPUT ###### 
		add_hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(add_INPUT_STATICTEXT, 0, wx.ALL, 0)
		add_hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox3.AddSpacer((5,5))
		add_hbox3.Add(self.add_INPUT_TEXTCTRL, 1, wx.EXPAND, 0)


		###### OUTPUT ###### 
		add_hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox4.AddSpacer((5,5))
		add_hbox4.Add(add_OUTPUT_STATICTEXT, 0, wx.ALL, 0)
		add_hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox5.AddSpacer((5,5))
		add_hbox5.Add(self.add_OUTPUT_TEXTCTRL, 1, wx.EXPAND, 0)



		vsizer = wx.BoxSizer(wx.VERTICAL)

		###### BUTTONS ###### 
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox1, 0, wx.ALL, 0)

		###### INPUT ###### 
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox2, 0, wx.ALL, 0)
		vsizer.Add(add_hbox3, 0, wx.EXPAND, 0)

		###### OUTPUT ###### 
		vsizer.AddSpacer((5,5))
		vsizer.AddStretchSpacer()
		vsizer.Add(add_hbox4, 0, wx.ALL, 0)
		vsizer.Add(add_hbox5, 100, wx.EXPAND, 0)


		self.SetSizer(vsizer)


		if self.p3.p2.p1.settings['Debug']==1:
			print 'def init TabTwo ends'



	def get_database_files(self, value):
		files = []
		for k in self.file_database:
			if self.file_database[k][0]==value:
				files.extend([k])
		return files



	def get_destination_filename(self, destination_dir, pathfile, newprefix):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def get_destination_filename destination_dir: %s pathfile: %s newprefix: %s' % (destination_dir, pathfile, newprefix)

		# destination_dir: /MyDisc/Audio/Neu filename: /MyDisc/Audio/Neu/parecord-20.wav oldprefix: .wav newprefix: .mp3

		self.filescan(destination_dir)

		# ('parecord-24','.wav')
		(newpart1,newpart2) = os.path.splitext(os.path.basename(pathfile))

		num=0
		newpart1pre = newpart1
		x = re.search('^(.*)-(\d+)$', newpart1pre)
		if x and x.group(1) and x.group(2):
			newpart1pre = x.group(1)
			num = int(x.group(2))

		# parecord
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def get_destination_filename newpart1pre: %s num: %s' % (newpart1pre,str(num))

		for item in self.all_files_in_dir:
			x = re.search('^(%s)-(\d+)%s' % (newpart1pre, newprefix), item)
			if x and x.group(1) and x.group(2):
				if self.p3.p2.p1.settings['Debug']==1:
					print 'def get_destination_filename found file %s -> increase num' % item
				if int(x.group(2))>=num:
					num=int(x.group(2))

		num+=1
		dest_filename='%s-%s%s' % (newpart1pre,num,newprefix)

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def get_destination_filename dest_filename: %s' % dest_filename

		return dest_filename





	def filescan(self, path):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def filescan - part: %s' % path


		# reset
		self.file_database = {}
		self.all_files_in_dir = []

		for root, dirs, files in os.walk(path):

			for item in files:

				if root==path:
					self.all_files_in_dir.extend([item])

				if 'incomplete' in root:
					pass
				elif root==self.p3.p2.p1.settings['Directory_Old']:
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






	def refresh_output_textctrl_timer(self, event):

		inactive_processes=0

		# copy dict to prevent ->  RuntimeError: dictionary changed size during iteration
		loop_process_database = dict(self.p3.process_database)

		for item in loop_process_database:

			if self.p3.p2.p1.settings['Debug']==1:
				print '\ndef refresh_output_textctrl_timer process_database: %s' % str(self.p3.process_database[item])


			if self.p3.process_database[item]['status']=='inactive':
				inactive_processes+=1


			if self.p3.process_database[item]['status']=='active' or self.p3.process_database[item]['status']=='killed':

				if self.p3.process_database[item]['status']=='killed':
					self.p3.process_database[item]['status']='inactive'


				############
				### show ###
				############
				if self.p3.process_database[item]['todo']=='show':

					if self.p3.process_database[item]['job']=='you2mp3':

						if self.p3.process_database[item]['output']:
							self.add_OUTPUT_TEXTCTRL.AppendText('%s\n' % '\n'.join(self.p3.process_database[item]['output']))
							self.p3.process_database[item]['output']=[]


					if self.p3.process_database[item]['job']=='record2wav':

						if self.p3.process_database[item]['identifier']=='pacmd':
							self.add_OUTPUT_TEXTCTRL.AppendText('%s\n' % self.p3.process_database[item]['output'])

						if self.p3.process_database[item]['identifier']=='parecord':
							erg = self.add_OUTPUT_TEXTCTRL.GetValue()
							if hasattr(self, 'textctrl_loop1'):
								self.add_OUTPUT_TEXTCTRL.SetValue(self.textctrl_loop1)
							self.textctrl_loop1 = self.add_OUTPUT_TEXTCTRL.GetValue()
							if self.p3.process_database[item]['output']:
								self.add_OUTPUT_TEXTCTRL.AppendText('%s\n' % self.p3.process_database[item]['output'][-1])
								self.p3.process_database[item]['output']=[]


					if self.p3.process_database[item]['job']=='file2mp3':
						if self.p3.process_database[item]['output']:
							self.add_OUTPUT_TEXTCTRL.AppendText('%s\n' % '\n'.join(self.p3.process_database[item]['output']))
							self.p3.process_database[item]['output']=[]


					if self.p3.process_database[item]['job']=='wav2flac':
						if self.p3.process_database[item]['output']:
							self.add_OUTPUT_TEXTCTRL.AppendText('%s\n' % '\n'.join(self.p3.process_database[item]['output']))
							self.p3.process_database[item]['output']=[]


				##############
				### result ###
				##############
				if self.p3.process_database[item]['todo']=='result':

					# enable buttons, stop refreh timer
					self.add_START_YOU2MP3_BUTTON.Enable()
					self.add_START_RECORD2WAV_BUTTON.Enable()
					self.add_START_FILE2MP3_BUTTON.Enable()
					self.add_START_WAV2FLAC_BUTTON.Enable()
					self.add_STOP_BUTTON.Disable()
					self.refresh_timer.Stop()


					if self.p3.process_database[item]['job']=='you2mp3':
						self.p3.process_database[item]['status']='inactive'
						if self.p3.process_database[item]['result']==True:
							self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s successfully done\n' % self.p3.process_database[item]['job'])
							self.add_INPUT_TEXTCTRL.Clear()
						else:
							self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s error\n' % self.p3.process_database[item]['job'])


					if self.p3.process_database[item]['job']=='record2wav':
						if self.p3.process_database[item]['identifier']=='pacmd':
							self.p3.process_database[item]['status']='inactive'
							if self.p3.process_database[item]['result']==True:
								self.start_parecord(self.p3.process_database[item])
							else:
								self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s aborted\n' % self.p3.process_database[item]['job'])
						if self.p3.process_database[item]['identifier']=='parecord':
							self.p3.process_database[item]['status']='inactive'



					if self.p3.process_database[item]['job']=='file2mp3':
						self.p3.process_database[item]['status']='inactive'
						if self.p3.process_database[item]['result']==True:
							self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s filename: %s successfully converted\n' % (self.p3.process_database[item]['job'],self.p3.process_database[item]['source']))
							if (os.path.exists(self.p3.p2.p1.settings['Directory_Old']))==False:
								os.mkdir(self.p3.p2.p1.settings['Directory_Old'])
							oldfilename = os.path.basename(self.p3.process_database[item]['source'])
							os.rename(self.p3.process_database[item]['source'],'%s/%s' % (self.p3.p2.p1.settings['Directory_Old'],oldfilename))
						else:
							self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s filename: %s error: %s\n' % (self.p3.process_database[item]['job'],self.p3.process_database[item]['source'],self.p3.process_database[item]['output']))



					if self.p3.process_database[item]['job']=='wav2flac':
						self.p3.process_database[item]['status']='inactive'
						if self.p3.process_database[item]['result']==True:
							self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s filename: %s successfully converted\n' % (self.p3.process_database[item]['job'],self.p3.process_database[item]['source']))
							if (os.path.exists(self.p3.p2.p1.settings['Directory_Old']))==False:
								os.mkdir(self.p3.p2.p1.settings['Directory_Old'])
							oldfilename = os.path.basename(self.p3.process_database[item]['source'])
							os.rename(self.p3.process_database[item]['source'],'%s/%s' % (self.p3.p2.p1.settings['Directory_Old'],oldfilename))
						else:
							self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s filename: %s error: %s\n' % (self.p3.process_database[item]['job'],self.p3.process_database[item]['source'],self.p3.process_database[item]['output']))



		if len(self.p3.process_database)==inactive_processes:
			self.refresh_timer.Stop()




	def start_parecord(self, process_database):

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def start_parecord - start job: %s' % process_database['job']


		output_device=''
		for item in process_database['output']:
			x1 = re.search('\s*Default sink name:\s*(alsa_output.*)', item)
			if x1 and x1.group(1):
				output_device=x1.group(1)
				break


		if not output_device:
			self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s cannot find a output_device' % process_database['job'])
		else:
			self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s output_device: %s\n' % (process_database['job'],output_device))

			if not 'monitor' in output_device:
				output_device = '%s.monitor' % output_device


			filename=self.add_INPUT_TEXTCTRL.GetValue()
			if filename:
				filename=(filename.encode('utf-8')).strip()
			if not filename:
				filename = self.p3.p2.p1.settings['Record2wav_Default_Wav_Filename']


			if '/' in filename:
				self.add_OUTPUT_TEXTCTRL.AppendText('-- job: %s / in filename is not allowed' % process_database['job'])
			else:

				self.add_START_YOU2MP3_BUTTON.Disable()
				self.add_START_RECORD2WAV_BUTTON.Disable()
				self.add_START_FILE2MP3_BUTTON.Disable()
				self.add_START_WAV2FLAC_BUTTON.Disable()
				self.add_STOP_BUTTON.Enable()

				
				wavfiles = self.get_database_files('.wav')
				num=0
				for item in wavfiles:
					x = re.search('%s-(\d+).wav' % filename, os.path.basename(item))
					if x and x.group(1):
						if int(x.group(1))>num:
							num=int(x.group(1))
				newfilename='%s-%d.wav' % (filename, (num+1))

				self.refresh_timer = wx.Timer(self)
				self.Bind(wx.EVT_TIMER, self.refresh_output_textctrl_timer, self.refresh_timer)
				self.refresh_timer.Start(1000)

				# parecord --verbose --record --channels=2 --format=s24le --rate=48000 --file-format=wav /MyDisc/Audio/Neu/test.wav
				cmd=['parecord','--verbose','--record','--channels=2', '--format=s24le', '--rate=48000', '--file-format=wav', '--volume=60000',\
				'--device=%s' % output_device, '%s/%s' % (self.p3.p2.p1.settings['Directory_New'],newfilename)]
				cwd=self.p3.p2.p1.settings['Directory_New']
				self.p3.process_starter(cmd=cmd, cwd=cwd, job='record2wav', identifier='parecord', source='')





	###### BUTTONS ######

	def START_YOU2MP3_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def START_YOU2MP3_BUTTON - start'

		self.add_START_YOU2MP3_BUTTON.Disable()
		self.add_START_RECORD2WAV_BUTTON.Disable()
		self.add_START_FILE2MP3_BUTTON.Disable()
		self.add_START_WAV2FLAC_BUTTON.Disable()
		self.add_STOP_BUTTON.Enable()

		self.add_OUTPUT_TEXTCTRL.Clear()


		# youtube-dl --help
		# youtube-dl --no-warnings --no-call-home --audio-quality=4 --extract-audio --audio-format=mp3 --title https://www.youtube.com/watch?v=w7BE3inS-NM

		source=str(self.add_INPUT_TEXTCTRL.GetValue()).strip()
		if not source:

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def START_YOU2MP3_BUTTON - no source'
			
			self.add_OUTPUT_TEXTCTRL.AppendText('no url in "Input:" textctrl, try for example: https://www.youtube.com/watch?v=w7BE3inS-NM\n')
			self.add_START_YOU2MP3_BUTTON.Enable()
			self.add_START_RECORD2WAV_BUTTON.Enable()
			self.add_START_FILE2MP3_BUTTON.Enable()
			self.add_START_WAV2FLAC_BUTTON.Enable()
			self.add_STOP_BUTTON.Disable()

		else:

			self.add_OUTPUT_TEXTCTRL.AppendText('-- job you2mp3 source: %s\n' % source)

			self.refresh_timer = wx.Timer(self)
			self.Bind(wx.EVT_TIMER, self.refresh_output_textctrl_timer, self.refresh_timer)
			self.refresh_timer.Start(1000)


			# youtube-dl https://www.youtube.com/watch?v=fKopy74weus&index=2&list=PL6D4C31FFA7EBABB5

			# youtube-dl --audio-quality=4 --no-warnings --no-call-home --extract-audio --audio-format=mp3 --exec 'echo done' --title https://www.youtube.com/watch....

			cmd=['youtube-dl','--audio-quality=4','--no-warnings','--no-call-home','--extract-audio','--audio-format=mp3','--exec','exit 0','--title',source]
			cwd=self.p3.p2.p1.settings['Directory_New']
			self.p3.process_starter(cmd=cmd, cwd=cwd, job='you2mp3', identifier='', source='')





	def START_RECORD2WAV_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def START_RECORD2WAV_BUTTON - start'


		self.add_START_YOU2MP3_BUTTON.Disable()
		self.add_START_RECORD2WAV_BUTTON.Disable()
		self.add_START_FILE2MP3_BUTTON.Disable()
		self.add_START_WAV2FLAC_BUTTON.Disable()
		self.add_STOP_BUTTON.Enable()


		self.filescan(self.p3.p2.p1.settings['Directory_New'])

		self.add_OUTPUT_TEXTCTRL.Clear()

		self.refresh_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.refresh_output_textctrl_timer, self.refresh_timer)
		self.refresh_timer.Start(1000)

		# pacmd stat | grep "Default sink name"
		cmd=['pacmd','stat']
		cwd='/usr/bin'
		self.p3.process_starter(cmd=cmd, cwd=cwd, job='record2wav', identifier='pacmd', source='')




	def START_FILE2MP3_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def START_FILE2MP3_BUTTON - start'


		self.add_START_YOU2MP3_BUTTON.Disable()
		self.add_START_RECORD2WAV_BUTTON.Disable()
		self.add_START_FILE2MP3_BUTTON.Disable()
		self.add_START_WAV2FLAC_BUTTON.Disable()
		self.add_STOP_BUTTON.Enable()

		self.filescan(self.p3.p2.p1.settings['Directory_New'])

		self.add_OUTPUT_TEXTCTRL.Clear()


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

		self.add_OUTPUT_TEXTCTRL.AppendText('number of files to change: %s\n' % files_to_change)

		if files_to_change==0:

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def START_FILE2MP3_BUTTON - no files to change'
			
			self.add_START_YOU2MP3_BUTTON.Enable()
			self.add_START_RECORD2WAV_BUTTON.Enable()
			self.add_START_FILE2MP3_BUTTON.Enable()
			self.add_START_WAV2FLAC_BUTTON.Enable()
			self.add_STOP_BUTTON.Disable()


		else:

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def START_FILE2MP3_BUTTON - try start_popen_thread'


			self.refresh_timer = wx.Timer(self)
			self.Bind(wx.EVT_TIMER, self.refresh_output_textctrl_timer, self.refresh_timer)
			self.refresh_timer.Start(1000)

			for oldprefix,files in allfiles:

				for pathfile in files:

					# destination_dir  pathfile  newprefix
					dest_filename = self.get_destination_filename(self.p3.p2.p1.settings['Directory_New'], pathfile, '.mp3')

					cwd=self.p3.p2.p1.settings['Directory_New']
					cmd=['nice','-n','19','ffmpeg','-v','error','-i',pathfile,'-ab', '%s' % str(self.p3.p2.p1.settings['File2mp3_Bitrate']),'-n',dest_filename]
					self.p3.process_starter(cmd=cmd, cwd=cwd, job='file2mp3', identifier='', source=pathfile)




	def START_WAV2FLAC_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def START_WAV2FLAC_BUTTON - start'

		self.add_START_YOU2MP3_BUTTON.Disable()
		self.add_START_RECORD2WAV_BUTTON.Disable()
		self.add_START_FILE2MP3_BUTTON.Disable()
		self.add_START_WAV2FLAC_BUTTON.Disable()
		self.add_STOP_BUTTON.Enable()

		self.filescan(self.p3.p2.p1.settings['Directory_New'])

		self.add_OUTPUT_TEXTCTRL.Clear()

		allfiles = []

		wavfiles = self.get_database_files('.wav')
		allfiles.extend([['.wav', wavfiles]])

		files_to_change = len(wavfiles)

		self.add_OUTPUT_TEXTCTRL.AppendText('number of files to change: %s\n' % files_to_change)

		if files_to_change==0:

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def START_WAV2FLAC_BUTTON - no files to change'

			self.add_START_YOU2MP3_BUTTON.Enable()
			self.add_START_RECORD2WAV_BUTTON.Enable()
			self.add_START_FILE2MP3_BUTTON.Enable()
			self.add_START_WAV2FLAC_BUTTON.Enable()
			self.add_STOP_BUTTON.Disable()

		else:

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def START_WAV2FLAC_BUTTON - try start_popen_thread'

			self.refresh_timer = wx.Timer(self)
			self.Bind(wx.EVT_TIMER, self.refresh_output_textctrl_timer, self.refresh_timer)
			self.refresh_timer.Start(1000)


			for oldprefix,files in allfiles:

				for pathfile in files:

					# destination_dir  pathfile  newprefix
					dest_filename = self.get_destination_filename(self.p3.p2.p1.settings['Directory_New'], pathfile, '.flac')

					# flac --compression-level-8 --replay-gain -s /MyDisc/Audio/Neu/parecord-4.mp3 --output-name  /MyDisc/Audio/Neu/test.flac
					cwd=self.p3.p2.p1.settings['Directory_New']
					cmd=['nice','-n','19','flac', '--no-delete-input-file', '--compression-level-8','--replay-gain','-s', pathfile, '--output-name',dest_filename]
					self.p3.process_starter(cmd=cmd, cwd=cwd, job='wav2flac', identifier='', source=pathfile)



	def STOP_BUTTON(self, event):

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def STOP_BUTTON - start'

		self.refresh_timer.Stop()

		self.p3.process_job_killer(job='you2mp3')
		self.p3.process_job_killer(job='record2wav')
		self.p3.process_job_killer(job='file2mp3')
		self.p3.process_job_killer(job='wav2flac')


		self.add_START_YOU2MP3_BUTTON.Enable()
		self.add_START_RECORD2WAV_BUTTON.Enable()
		self.add_START_FILE2MP3_BUTTON.Enable()
		self.add_START_WAV2FLAC_BUTTON.Enable()
		self.add_STOP_BUTTON.Disable()

