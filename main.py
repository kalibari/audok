#!/usr/bin/python
# -*- coding: utf-8 -*-

import wx
import os
import re
import threading
import signal
import socket
import subprocess
import tabone
import tabtwo
import tabthree
import tabfour

class Music_Admin_GUI(wx.Notebook):

	def __init__(self, p2, panel):

		wx.Notebook.__init__(self, panel, id=wx.ID_ANY, style=wx.BK_DEFAULT)


		self.p2 = p2

		signal.signal(signal.SIGUSR1, self.signal_handler_sigusr1)
		signal.signal(signal.SIGUSR2, self.signal_handler_sigusr2)

		self.pnum = 0

		self.process_database = {}
		# self.process_database[item]['status'] -> active, inactive, killed  necessary for refresh_output_textctrl_timer
		# self.process_database[item]['todo']   -> show, nooutput, result
		# self.process_database[item]['result'] -> True, False


		self.tab_one = tabone.TabOne(self)
		self.AddPage(self.tab_one, 'Audio Player')

		self.tab_two = tabtwo.TabTwo(self)
		self.AddPage(self.tab_two, 'Converter')

		self.tab_three = tabthree.TabThree(self)
		self.AddPage(self.tab_three , 'Streamripper')

		self.tab_four = tabfour.TabFour(self)
		self.AddPage(self.tab_four, 'Settings')




		if self.p2.p1.settings['Debug']==1:
			print 'def init - Main add signal handlers'


		try:
			thread = threading.Thread(target=self.ipc_server)
			thread.setDaemon(True)
			thread.start()
		except Exception as e:
			if self.p2.p1.settings['Debug']==1:
				print 'def init - PanelOne ipc_server error: %s' % str(e)


		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
		self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
		self.Bind(wx.EVT_SIZE, self.ReSize)



	def ReSize(self, event):
		size = event.GetSize()
		self.p2.p1.settings['Size_X']=size.width
		self.p2.p1.settings['Size_Y']=(size.height + 37)

		# resize scroll window
		self.tab_three.scroll.SetSize((self.p2.p1.settings['Size_X']-20, self.p2.p1.settings['Size_Y']-50))
		self.tab_three.scroll.SetScrollbars(noUnitsX=0, noUnitsY=5, pixelsPerUnitX=0, pixelsPerUnitY=100)
		self.tab_three.Refresh()

		


	def OnPageChanged(self, event):
		old = event.GetOldSelection()
		new = event.GetSelection()
		self.active_panel = self.GetSelection()
		event.Skip()
		if self.p2.p1.settings['Debug']==1:
			print 'OnPageChanged - self.active_panel: %d' % self.active_panel



	def OnPageChanging(self, event):
		event.GetOldSelection()
		event.GetSelection()
		self.GetSelection()
		event.Skip()



	def signal_handler_sigusr1(self, signal, frame):
		if self.p2.p1.settings['Debug']==1:
			print 'def signal_handler_sigusr1 start'

		self.p2.p1.settings['Play']='file'
		
		self.tab_one.play_song()



	def signal_handler_sigusr2(self, signal, frame):
		
		if self.p2.p1.settings['Debug']==1:
			print 'def signal_handler_sigusr2 start'
		self.p2.p1.settings['Play']='database'

		self.tab_one.next_song()




	def process_all_killer(self):
	
		if self.p2.p1.settings['Debug']==1:
			print 'def process_all_killer - start'

		for item in self.process_database:
			if self.process_database[item]['status']=='active':
				try:
					os.kill(int(self.process_database[item]['pid']), signal.SIGINT)
				except:
					pass




	def process_job_killer(self, job):

		if self.p2.p1.settings['Debug']==1:
			print 'def process_job_killer - start'

		for item in self.process_database:
			if self.process_database[item]['status']=='active':
				if self.process_database[item]['job']==job:
					try:
						os.kill(int(self.process_database[item]['pid']), signal.SIGINT)
						self.process_database[item]['status']='killed'
					except:
						pass

					if self.p2.p1.settings['Debug']==1:
						if self.process_database[item]['status']=='killed':
							print 'def process_job_killer - job: %s killed pid: %s' % (self.process_database[item]['job'],self.process_database[item]['pid'])
						else:
							print 'def process_job_killer - job: %s cannot kill pid: %s' % (self.process_database[item]['job'],self.process_database[item]['pid'])




	def process_starter(self, cmd=[], cwd='', job='', identifier='', source=''):

		self.pnum+=1
		k = {self.pnum: {	'status': 'active',
								'job': job,
								'todo': '',
								'source': source,
								'identifier': identifier,
								'output': []}}

		self.process_database.update(k)


		if self.p2.p1.settings['Debug']==1:
			print 'def process_starter start'

		try:
			thread = threading.Thread(target=self.process, args=(cmd, cwd, self.pnum, self.process_database))
			thread.setDaemon(True)
			thread.start()
		except Exception as e:
			if self.p2.p1.settings['Debug']==1:
				print 'def process_starter error: %s' % str(e)



	def process(self, cmd=[], cwd='', pnum='', process_database={}):

		if self.p2.p1.settings['Debug']==1:
			print 'def process start cmd: %s cwd: %s' % (cmd,cwd)


		output_list=[]
		output_str=''
		process_pid=''
		i=0

		try:			
			process = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False, close_fds=True)

			# add PID
			if self.p2.p1.settings['Debug']==1:
				print 'def process: add pid %s' % process.pid
			process_database[pnum]['pid']=process.pid


			while True:

				line = process.stdout.readline(20)
				output_str=output_str+str(line)

				out = output_str.split('\n')
				if len(out)<2:
					out = output_str.split('\r')

				if len(out)>=2:
					output_list.extend(out[:-1])
					for item in out[:-1]:
						process_database[pnum]['todo']='show'
						process_database[pnum]['output'].extend([item])

					output_str=out[-1]

				if not line:
					if process_database[pnum]['todo']!='nooutput':
						process_database[pnum]['todo']='nooutput'

						if self.p2.p1.settings['Debug']==1:
							print 'def process - break'
						break


			wait_erg=process.wait()
			if wait_erg==0:
				process_database[pnum]['result']=True
			else:
				process_database[pnum]['result']=False


		except Exception as e:
			if self.p2.p1.settings['Debug']==1:
				print 'def process error: %s job: %s' % (str(e),process_database[pnum]['job'])


		if self.p2.p1.settings['Debug']==1:
			print 'def process job %s done' % process_database[pnum]['job']
		process_database[pnum]['todo']='result'






	def ipc_server(self):
		if self.p2.p1.settings['Debug']==1:
			print 'def ipc_server - thread start'

		for num in range(0,10):

			self.p2.p1.settings['Ipc_Port'] = self.p2.p1.settings['Ipc_Port'] + num

			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.bind(('localhost', self.p2.p1.settings['Ipc_Port']))
				sock.listen(1)
				#sock.setblocking(0)
				#sock.settimeout(10)
				break
			except:
				if self.p2.p1.settings['Debug']==1:
					print 'def ipc_server - thread port is probably blocked -> try next port'


		if self.p2.p1.settings['Debug']==1:
			print 'def ipc_server - thread listen on port: %s' % self.p2.p1.settings['Ipc_Port']



		while True:

			os.kill(self.p2.p1.settings['Mainpid'], signal.SIGUSR1)

			connection, client_address = sock.accept()

			try:
				while True:
					data = connection.recv(130)
					if data:
						if self.p2.p1.settings['Debug']==1:
							print 'def ipc_server - thread received "%s"' % data
						self.p2.p1.settings['Play_Num'] = 1
						self.p2.p1.playlist = {self.p2.p1.settings['Play_Num']:data}
					else:
						if self.p2.p1.settings['Debug']==1:
							print 'def ipc_server - thread send SIGUSR1 to pid: %s type: %s' % (self.p2.p1.settings['Mainpid'],type(self.p2.p1.settings['Mainpid']))
						# play one song
						break

				if self.p2.p1.settings['Debug']==1:
					print 'def ipc_server - thread wait...'

			finally:
				connection.close()



