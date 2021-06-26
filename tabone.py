#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import wx.media
import os
import re
import random
import threading
import signal
import time


class TabOne(wx.Panel):

	def __init__(self, p3):

		wx.Panel.__init__(self, parent=p3, id=wx.ID_ANY)

		self.p3 = p3


		###### MUSIC SETTINGS ###### 
		newid = wx.NewId()
		add_PLAY_TIME_STATICTEXT = wx.StaticText(self, id=newid, label='Play Time:')
		newid = wx.NewId()
		self.add_PLAY_TIME_COMBOBOX = wx.ComboBox(self, id=newid, value=self.p3.p2.p1.settings['Play_Time'], pos=(0, 0), size=(90, 30), choices=self.p3.p2.p1.settings['Choice_Play_Time'].split(','), style=wx.CB_DROPDOWN)
		self.Bind(wx.EVT_COMBOBOX, self.PLAY_TIME_COMBOBOX, id=newid)


		newid = wx.NewId()
		add_RANDOM_STATICTEXT = wx.StaticText(self, id=newid, label='Random start:')
		newid = wx.NewId()
		self.add_RANDOM_COMBOBOX = wx.ComboBox(self, id=newid, value=self.p3.p2.p1.settings['Random_Time'], pos=(0, 0), size=(120, 30), choices=self.p3.p2.p1.settings['Choice_Random_Time'].split(','), style=wx.CB_DROPDOWN)
		self.Bind(wx.EVT_COMBOBOX, self.RANDOM_COMBOBOX, id=newid)


		bmp = wx.Bitmap('%s/loop_small.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		newid = wx.NewId()
		add_LOOP_STATICBITMAP = wx.StaticBitmap(self, id=newid, bitmap=bmp, size=(40,35))
		add_LOOP_STATICBITMAP.SetToolTip(wx.ToolTip('Loop Files in Dir'))
		newid = wx.NewId()
		self.add_LOOP_CHECKBOX = wx.CheckBox(self, id=newid, name='', pos=(0, 0), size=(30, 30))
		self.Bind(wx.EVT_BUTTON, None , id=newid)
		self.add_LOOP_CHECKBOX.SetValue(True)
		self.add_LOOP_CHECKBOX.SetToolTip(wx.ToolTip('Loop Files in Dir'))


		bmp = wx.Bitmap('%s/auto_olddir_small.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		add_AUTO_MV_OLD_STATICBITMAP = wx.StaticBitmap(self, id=wx.ID_ANY, bitmap=bmp, size=(40,35))
		add_AUTO_MV_OLD_STATICBITMAP.SetToolTip(wx.ToolTip('Auto move Files after Play Time to Directory Old: %s' % self.p3.p2.p1.settings['Directory_Old']))
		newid = wx.NewId()
		self.add_AUTO_MV_OLD_CHECKBOX = wx.CheckBox(self, id=newid, name='', pos=(0, 0), size=(30, 30))
		self.add_AUTO_MV_OLD_CHECKBOX.SetToolTip(wx.ToolTip('Auto move Files after Play Time to Directory Old: %s' % self.p3.p2.p1.settings['Directory_Old']))
		self.Bind(wx.EVT_BUTTON, None , id=newid)


		newid = wx.NewId()
		self.add_SCAN_BUTTON = wx.Button(self, id=newid, label='Scan Dir', pos=(0, 0), size=(85, 30))
		self.Bind(wx.EVT_BUTTON, self.SCAN_BUTTON , id=newid)


		bmp = wx.Bitmap('%s/streamripperdir_small.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		newid = wx.NewId()
		add_INCLUDE_STR_STATICBITMAP = wx.StaticBitmap(self, id=newid, bitmap=bmp, size=(40,35))
		add_INCLUDE_STR_STATICBITMAP.SetToolTip(wx.ToolTip('Directory Streamripper: %s' % self.p3.p2.p1.settings['Directory_Streamripper']))
		newid = wx.NewId()
		self.add_INCLUDE_STR_CHECKBOX = wx.CheckBox(self, id=newid, name='', pos=(0, 0), size=(30, 30))
		self.Bind(wx.EVT_BUTTON, None , id=newid)
		self.add_INCLUDE_STR_CHECKBOX.SetToolTip(wx.ToolTip('Directory Streamripper: %s' % self.p3.p2.p1.settings['Directory_Streamripper']))
		self.add_INCLUDE_STR_CHECKBOX.SetValue(True)


		bmp = wx.Bitmap('%s/newdir_small.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		add_INCLUDE_NEW_STATICBITMAP = wx.StaticBitmap(self, id=wx.ID_ANY, bitmap=bmp, size=(40,35))
		add_INCLUDE_NEW_STATICBITMAP.SetToolTip(wx.ToolTip('Directory New: %s' % self.p3.p2.p1.settings['Directory_New']))
		newid = wx.NewId()
		self.add_INCLUDE_NEW_CHECKBOX = wx.CheckBox(self, id=newid, name='', pos=(0, 0), size=(30, 30))
		self.add_INCLUDE_NEW_CHECKBOX.SetToolTip(wx.ToolTip('Directory New: %s' % self.p3.p2.p1.settings['Directory_New']))
		self.Bind(wx.EVT_BUTTON, None , id=newid)


		bmp = wx.Bitmap('%s/olddir_small.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		newid = wx.NewId()
		add_INCLUDE_OLD_STATICBITMAP = wx.StaticBitmap(self, id=newid, bitmap=bmp, size=(40,35))
		add_INCLUDE_OLD_STATICBITMAP.SetToolTip(wx.ToolTip('Directory Old: %s' % self.p3.p2.p1.settings['Directory_Old']))
		newid = wx.NewId()
		self.add_INCLUDE_OLD_CHECKBOX = wx.CheckBox(self, id=newid, name='', pos=(0, 0), size=(30, 30))
		self.add_INCLUDE_OLD_CHECKBOX.SetToolTip(wx.ToolTip('Directory Old: %s' % self.p3.p2.p1.settings['Directory_Old']))
		self.Bind(wx.EVT_BUTTON, None , id=newid)


		# FILES_SUM_TEXTCTRL
		newid = wx.NewId()
		self.add_FILES_SUM_TEXTCTRL = wx.TextCtrl(self, newid, 'Database',  pos=(0, 0), size=(85, 30), style=wx.TE_READONLY & wx.BORDER_NONE)
		self.Bind(wx.EVT_TEXT, None, id=newid)
		self.add_FILES_SUM_TEXTCTRL.Disable()



		###### BUTTONS ######
		bmp = wx.Bitmap('%s/open.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		self.add_OPEN_BUTTON = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp, size=(64,40))
		self.Bind(wx.EVT_BUTTON, self.OPEN_BUTTON , self.add_OPEN_BUTTON)


		bmp = wx.Bitmap('%s/back.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		self.add_BACK_BUTTON = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp, size=(64,40))
		self.Bind(wx.EVT_BUTTON, self.BACK_BUTTON , self.add_BACK_BUTTON)
		self.add_BACK_BUTTON.Disable()
		
		bmp = wx.Bitmap('%s/play.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		self.add_PLAY_BUTTON = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp, size=(64,40))
		self.Bind(wx.EVT_BUTTON, self.PLAY_BUTTON, self.add_PLAY_BUTTON)
		if len(self.p3.p2.p1.playlist)==0:
			self.add_PLAY_BUTTON.Disable()

		bmp = wx.Bitmap('%s/pause.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		self.add_PAUSE_BUTTON = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp, size=(64,40))
		self.Bind(wx.EVT_BUTTON, self.PAUSE_BUTTON , self.add_PAUSE_BUTTON)
		self.add_PAUSE_BUTTON.Disable()

		bmp = wx.Bitmap('%s/next.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		self.add_NEXT_BUTTON = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp, size=(64,40))
		self.Bind(wx.EVT_BUTTON, self.NEXT_BUTTON , self.add_NEXT_BUTTON)
		self.add_NEXT_BUTTON.Disable()


		bmp = wx.Bitmap('%s/olddir.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		self.add_MOVE_OLD_BUTTON = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp, size=(64,40))
		self.add_MOVE_OLD_BUTTON.SetToolTip(wx.ToolTip('move File to Directory Old: %s' % self.p3.p2.p1.settings['Directory_Old']))
		self.Bind(wx.EVT_BUTTON, self.MOVE_OLD_BUTTON , self.add_MOVE_OLD_BUTTON)
		self.add_MOVE_OLD_BUTTON.SetToolTip(wx.ToolTip('move File to Directory Old: %s' % self.p3.p2.p1.settings['Directory_Old']))
		self.add_MOVE_OLD_BUTTON.Disable()


		bmp = wx.Bitmap('%s/newdir.png' % self.p3.p2.p1.settings['Path'], wx.BITMAP_TYPE_ANY)
		self.add_MOVE_NEW_BUTTON = wx.BitmapButton(self, id=wx.ID_ANY, bitmap=bmp, size=(64,40))
		self.add_MOVE_NEW_BUTTON.SetToolTip(wx.ToolTip('move File to Directory New: %s' % self.p3.p2.p1.settings['Directory_New']))
		self.Bind(wx.EVT_BUTTON, self.MOVE_NEW_BUTTON , self.add_MOVE_NEW_BUTTON)
		self.add_MOVE_NEW_BUTTON.SetToolTip(wx.ToolTip('move File to Directory New: %s' % self.p3.p2.p1.settings['Directory_New']))
		self.add_MOVE_NEW_BUTTON.Disable()

		###### SLIDER ######
		newid = wx.NewId()
		self.PLAYBACK_SLIDER = wx.Slider(self, id=newid, size=(self.p3.p2.p1.settings['Size_X']-30, 30), style=wx.SL_HORIZONTAL)
		self.Bind(wx.EVT_SLIDER, self.onSeek, self.PLAYBACK_SLIDER, id=newid)


		###### PLAY FILE ###### 
		newid = wx.NewId()
		add_current_file_STATICTEXT = wx.StaticText(self, id=newid, label='Play File:')

		newid = wx.NewId()
		self.add_play_file_TEXTCTRL = wx.TextCtrl(self, newid, '', pos=(0, 0), size=(self.p3.p2.p1.settings['Size_X'] - 30, 30), style=wx.TE_READONLY|wx.TE_DONTWRAP|wx.SUNKEN_BORDER)
		self.Bind(wx.EVT_TEXT, None, id=newid)



		###### HISTORY ###### 
		newid = wx.NewId()
		add_HISTORY_STATICTEXT = wx.StaticText(self, id=newid, label='History:')

		newid = wx.NewId()
		self.add_HISTORY_TEXTCTRL = wx.TextCtrl(self, newid, '', pos=(0, 0), size=(self.p3.p2.p1.settings['Size_X'] - 30, 30), style=wx.TE_READONLY|wx.TE_MULTILINE|wx.SUNKEN_BORDER)
		self.Bind(wx.EVT_TEXT, None, id=newid)



		###### MUSIC SETTINGS ######
		add_hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(add_PLAY_TIME_STATICTEXT, 0, wx.ALL, 4)
		add_hbox1.Add(self.add_PLAY_TIME_COMBOBOX, 0, wx.ALL, 0)
		add_hbox1.Add(add_RANDOM_STATICTEXT, 0, wx.ALL, 4)
		add_hbox1.Add(self.add_RANDOM_COMBOBOX, 0, wx.ALL, 0)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(add_LOOP_STATICBITMAP, 0, wx.ALL, -2)
		add_hbox1.Add(self.add_LOOP_CHECKBOX, 0, wx.ALL, 0)
		add_hbox1.Add(add_AUTO_MV_OLD_STATICBITMAP, 0, wx.ALL, -2)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(self.add_AUTO_MV_OLD_CHECKBOX, 0, wx.ALL, 0)
		add_hbox1.AddSpacer((20,5))
		add_hbox1.Add(self.add_SCAN_BUTTON, 0, wx.ALL, 0)
		add_hbox1.AddSpacer((5,5))
		add_hbox1.Add(add_INCLUDE_STR_STATICBITMAP, 0, wx.ALL, -2)
		add_hbox1.Add(self.add_INCLUDE_STR_CHECKBOX, 0, wx.ALL, 0)
		add_hbox1.Add(add_INCLUDE_NEW_STATICBITMAP, 0, wx.ALL, -2)
		add_hbox1.Add(self.add_INCLUDE_NEW_CHECKBOX, 0, wx.ALL, 0)
		add_hbox1.Add(add_INCLUDE_OLD_STATICBITMAP, 0, wx.ALL, -2)
		add_hbox1.Add(self.add_INCLUDE_OLD_CHECKBOX, 0, wx.ALL, 0)
		add_hbox1.Add(self.add_FILES_SUM_TEXTCTRL, 0, wx.ALL, 0)

		###### BUTTONS ######
		add_hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(self.add_OPEN_BUTTON, 0, wx.ALL, 0)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(self.add_BACK_BUTTON, 0, wx.ALL, 0)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(self.add_PLAY_BUTTON, 0, wx.ALL, 0)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(self.add_NEXT_BUTTON, 0, wx.ALL, 0)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(self.add_PAUSE_BUTTON, 0, wx.ALL, 0)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(self.add_MOVE_OLD_BUTTON, 0, wx.ALL, 0)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(self.add_MOVE_NEW_BUTTON, 0, wx.ALL, 0)

		###### SLIDER ######
		add_hbox3 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox3.AddSpacer((5,5))
		add_hbox3.Add(self.PLAYBACK_SLIDER, 1, wx.EXPAND, 0)


		###### CURRENT FILE ######
		add_hbox4 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox4.AddSpacer((5,5))
		add_hbox4.Add(add_current_file_STATICTEXT, 0, wx.ALL, 0)

		add_hbox5 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox5.AddSpacer((5,5))
		
		add_hbox5.Add(self.add_play_file_TEXTCTRL, 1, wx.EXPAND, 0)


		###### LAST FILES ######
		add_hbox6 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox6.AddSpacer((5,5))
		add_hbox6.Add(add_HISTORY_STATICTEXT, 0, wx.ALL, 0)

		add_hbox7 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox7.AddSpacer((5,5))
		add_hbox7.Add(self.add_HISTORY_TEXTCTRL, 1, wx.EXPAND, 1)



		vsizer = wx.BoxSizer(wx.VERTICAL)
		###### MUSIC SETTINGS ###### 
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox1, 0, wx.ALL, 0)
		###### BUTTONS ######
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox2, 0, wx.ALL, 0)
		###### SLIDER ######
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox3, 0, wx.EXPAND, 0)
		###### CURRENT FILE ######
		vsizer.Add(add_hbox4, 0, wx.ALL, 0)
		vsizer.AddSpacer((5,5))
		vsizer.Add(add_hbox5, 0, wx.EXPAND, 0)
		###### LAST FILES ######
		vsizer.Add(add_hbox6, 0, wx.ALL, 0)
		vsizer.AddSpacer((5,5))
		vsizer.AddStretchSpacer()
		vsizer.Add(add_hbox7, 100, wx.EXPAND, 0)

		self.SetSizer(vsizer)



		# keep current folder for OPEN BUTTON
		sp = wx.StandardPaths.Get()
		self.p3.p2.p1.settings['Directory_Open_Filebrowser']==sp.GetDocumentsDir()



		# Init mediaPlayer
		#self.mediaPlayer = wx.media.MediaCtrl(self, size=(0,0), szBackend=wx.media.MEDIABACKEND_MCI, style=0)
		#self.mediaPlayer = wx.media.MediaCtrl(self, size=(0,0), szBackend=wx.media.MEDIABACKEND_GSTREAMER, style=0)
		self.mediaPlayer = wx.media.MediaCtrl(self)
		self.Bind(wx.media.EVT_MEDIA_STOP, self.OnMediaStop, self.mediaPlayer)



		self.slider_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.onSliderTimer, self.slider_timer)

		if len (self.p3.p2.p1.playlist)>0:
			self.play_song()

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def init TabOne ends'





	def OnMediaStop(self, event):		
		if self.p3.p2.p1.settings['Debug']==1:

			if self.mediaPlayer.GetState()==0:
				print 'def OnMediaStop - GetState: 0 - init state'
			elif self.mediaPlayer.GetState()==1:
				print 'def OnMediaStop - GetState: 1 - pause -> continue play'
			elif self.mediaPlayer.GetState()==2:
				print 'def OnMediaStop - GetState: 2 - song end'
			else:
				print 'def OnMediaStop - GetState: %s' % self.mediaPlayer.GetState()



		if self.mediaPlayer.GetState()==2:

			self.p3.p2.p1.settings['Auto_mv_Old'] = self.add_AUTO_MV_OLD_CHECKBOX.GetValue()
			if self.p3.p2.p1.settings['Auto_mv_Old']==True:
				self.move_old()


			self.p3.p2.p1.settings['Loop'] = self.add_LOOP_CHECKBOX.GetValue()
			if self.p3.p2.p1.settings['Loop']==True:
				self.next_song()
				event.Veto()
			else:
				self.pause_stop()



	def onSeek(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def onSeek start'
		offset = self.PLAYBACK_SLIDER.GetValue()
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def onSeek offset: %s' % offset
		self.mediaPlayer.Seek(offset)

 

	def onSliderTimer(self, event):
		offset = self.mediaPlayer.Tell()
		self.PLAYBACK_SLIDER.SetValue(offset)


		
	def play_timer_stop(self):
		if hasattr(self, 't'):
			if self.p3.p2.p1.settings['Debug']==1:
				print 'def play_timer_stop - cancel'
			self.t.cancel()


	def play_timer_end(self):
		self.p3.p2.p1.settings['Auto_mv_Old'] = self.add_AUTO_MV_OLD_CHECKBOX.GetValue()

		if self.p3.p2.p1.settings['Play_Num'] in self.p3.p2.p1.playlist:
			self.add_HISTORY_TEXTCTRL.WriteText('%s - %s\n' % (self.p3.p2.p1.settings['Play_Num'],self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]))

		if self.p3.p2.p1.settings['Auto_mv_Old']==True:
			self.move_old()

		os.kill(self.p3.p2.p1.settings['Mainpid'], signal.SIGUSR2)


	def play_timer_start(self):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def play_timer_start - start with play_time: %s' % self.p3.p2.p1.settings['Play_Time']
		self.play_timer_stop()
		self.t = threading.Timer(int(self.p3.p2.p1.settings['Play_Time']), self.play_timer_end)
		self.t.start()



	def playlist_filescan(self):

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def playlist_filescan - start'


		allfiles = []

		if self.add_INCLUDE_NEW_CHECKBOX.GetValue()==True:

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def playlist_filescan - scan dir: %s' % self.p3.p2.p1.settings['Directory_New']

			for root, dirs, files in os.walk(self.p3.p2.p1.settings['Directory_New']):

				for item in files:

					if re.search('^%s' % self.p3.p2.p1.settings['Directory_Old'], root):
						pass
					elif re.search('^%s' % self.p3.p2.p1.settings['Directory_Streamripper'], root):
						pass
					else:
						allfiles.extend(['%s/%s' % (root,item)])



		if self.add_INCLUDE_OLD_CHECKBOX.GetValue()==True:

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def playlist_filescan - scan dir: %s' % self.p3.p2.p1.settings['Directory_Old']

			for root, dirs, files in os.walk(self.p3.p2.p1.settings['Directory_Old']):

				for item in files:

					if root==self.p3.p2.p1.settings['Directory_New']:
						pass
					elif root==self.p3.p2.p1.settings['Directory_Streamripper']:
						pass
					else:						
						allfiles.extend(['%s/%s' % (root,item)])




		if self.add_INCLUDE_STR_CHECKBOX.GetValue()==True:

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def playlist_filescan - scan dir: %s' % self.p3.p2.p1.settings['Directory_Streamripper']

			for root, dirs, files in os.walk(self.p3.p2.p1.settings['Directory_Streamripper']):
	
				for item in files:

					if root==self.p3.p2.p1.settings['Directory_Old']:
						pass
					elif root==self.p3.p2.p1.settings['Directory_New']:
						pass
					elif 'incomplete' in root:
						pass
					else:
						allfiles.extend(['%s/%s' % (root,item)])



		# reverse
		allfiles=allfiles[::-1]

		# reset
		self.p3.p2.p1.playlist = {}

		i=0
		for item in allfiles:
			i+=1
			p = {i:item}
			self.p3.p2.p1.playlist.update(p)

		self.p3.p2.p1.settings['Play_Num'] = 1

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def playlist_filescan - len(allfiles): %s' % len(allfiles)




	def back_song(self):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def back_song - start'

		self.p3.p2.p1.settings['Play_Num']-=1

		if not self.p3.p2.p1.playlist.has_key(self.p3.p2.p1.settings['Play_Num']):
			self.playlist_filescan()

		if self.p3.p2.p1.playlist.has_key(self.p3.p2.p1.settings['Play_Num']):
			if self.p3.p2.p1.settings['Debug']==1:
				print 'def back_song - play_num: %s' % self.p3.p2.p1.settings['Play_Num']

			self.load_playlist()
			self.play_song()




	def next_song(self):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def next_song - start len playlist %s' % len(self.p3.p2.p1.playlist)

		self.add_FILES_SUM_TEXTCTRL.Clear()

		if len(self.p3.p2.p1.playlist)>0:

			if self.p3.p2.p1.settings['Play']=='database':

				if self.p3.p2.p1.settings['Play_Num'] in self.p3.p2.p1.playlist:
					self.add_HISTORY_TEXTCTRL.WriteText('%s - %s\n' % (self.p3.p2.p1.settings['Play_Num'],self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]))

				self.p3.p2.p1.settings['Play_Num']+=1

				if not self.p3.p2.p1.playlist.has_key(self.p3.p2.p1.settings['Play_Num']):
					if self.p3.p2.p1.settings['Debug']==1:
						print 'def next_song - restart playlist'
					self.playlist_filescan()



			if self.p3.p2.p1.playlist.has_key(self.p3.p2.p1.settings['Play_Num']):
				if self.p3.p2.p1.settings['Debug']==1:
					print 'def next_song - play_num: %s' % self.p3.p2.p1.settings['Play_Num']

				self.play_song()




	def load_playlist(self):
		if self.p3.p2.p1.settings['Debug']==1:
			if len(self.p3.p2.p1.playlist)>0:
				print 'def load_playlist start play_num: %s' % str(os.path.join(self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]))
			else:
				print 'def load_playlist no files in playlist'


		if self.p3.p2.p1.settings['Play']=='database':
			self.add_FILES_SUM_TEXTCTRL.Clear()
			self.add_FILES_SUM_TEXTCTRL.WriteText(str(len(self.p3.p2.p1.playlist)))
		elif self.p3.p2.p1.settings['Play']=='file':
			self.add_FILES_SUM_TEXTCTRL.Clear()


		if len(self.p3.p2.p1.playlist)>0:

			self.add_play_file_TEXTCTRL.Clear()

			# Problem: Media playback error: No valid frames decoded before end of stream
			# try without affect
			self.mediaPlayer.Load(unicode(os.path.join(self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]).decode('utf8')))

			self.mediaPlayer.SetInitialSize()


			time.sleep(0.05)
			self.PLAYBACK_SLIDER.SetRange(0, self.mediaPlayer.Length())
			self.add_play_file_TEXTCTRL.WriteText('%s - %s' % (self.p3.p2.p1.settings['Play_Num'],self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]))




	def play_song(self):
		if self.p3.p2.p1.settings['Debug']==1:
			if len(self.p3.p2.p1.playlist)>0:
				print 'def play_song start play_num: %s' % unicode(os.path.join(self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]).decode('utf8'))
			else:
				print 'def play_song no files in playlist'


		self.slider_timer.Start(200)

		if self.p3.p2.p1.settings['Play']=='file':

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def play_song -> file'

			self.p3.p2.p1.settings['Play_Time']='0'
			self.play_timer_stop()

			self.add_HISTORY_TEXTCTRL.Clear()

			self.add_PLAY_TIME_COMBOBOX.Disable()
			self.add_FILES_SUM_TEXTCTRL.Disable()
			self.add_AUTO_MV_OLD_CHECKBOX.Disable()
			self.add_HISTORY_TEXTCTRL.Disable()

			self.add_NEXT_BUTTON.Disable()
			self.add_BACK_BUTTON.Disable()


		if self.p3.p2.p1.settings['Play']=='database':

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def play_song -> database'

			self.add_PLAY_TIME_COMBOBOX.Enable()
			self.add_FILES_SUM_TEXTCTRL.Enable()
			self.add_AUTO_MV_OLD_CHECKBOX.Enable()
			self.add_HISTORY_TEXTCTRL.Enable()


			if int(self.p3.p2.p1.settings['Play_Time'])>0:
				self.play_timer_start()
			else:
				self.play_timer_stop()

			self.add_NEXT_BUTTON.Enable()
			self.add_BACK_BUTTON.Enable()


		self.add_PAUSE_BUTTON.Enable()
		self.add_PLAY_BUTTON.Disable()
		self.add_MOVE_OLD_BUTTON.Enable()
		self.add_MOVE_NEW_BUTTON.Enable()


		if self.mediaPlayer.GetState()==0:
			if self.p3.p2.p1.settings['Debug']==1:
				print 'def play_song - GetState: 0 - init state -> try to load_playlist'
			self.load_playlist()

		elif self.mediaPlayer.GetState()==2:
			if self.p3.p2.p1.settings['Debug']==1:
				print 'def play_song - GetState: 2 - song end -> try to load_playlist'
			self.load_playlist()


		if self.p3.p2.p1.settings['Debug']==1:
			print 'def play_song - PLAY'
		self.mediaPlayer.Play()


		if self.p3.p2.p1.settings['Random_Time']!='0':

			(random_t1,random_t2) = self.p3.p2.p1.settings['Random_Time'].split('-')

			if self.p3.p2.p1.settings['Debug']==1:
				print 'def play_song random_t1: %s random_t1: %s' % (random_t1,random_t2)

			start_time_s=random.randint(int(random_t1),int(random_t2))
			start_time_ms=start_time_s*1000
			if self.p3.p2.p1.settings['Debug']==1:
				print 'def play_song - start-time: %s ms' % start_time_ms
			self.mediaPlayer.Seek(start_time_ms)




	def pause_stop(self):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def pause_stop start'

		self.slider_timer.Stop()
		self.play_timer_stop()
		self.mediaPlayer.Pause()




	def move_old(self):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def move_old - start'

		if self.p3.p2.p1.settings['Play_Num'] in self.p3.p2.p1.playlist:

			filename = os.path.basename(self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']])
			try:
				if (os.path.exists(self.p3.p2.p1.settings['Directory_Old']))==False:
					os.mkdir(self.p3.p2.p1.settings['Directory_Old'])
				os.rename(self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']],'%s/%s' % (self.p3.p2.p1.settings['Directory_Old'],filename))
				del self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]
			except Exception as e:
				if self.p3.p2.p1.settings['Debug']==1:
					print 'def move_old error: %s' % str(e)




	def move_new(self):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def move_new - start'

		if self.p3.p2.p1.settings['Play_Num'] in self.p3.p2.p1.playlist:

			filename = os.path.basename(self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']])
			try:
				if (os.path.exists(self.p3.p2.p1.settings['Directory_New']))==False:
					os.mkdir(self.p3.p2.p1.settings['Directory_New'])
				os.rename(self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']],'%s/%s' % (self.p3.p2.p1.settings['Directory_New'],filename))
				del self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]
			except Exception as e:
				if self.p3.p2.p1.settings['Debug']==1:
					print 'def move_new error: %s' % str(e)




	def PLAY_TIME_COMBOBOX(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def PLAY_TIME_COMBOBOX - start - choose: %s' % event.GetString()
		self.p3.p2.p1.settings['Play_Time'] = event.GetString()

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def PLAY_TIME_COMBOBOX - GetState: %s (2==Loop)' % self.mediaPlayer.GetState()

		if self.mediaPlayer.GetState()==2:
			self.play_timer_start()



	def RANDOM_COMBOBOX(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def RANDOM_COMBOBOX - start - choose: %s' % event.GetString()

		self.p3.p2.p1.settings['Random_Time'] = event.GetString()



	###### BUTTONS ######
	def SCAN_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def SCAN_BUTTON - start'

		self.add_HISTORY_TEXTCTRL.Clear()
		self.pause_stop()
		self.playlist_filescan()


		if len(self.p3.p2.p1.playlist)>=1:
			self.p3.p2.p1.settings['Play']='database'
			self.add_AUTO_MV_OLD_CHECKBOX.Enable()
			self.add_PLAY_TIME_COMBOBOX.Enable()
			self.add_PLAY_BUTTON.Enable()

		self.load_playlist()


	def OPEN_BUTTON(self, event):
		wildcard = 'MP3 (*.mp3)|*.mp3|WAV (*.wav)|*.wav|FLAC (*.flac)|*.flac'

		dlg = wx.FileDialog(self, message='Choose a file',defaultDir=str(self.p3.p2.p1.settings['Directory_Open_Filebrowser']), defaultFile='', wildcard=wildcard, style=wx.OPEN|wx.CHANGE_DIR)

		if dlg.ShowModal()==wx.ID_OK:
			self.p3.p2.p1.settings['Play_Num'] = 1
			self.p3.p2.p1.settings['song'] = 'file'
			self.p3.p2.p1.playlist = {self.p3.p2.p1.settings['Play_Num']:dlg.GetPath()}

			# keep current folder maybe for next open file
			self.p3.p2.p1.settings['Directory_Open_Filebrowser'] = os.path.dirname(dlg.GetPath())
			self.play_song()

		dlg.Destroy()



	def PLAY_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def PLAY_BUTTON - start'
		self.play_song()



	def NEXT_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def NEXT_BUTTON - start'
		self.next_song()



	def BACK_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def BACK_BUTTON - start'
		self.back_song()



	def PAUSE_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def PAUSE_BUTTON - start'
		self.pause_stop()

		self.add_PAUSE_BUTTON.Disable()
		self.add_PLAY_BUTTON.Enable()
		self.add_BACK_BUTTON.Disable()
		self.add_NEXT_BUTTON.Disable()



	def MOVE_OLD_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def MOVE_OLD_BUTTON start'
		if self.p3.p2.p1.settings['Play_Num'] in self.p3.p2.p1.playlist:
			self.add_HISTORY_TEXTCTRL.WriteText('%s - %s\n' % (self.p3.p2.p1.settings['Play_Num'],self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]))
		self.move_old()
		self.next_song()



	def MOVE_NEW_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def MOVE_NEW_BUTTON start'
		if self.p3.p2.p1.settings['Play_Num'] in self.p3.p2.p1.playlist:
			self.add_HISTORY_TEXTCTRL.WriteText('%s - %s\n' % (self.p3.p2.p1.settings['Play_Num'],self.p3.p2.p1.playlist[self.p3.p2.p1.settings['Play_Num']]))
		self.move_new()
		self.next_song()

