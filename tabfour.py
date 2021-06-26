#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import os
import re


class TabFour(wx.Panel):

	def __init__(self, p3):

		wx.Panel.__init__(self, parent=p3, id=wx.ID_ANY)

		self.p3 = p3

		self.circle_horizontal = 285
		self.circle_vertical = 53

		newid = wx.NewId()
		add_PULSEAUDIO_STATICTEXT = wx.StaticText(self, id=newid, label='Pulseaudio:')

		###### BUTTONS ######
		newid = wx.NewId()
		self.add_START_DLNA_BUTTON = wx.Button(self, id=newid,  label='dlna', pos=(0, 0), size=(120, 30))
		self.Bind(wx.EVT_BUTTON, self.START_DLNA_BUTTON, id=newid)

		newid = wx.NewId()
		self.add_STOP_DLNA_BUTTON = wx.Button(self, id=newid,  label='stop', pos=(0, 0), size=(120, 30))
		self.Bind(wx.EVT_BUTTON, self.STOP_DLNA_BUTTON, id=newid)
		self.add_STOP_DLNA_BUTTON.Disable()

		###### CIRCLE ######
		self.Bind(wx.EVT_PAINT, self.Circle_Red) 


		###### TextCtrl ######
		newid = wx.NewId()
		add_FILTER_STATICTEXT = wx.StaticText(self, id=newid, label='Filter:')
		newid = wx.NewId()
		self.add_FILTER_TEXTCTRL = wx.TextCtrl(self, newid, '%s' % self.p3.p2.p1.settings['Dlna_Filter'], pos=(0, 0), size=(180, 30), style=wx.SUNKEN_BORDER)
		self.Bind(wx.EVT_TEXT, None, id=newid)


		newid = wx.NewId()
		add_PORT_STATICTEXT = wx.StaticText(self, newid, label='Port:')
		newid = wx.NewId()
		self.add_PORT_TEXTCTRL = wx.TextCtrl(self, newid, '%s' % self.p3.p2.p1.settings['Dlna_Port'], pos=(0, 0), size=(80, 30), style=wx.SUNKEN_BORDER)
		self.Bind(wx.EVT_TEXT, None, id=newid)


		newid = wx.NewId()
		add_DIRECTORIES_STATICTEXT = wx.StaticText(self, newid, label='Directories:')


		bmp = wx.Bitmap('%s/newdir_small.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		add_NEW_STATICBITMAP = wx.StaticBitmap(self, id=wx.ID_ANY, bitmap=bmp, size=(40,35))
		add_NEW_STATICBITMAP.SetToolTip(wx.ToolTip('Directory New: %s' % self.p3.p2.p1.settings['Directory_New']))
		newid = wx.NewId()
		self.add_AUDIO_PATH_NEW_TEXTCTRL = wx.TextCtrl(self, newid, '%s' % self.p3.p2.p1.settings['Directory_New'], pos=(0, 0), size=(300, 30), style=wx.SUNKEN_BORDER)
		self.Bind(wx.EVT_TEXT, None, id=newid)


		bmp = wx.Bitmap('%s/olddir_small.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		newid = wx.NewId()
		add_OLD_STATICBITMAP = wx.StaticBitmap(self, id=newid, bitmap=bmp, size=(40,35))
		add_OLD_STATICBITMAP.SetToolTip(wx.ToolTip('Directory Old: %s' % self.p3.p2.p1.settings['Directory_Old']))
		newid = wx.NewId()
		self.add_AUDIO_PATH_OLD_TEXTCTRL = wx.TextCtrl(self, newid, '%s' % self.p3.p2.p1.settings['Directory_Old'], pos=(0, 0), size=(300, 30), style=wx.SUNKEN_BORDER)
		self.Bind(wx.EVT_TEXT, None, id=newid)


		bmp = wx.Bitmap('%s/streamripperdir_small.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		newid = wx.NewId()
		add_STR_STATICBITMAP = wx.StaticBitmap(self, id=newid, bitmap=bmp, size=(40,35))
		add_STR_STATICBITMAP.SetToolTip(wx.ToolTip('Directory Streamripper: %s' % self.p3.p2.p1.settings['Directory_Streamripper']))
		newid = wx.NewId()
		self.add_STR_PATH_TEXTCTRL = wx.TextCtrl(self, newid, '%s' % self.p3.p2.p1.settings['Directory_Streamripper'], pos=(0, 0), size=(300, 30), style=wx.SUNKEN_BORDER)
		self.Bind(wx.EVT_TEXT, None, id=newid)

		newid = wx.NewId()
		add_CONVERTER_STATICTEXT = wx.StaticText(self, id=newid, label='Converter:')


		newid = wx.NewId()
		add_FILE2MP3BITRATE_STATICTEXT = wx.StaticText(self, id=newid, label='file2mp3 bitrate:')
		newid = wx.NewId()
		add_FILE2MP3BITRATE_COMBOBOX = wx.ComboBox(self, id=newid, value=self.p3.p2.p1.settings['File2mp3_Bitrate'], pos=(0, 0), size=(120, 30), choices=self.p3.p2.p1.settings['Choice_File2mp3_Bitrate'].split(','), style=wx.CB_DROPDOWN)
		self.Bind(wx.EVT_COMBOBOX, self.FILE2MP3BITRATE_COMBOBOX, id=newid)


		newid = wx.NewId()
		self.add_SAVE_BUTTON = wx.Button(self, id=newid, label='save', pos=(0, 0), size=(80, 30))
		self.Bind(wx.EVT_BUTTON, self.SAVE_BUTTON, id=newid)

		newid = wx.NewId()
		self.add_RESET_BUTTON = wx.Button(self, id=newid, label='reset', pos=(0, 0), size=(80, 30))
		self.Bind(wx.EVT_BUTTON, self.RESET_BUTTON, id=newid)


		newid = wx.NewId()
		self.add_ABOUT_BUTTON = wx.Button(self, id=newid, label='about', pos=(0, 0), size=(115, 30))
		self.Bind(wx.EVT_BUTTON, self.ABOUT_BUTTON, id=newid)


		add_hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(add_PULSEAUDIO_STATICTEXT, 0, wx.ALL, 4)

		###### BUTTONS ######
		add_hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(self.add_START_DLNA_BUTTON, 0, wx.ALL, 0)
		add_hbox2.Add(self.add_STOP_DLNA_BUTTON, 0, wx.ALL, 0)
		add_hbox2.AddSpacer((70,5))

		###### TEXTCTRL ######
		add_hbox2.Add(add_FILTER_STATICTEXT, 0, wx.ALL, 4)
		add_hbox2.Add(self.add_FILTER_TEXTCTRL, 0, wx.ALL, 0)
		add_hbox2.Add(add_PORT_STATICTEXT, 0, wx.ALL, 4)
		add_hbox2.Add(self.add_PORT_TEXTCTRL, 0, wx.ALL, 0)


		add_hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox3.Add(add_DIRECTORIES_STATICTEXT, 0, wx.ALL, 4)


		###### TEXTCTRL ######
		add_hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox4.AddSpacer((5,5))
		add_hbox4.Add(add_NEW_STATICBITMAP, 0, wx.ALL, -2)
		add_hbox4.AddSpacer((5,5))
		add_hbox4.Add(self.add_AUDIO_PATH_NEW_TEXTCTRL, 0, wx.ALL, 0)



		add_hbox6 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox6.AddSpacer((5,5))
		add_hbox6.Add(add_OLD_STATICBITMAP, 0, wx.ALL, -2)
		add_hbox6.AddSpacer((5,5))
		add_hbox6.Add(self.add_AUDIO_PATH_OLD_TEXTCTRL, 0, wx.ALL, 0)


		add_hbox7 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox7.AddSpacer((5,5))
		add_hbox7.Add(add_STR_STATICBITMAP, 0, wx.ALL, -2)
		add_hbox7.AddSpacer((5,5))
		add_hbox7.Add(self.add_STR_PATH_TEXTCTRL, 0, wx.ALL, 0)



		add_hbox8 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox8.AddSpacer((5,5))
		add_hbox8.Add(add_CONVERTER_STATICTEXT, 0, wx.ALL, 0)


		add_hbox9 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox9.AddSpacer((5,5))
		add_hbox9.Add(add_FILE2MP3BITRATE_STATICTEXT, 0, wx.ALL, 4)
		add_hbox9.AddSpacer((5,5))
		add_hbox9.Add(add_FILE2MP3BITRATE_COMBOBOX, 0, wx.ALL, 0)


		add_hbox10 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox10.AddSpacer((5,5))
		add_hbox10.Add(self.add_SAVE_BUTTON, 0, wx.ALL, 0)
		add_hbox10.AddSpacer((5,5))
		add_hbox10.Add(self.add_RESET_BUTTON, 0, wx.ALL, 0)
		add_hbox10.AddSpacer((50,5))
		add_hbox10.Add(self.add_ABOUT_BUTTON, 0, wx.ALL, 0)


		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.AddSpacer((5,5))

		vsizer.Add(add_hbox1, 0, wx.ALL, 0)
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox2, 0, wx.ALL, 0)
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox3, 0, wx.ALL, 0)
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox4, 0, wx.ALL, 0)
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox6, 0, wx.ALL, 0)
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox7, 0, wx.ALL, 0)
		vsizer.AddSpacer((5,10))
		vsizer.Add(add_hbox8, 0, wx.ALL, 0)
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox9, 0, wx.ALL, 0)

		vsizer.AddStretchSpacer()
		vsizer.Add(add_hbox10, 0, wx.ALL, 0)

		self.SetSizer(vsizer)

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def init TabFour ends'




	def Circle_Red(self, event):
		dc = wx.PaintDC(self)
		# red green blue
		color = wx.Colour(255,0,0)
		b = wx.Brush(color)
		dc.SetBrush(b)
		# horizontal, vertical, size
		dc.DrawCircle(self.circle_horizontal,self.circle_vertical,15)
		# white small circle
		dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
		dc.DrawCircle(self.circle_horizontal,self.circle_vertical,8)


	def Circle_Green(self, event):
		dc = wx.PaintDC(self)
		# red green blue
		color = wx.Colour(0,170,90)
		b = wx.Brush(color)
		dc.SetBrush(b)
		# horizontal, vertical, size
		dc.DrawCircle(self.circle_horizontal,self.circle_vertical,15)
		# white small circle
		dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
		dc.DrawCircle(self.circle_horizontal,self.circle_vertical,8)


	def Circle_Orange(self, event):
		dc = wx.PaintDC(self)
		# red green blue
		color = wx.Colour(255,126,0)
		b = wx.Brush(color)
		dc.SetBrush(b)
		# horizontal, vertical, size
		dc.DrawCircle(self.circle_horizontal,self.circle_vertical,15)
		# white small circle
		dc.SetBrush(wx.Brush(wx.Colour(255,255,255)))
		dc.DrawCircle(self.circle_horizontal,self.circle_vertical,8)



	def change_dlna_colour(self, colour):

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def change_dlna_colour - colour: %s' % colour

		if colour=='red':
			self.Bind(wx.EVT_PAINT, self.Circle_Red)
		if colour=='orange':
			self.Bind(wx.EVT_PAINT, self.Circle_Orange)
		if colour=='green':
			self.Bind(wx.EVT_PAINT, self.Circle_Green) 

		self.Refresh()




	def FILE2MP3BITRATE_COMBOBOX(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def FILE2MP3BITRATE_COMBOBOX - start - choose: %s' % event.GetString()


	def SAVE_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def SAVE_BUTTON - start'

		self.p3.p2.p1.settings['Directory_New'] = self.add_AUDIO_PATH_NEW_TEXTCTRL.GetValue()
		self.p3.p2.p1.settings['Directory_Old'] = self.add_AUDIO_PATH_OLD_TEXTCTRL.GetValue()
		self.p3.p2.p1.settings['Directory_Streamripper'] = self.add_STR_PATH_TEXTCTRL.GetValue()
		self.p3.p2.p1.settings['Dlna_Port'] = self.add_PORT_TEXTCTRL.GetValue()
		self.p3.p2.p1.settings['Dlna_Filter'] = self.add_FILTER_TEXTCTRL.GetValue()


		if not os.path.exists('%s/.config/audok' % os.environ['HOME']):
			os.mkdir('%s/.config/audok' % os.environ['HOME'], 0755 );

		f = open('%s/.config/audok/settings.xml' % os.environ['HOME'], 'w')


		f.write('<?xml version="1.0"?>\n')
		f.write('<data>\n')
		for item1 in self.p3.p2.p1.settings:
			f.write('\t<' + str(item1) + '>' + str(self.p3.p2.p1.settings[item1]) + '</' + str(item1) + '>\n')
		f.write('</data>\n')

		f.close()




	def RESET_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def RESET_BUTTON - start'

		self.p3.p2.OnClose(None)

		if os.path.exists('%s/.config/audok/settings.xml' % os.environ['HOME']):
			os.remove('%s/.config/audok/settings.xml' % os.environ['HOME'])
	



	def ABOUT_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def ABOUT_BUTTON - start'

		info = wx.AboutDialogInfo()
		info.Name = self.p3.p2.p1.settings['Name']
		info.Version = self.p3.p2.p1.settings['Version']
		info.Licence = 'GNU GENERAL PUBLIC LICENSE Version 3\n'
		info.Icon = wx.Icon('%s/audok.ico' % self.p3.p2.p1.settings['Path'] , wx.BITMAP_TYPE_ICO)
		info.Copyright = 'Copyright (c) 2017\nkalibari\n'
		info.Description = 'Music Player'
		info.WebSite = ("https://github.com/kalibari/audok", "Audok")
		wx.AboutBox(info)



	def START_DLNA_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def START_DLNA_BUTTON - start pulseaudio-dlna'

		self.add_START_DLNA_BUTTON.Disable()
		self.add_STOP_DLNA_BUTTON.Enable()

		# /usr/bin/pulseaudio-dlna --filter-device 'Chromecast' --port 10291

		dlna_filter=''
		cmd = []
		if bool(self.p3.p2.p1.settings['Dlna_Filter']):
			cmd=['pulseaudio-dlna','--port','%s' % self.p3.p2.p1.settings['Dlna_Port'], '--filter-device','%s' % self.p3.p2.p1.settings['Dlna_Filter']]
		else:
			cmd=['pulseaudio-dlna','--port','%s' % self.p3.p2.p1.settings['Dlna_Port']]


		cwd='/usr/bin'
		self.p3.process_starter(cmd=cmd, cwd=cwd, job='dlna', identifier='', source='')

		self.refresh_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.refresh_circle_timer, self.refresh_timer)
		self.refresh_timer.Start(1000)



	def STOP_DLNA_BUTTON(self, event):

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def STOP_DLNA_BUTTON - start'

		self.add_START_DLNA_BUTTON.Enable()
		self.add_STOP_DLNA_BUTTON.Disable()

		self.change_dlna_colour('red')
		self.refresh_timer.Stop()

		self.p3.process_job_killer(job='dlna')



	def refresh_circle_timer(self, event):

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def refresh_circle_timer start'


		for item in self.p3.process_database:

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def refresh_circle_timer process_database: %s' % str(self.p3.process_database[item])


			if self.p3.process_database[item]['status']=='active' or self.p3.process_database[item]['status']=='killed':

				if self.p3.process_database[item]['status']=='killed':
					self.p3.process_database[item]['status']='inactive'


				############
				### show ###
				############
				if self.p3.process_database[item]['todo']=='show':

					if self.p3.process_database[item]['job']=='dlna':

						if self.p3.process_database[item]['output']:

							for out in self.p3.process_database[item]['output']:
								
								x1 = re.search('Using localhost.*%s' % self.p3.p2.p1.settings['Dlna_Port'], out)
								if x1:
									self.change_dlna_colour('orange')
								x2 = re.search('could not determine your host address', out)
								if x2:
									self.change_dlna_colour('red')
								x3 = re.search('Added the device.*%s' % self.p3.p2.p1.settings['Dlna_Filter'], out)
								if x3:
									self.change_dlna_colour('green')


							self.p3.process_database[item]['output']=[]


				##############
				### result ###
				##############
				if self.p3.process_database[item]['todo']=='result':

					if self.p3.process_database[item]['job']=='dlna':

						self.p3.process_database[item]['status']='inactive'

						for item in self.p3.process_database[item]['output']:
							x1 = re.search('Application is shutting down', item)
							if x1:
								self.change_dlna_colour('red')


						self.refresh_timer.Stop()

