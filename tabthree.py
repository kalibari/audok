#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import os


class TabThree(wx.Panel):

	def __init__(self, p3):

		wx.Panel.__init__(self, parent=p3, id=wx.ID_ANY)

		self.p3 = p3


		newid = wx.NewId()
		self.panel1 = wx.Panel(self, id=newid, size=(self.p3.p2.p1.settings['Size_X']-30,self.p3.p2.p1.settings['Size_Y']))

		newid = wx.NewId()
		self.panel2 = wx.Panel(self, id=newid, size=(self.p3.p2.p1.settings['Size_X']-30,30))


		newid = wx.NewId()
		self.scroll = wx.ScrolledWindow(self.panel1, style=wx.VSCROLL)


		fgs = wx.FlexGridSizer(rows=len(self.p3.p2.p1.stationlist), cols=4, vgap=1, hgap=1)


		self.checkbox = []
		self.genre_file_TEXTCTRL = []
		self.name_file_TEXTCTRL = []
		self.url_file_TEXTCTRL = []


		i=0
		for item in self.p3.p2.p1.stationlist:

			newid = wx.NewId()
			add_checkbox = wx.CheckBox(self.scroll, newid , '', pos=(0, 0), size=(24, 24))
			self.Bind(wx.EVT_TEXT, None, id=newid)
			add_checkbox.SetValue(0)
			self.checkbox.extend([add_checkbox])

			newid = wx.NewId()
			add_genre_file_TEXTCTRL = wx.TextCtrl(self.scroll, newid, '%s' % item[0], size=(110, 24))
			self.Bind(wx.EVT_TEXT, None, id=newid)
			self.genre_file_TEXTCTRL.extend([add_genre_file_TEXTCTRL])

			newid = wx.NewId()
			add_name_file_TEXTCTRL = wx.TextCtrl(self.scroll, newid, '%s' % item[1], size=(300, 24))
			self.Bind(wx.EVT_TEXT, None, id=newid)
			self.name_file_TEXTCTRL.extend([add_name_file_TEXTCTRL])


			newid = wx.NewId()
			add_url_file_TEXTCTRL = wx.TextCtrl(self.scroll, newid, '' , size=(1400, 24))
			self.Bind(wx.EVT_TEXT, None, id=newid)
			self.url_file_TEXTCTRL.extend([add_url_file_TEXTCTRL])

			fgs.AddMany([add_checkbox, add_genre_file_TEXTCTRL, add_name_file_TEXTCTRL, (add_url_file_TEXTCTRL, 1, wx.ALL)])



		fgs.AddGrowableCol(2, 1)

		newid = wx.NewId()
		self.add_SELECT_ALL_BUTTON = wx.Button(self.panel2, id=newid, label='Select All', size=(110, 30))
		self.Bind(wx.EVT_BUTTON, self.SELECT_ALL_BUTTON, id=newid)


		newid = wx.NewId()
		self.add_DESELECT_ALL_BUTTON = wx.Button(self.panel2, id=newid, label='Deselect All', size=(110, 30))
		self.Bind(wx.EVT_BUTTON, self.DESELECT_ALL_BUTTON, id=newid)


		newid = wx.NewId()
		self.add_START_RECORD_BUTTON = wx.Button(self.panel2, id=newid, label='Record', size=(110, 30))
		self.Bind(wx.EVT_BUTTON, self.START_RECORD_BUTTON, id=newid)


		newid = wx.NewId()
		self.add_STOP_RECORD_BUTTON = wx.Button(self.panel2, id=newid, label='Stop', size=(110, 30))
		self.Bind(wx.EVT_BUTTON, self.STOP_RECORD_BUTTON, id=newid)
		self.add_STOP_RECORD_BUTTON.Disable()


		newid = wx.NewId()
		self.add_EDIT_BUTTON = wx.Button(self.panel2, id=newid, label='Edit', size=(110, 30))
		self.Bind(wx.EVT_BUTTON, self.EDIT_BUTTON, id=newid)


		newid = wx.NewId()
		self.add_SAVE_BUTTON = wx.Button(self.panel2, id=newid, label='Save', size=(110, 30))
		self.Bind(wx.EVT_BUTTON, self.SAVE_BUTTON, id=newid)
		self.add_SAVE_BUTTON.Disable()


		newid = wx.NewId()
		self.add_RESET_BUTTON = wx.Button(self.panel2, id=newid, label='Reset', size=(110, 30))
		self.Bind(wx.EVT_BUTTON, self.RESET_BUTTON, id=newid)


		newid = wx.NewId()
		self.add_INFO_BUTTON = wx.Button(self.panel2, id=newid, label='Info', size=(110, 30))
		self.Bind(wx.EVT_BUTTON, self.INFO_BUTTON, id=newid)


		add_hbox1 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox1.Add(fgs, proportion = 1, flag = wx.ALL , border = 4)
		self.panel1.SetSizer(add_hbox1)


		add_hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		add_hbox2.AddSpacer((5,5))
		add_hbox2.Add(self.add_SELECT_ALL_BUTTON, 0, wx.ALL, 0)
		add_hbox2.Add(self.add_DESELECT_ALL_BUTTON, 0, wx.ALL, 0)
		add_hbox2.Add(self.add_START_RECORD_BUTTON, 0, wx.ALL, 0)
		add_hbox2.Add(self.add_STOP_RECORD_BUTTON, 0, wx.ALL, 0)
		add_hbox2.AddSpacer((60,5))

		add_hbox2.Add(self.add_EDIT_BUTTON, 0, wx.ALL, 0)
		add_hbox2.Add(self.add_SAVE_BUTTON, 0, wx.ALL, 0)
		add_hbox2.Add(self.add_RESET_BUTTON, 0, wx.ALL, 0)
		add_hbox2.Add(self.add_INFO_BUTTON, 0, wx.ALL, 0)

		
		self.panel2.SetSizer(add_hbox2)


		vsizer = wx.BoxSizer(wx.VERTICAL)
		vsizer.Add(self.panel1, -50, wx.EXPAND, 0)
		vsizer.AddStretchSpacer()
		vsizer.Add(self.panel2, 0, wx.ALL, 0)
		self.SetSizer(vsizer)


		#self.SetAutoLayout(1)
		#self.Fit()

		if self.p3.p2.p1.settings['Debug']==1:
			print 'def init TabThree ends'





	def SELECT_ALL_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def SELECT_ALL_BUTTON start'

		for item in self.checkbox:
			erg = item.SetValue(1)



	def DESELECT_ALL_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def DESELECT_ALL_BUTTON start'

		for item in self.checkbox:
			erg = item.SetValue(0)



	def EDIT_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def EDIT_BUTTON start'

		self.add_EDIT_BUTTON.Disable()

		for item in self.genre_file_TEXTCTRL:
			item.SetEditable(True)

		for item in self.name_file_TEXTCTRL:
			item.SetEditable(True)

		i=0
		for item in self.url_file_TEXTCTRL:
			item.SetEditable(True)
			item.Clear()
			item.AppendText('%s' % self.p3.p2.p1.stationlist[i][2])
			i+=1

		self.add_SAVE_BUTTON.Enable()



	def SAVE_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def SAVE_BUTTON start'


		self.add_SAVE_BUTTON.Disable()

		i=0
		for item in self.genre_file_TEXTCTRL:
			item.SetEditable(False)
			self.p3.p2.p1.stationlist[i][0] = str(item.GetValue())
			i+=1

		i=0
		for item in self.name_file_TEXTCTRL:
			item.SetEditable(False)
			self.p3.p2.p1.stationlist[i][1] = str(item.GetValue())
			i+=1


		i=0
		for item in self.url_file_TEXTCTRL:
			item.SetEditable(False)
			self.p3.p2.p1.stationlist[i][2] = str(item.GetValue().strip())
			item.Clear()
			i+=1

		self.add_EDIT_BUTTON.Enable()


		# Save new Stations
		if not os.path.exists('%s/.config/%s' % (os.environ['HOME'], self.p3.p2.p1.settings['Name'])):
			os.mkdir('%s/.config/%s' % (os.environ['HOME'], self.p3.p2.p1.settings['Name']), 0755 );
		f = open('%s/.config/%s/stations.xml' % (os.environ['HOME'], self.p3.p2.p1.settings['Name']), 'w')
		f.write('<?xml version="1.0"?>\n')
		f.write('<data>\n')
		for item1,item2,item3 in self.p3.p2.p1.stationlist:
			f.write('\t<station>\n' + '\t\t<name>' + str(item1) + '</name>\n'  + '\t\t<genre>' + str(item2) + '</genre>\n'  + '\t\t<url>' + str(item3) +  '</url>\n' +  '\t</station>\n')
		f.write('</data>\n')

		f.close()




	def RESET_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def RESET_BUTTON - start'

		self.p3.p2.OnClose(None)

		if os.path.exists('%s/.config/audok/stations.xml' % os.environ['HOME']):
			os.remove('%s/.config/audok/stations.xml' % os.environ['HOME'])
	



	class Info_Dialog(wx.Dialog):
		def __init__(self):
			wx.Dialog.__init__(self, None, -1, 'Info', size=(450, 150))

			newid = wx.NewId()
			add_link_HyperlinkCtrl = wx.HyperlinkCtrl(self, id=newid, label='Get new stations at: http://www.shoutcast.com', url='http://www.shoutcast.com', pos=(10, 10), size=(400, 30), style=wx.HL_ALIGN_CENTRE|wx.HL_DEFAULT_STYLE)



	def INFO_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def INFO_BUTTON - start'

		dlg = self.Info_Dialog()
		dlg.ShowModal()
		dlg.Destroy()



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

					if self.p3.process_database[item]['job']=='streamripper':

						identifier = int(self.p3.process_database[item]['identifier'])

						if self.p3.process_database[item]['output']:
							self.url_file_TEXTCTRL[identifier].Clear()
							self.url_file_TEXTCTRL[identifier].WriteText('%s' % self.p3.process_database[item]['output'][-1])
							self.p3.process_database[item]['output']=[]


				##############
				### result ###
				##############
				if self.p3.process_database[item]['todo']=='result':

					if self.p3.process_database[item]['job']=='streamripper':

						self.p3.process_database[item]['status']='inactive'

						identifier = int(self.p3.process_database[item]['identifier'])

						self.checkbox[identifier].Enable()


		if len(self.p3.process_database)==inactive_processes:
			self.refresh_timer.Stop()





	def START_RECORD_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def START_RECORD_BUTTON start'

		self.add_STOP_RECORD_BUTTON.Enable()
		self.add_EDIT_BUTTON.Disable()
		self.add_RESET_BUTTON.Disable()


		self.refresh_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.refresh_output_textctrl_timer, self.refresh_timer)
		self.refresh_timer.Start(1000)

		if (os.path.exists(self.p3.p2.p1.settings['Directory_Streamripper']))==False:
			os.mkdir(self.p3.p2.p1.settings['Directory_Streamripper'])


		checkbox_enabled=0
		identifier=0

		for item in self.checkbox:
			erg = item.GetValue()
			if erg==True:
				checkbox_enabled+=1
				if item.IsEnabled():
					if self.p3.p2.p1.settings['Debug']==1:
						print 'def START_RECORD_BUTTON identifier: %s file: %s' % (identifier,self.p3.p2.p1.stationlist[identifier])

					# streamripper http://www.top100station.de/switch/r3472.pls -u WinampMPEG/5.0 -d /MyDisc/Audio/Neu/Streamtuner/

					cmd=['streamripper','%s' % self.p3.p2.p1.stationlist[identifier][2],'-u','WinampMPEG/5.0','-d','%s' % self.p3.p2.p1.settings['Directory_Streamripper']]
					cwd=self.p3.p2.p1.settings['Directory_Streamripper']
					self.p3.process_starter(cmd=cmd, cwd=cwd, job='streamripper', identifier=str(identifier), source=self.p3.p2.p1.stationlist[identifier][2])
					item.Disable()
					
			identifier+=1

		if checkbox_enabled==0:
			self.add_STOP_RECORD_BUTTON.Disable()
			self.add_EDIT_BUTTON.Enable()
			self.add_RESET_BUTTON.Enable()




	def STOP_RECORD_BUTTON(self, event):
		if self.p3.p2.p1.settings['Debug']==1:
			print 'def STOP_RECORD_BUTTON start'

		self.refresh_timer.Stop()

		self.add_START_RECORD_BUTTON.Enable()
		self.add_STOP_RECORD_BUTTON.Disable()

		self.add_EDIT_BUTTON.Enable()
		self.add_SAVE_BUTTON.Enable()
		self.add_RESET_BUTTON.Enable()



		for item in self.checkbox:
			item.Enable()

		self.p3.process_job_killer(job='streamripper')