class Music_Admin_Frame(wx.Frame):

	def __init__(self, p1):
		self.p1 = p1

		wx.Frame.__init__(self, None, wx.ID_ANY, self.p1.settings['Name'].title())

		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_MOVE, self.OnMove)

		panel = wx.Panel(self)
		self.admin_gui = Music_Admin_GUI(self, panel)

		sizer = wx.BoxSizer(wx.VERTICAL)

		sizer.Add(self.admin_gui, 1, wx.EXPAND, 5)

		panel.SetSizer(sizer)
		self.Layout()
		self.Show()


	def OnMove(self, event):
		self.p1.settings['Position_X'], self.p1.settings['Position_Y'] = event.GetPosition()



	def OnClose(self, event):

		if self.p1.settings['Debug']==1:
			print 'def OnClose - start'

		self.admin_gui.tab_one.mediaPlayer.Stop()
		self.admin_gui.tab_one.mediaPlayer.Close()

		self.admin_gui.tab_one.play_timer_stop()
		self.admin_gui.tab_one.slider_timer.Stop()

		if hasattr(self.admin_gui.tab_two, 'refresh_timer'):
			self.admin_gui.tab_two.refresh_timer.Stop()
		if hasattr(self.admin_gui.tab_three, 'refresh_timer'):
			self.admin_gui.tab_three.refresh_timer.Stop()
		if hasattr(self.admin_gui.tab_four, 'refresh_timer'):
			self.admin_gui.tab_four.refresh_timer.Stop()


		self.admin_gui.process_all_killer()


		# Save new Size / Position
		if not os.path.exists('%s/.config/%s' % (os.environ['HOME'], self.p1.settings['Name'])):
			os.mkdir('%s/.config/%s' % (os.environ['HOME'], self.p1.settings['Name']), 0755 );
		f = open('%s/.config/%s/settings.xml' % (os.environ['HOME'], self.p1.settings['Name']), 'w')
		f.write('<?xml version="1.0"?>\n')
		f.write('<data>\n')
		for item1 in self.p1.settings:
			f.write('\t<' + str(item1) + '>' + str(self.p1.settings[item1]) + '</' + str(item1) + '>\n')
		f.write('</data>\n')
		f.close()


		if self.p1.settings['Debug']==1:
			print 'def OnClose - try to destroy'

		self.Destroy()



class Music_Admin_Start():

	def __init__(self, settings, playlist, stationlist):
		self.settings = settings
		self.playlist = playlist
		self.stationlist = stationlist


	def start(self):

		self.app = wx.App()
		self.frame = Music_Admin_Frame(self)

		self.frame.SetIcon(wx.Icon('%s/audok.ico' % self.settings['Path'] , wx.BITMAP_TYPE_ICO))
		self.frame.Show(True)
		self.frame.SetDimensions(self.settings['Position_X'],self.settings['Position_Y'],self.settings['Size_X'],self.settings['Size_Y'])


		self.app.MainLoop()


