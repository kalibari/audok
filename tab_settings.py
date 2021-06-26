import os
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk, GObject


class TabSettings:

   def __init__(self, main, settings):
      self.main = main
      self.settings = settings

      self.box = Gtk.Box()
      self.box.set_border_width(10)

      grid = Gtk.Grid()
      grid.set_column_homogeneous(True)
      grid.set_row_homogeneous(True)

      #############################

      hbox_directories_ad = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_directories_ad = Gtk.Label("Audio Player Directories:", xalign=0)

      hbox_directories_ad.pack_start(label_directories_ad, False, False, 0)

      grid.add(hbox_directories_ad)

      #############################

      hbox_dir_new= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox_dir_new.set_hexpand(True)


      image1 = Gtk.Image()
      image1.set_from_file('%s/newdir_small.png' % self.settings['Path'])
      label1 = Gtk.Label("New:", xalign=0)
      label1.set_size_request(150, -1)


      self.entry_input_dir_new = Gtk.Entry()
      self.entry_input_dir_new.set_size_request(-1, 10)
      self.entry_input_dir_new.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      self.entry_input_dir_new.set_text(self.settings['Directory_New'])



      hbox_dir_new.pack_start(image1, False, False, 0)
      hbox_dir_new.pack_start(label1, False, True, 0)
      hbox_dir_new.pack_start(self.entry_input_dir_new, True, True, 0)


      grid.attach_next_to(hbox_dir_new, hbox_directories_ad, Gtk.PositionType.BOTTOM, 1, 1)

      #############################


      hbox_dir_old= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      hbox_dir_old.set_hexpand(True)

      image2 = Gtk.Image()
      image2.set_from_file('%s/olddir_small.png' % self.settings['Path'])
      label2 = Gtk.Label("Old:", xalign=0)
      label2.set_size_request(150, -1)


      self.entry_input_dir_old = Gtk.Entry()
      self.entry_input_dir_old.set_size_request(-1, 10)
      self.entry_input_dir_old.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      self.entry_input_dir_old.set_text(self.settings['Directory_Old'])


      hbox_dir_old.pack_start(image2, False, False, 0)
      hbox_dir_old.pack_start(label2, False, True, 0)
      hbox_dir_old.pack_start(self.entry_input_dir_old, True, True, 0)

      grid.attach_next_to(hbox_dir_old, hbox_dir_new, Gtk.PositionType.BOTTOM, 1, 1)


      #############################


      hbox_directory_st = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_directory_st = Gtk.Label("Streamripper Directory:", xalign=0)

      hbox_directory_st.pack_start(label_directory_st, False, False, 0)

      grid.attach_next_to(hbox_directory_st, hbox_dir_old, Gtk.PositionType.BOTTOM, 1, 1)


      #############################

      hbox_dir_st= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      image3 = Gtk.Image()
      image3.set_from_file('%s/streamripperdir_small.png' % self.settings['Path'])
      label3 = Gtk.Label("Streamripper:", xalign=0)
      label3.set_size_request(150, -1)

      self.entry_input_dir_st = Gtk.Entry()
      self.entry_input_dir_st.set_size_request(-1, 10)
      self.entry_input_dir_st.override_background_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0, 1, 1, 46590))
      self.entry_input_dir_st.set_text(self.settings['Directory_Streamripper'])


      hbox_dir_st.pack_start(image3, False, False, 0)
      hbox_dir_st.pack_start(label3, False, True, 0)
      hbox_dir_st.pack_start(self.entry_input_dir_st, True, True, 0)

      grid.attach_next_to(hbox_dir_st, hbox_directory_st, Gtk.PositionType.BOTTOM, 1, 1)


      #############################

      hbox_coverter = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_coverter = Gtk.Label("Converter:", xalign=0)

      hbox_coverter.pack_start(label_coverter, False, False, 0)

      grid.attach_next_to(hbox_coverter, hbox_dir_st, Gtk.PositionType.BOTTOM, 1, 1)


      #############################


      hbox_file2mp3= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_file2mp3 = Gtk.Label("file2mp3 bitrate:", xalign=0)
      label_file2mp3.set_size_request(195, -1)


      combo_file2mp3 = Gtk.ComboBoxText()
      choice_file2mp3=self.settings['Choice_File2mp3_Bitrate'].split(',')


      #hbox_youtube_dl= Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      #update_youtube_dl = Gtk.Button(label="update youtube-dl")
      #update_youtube_dl.connect("clicked", self.START_UPDATE_YOUTUBE_DL_BUTTON)



      choice_active=0
 
      for i,item in enumerate(choice_file2mp3):
         if item==self.settings['File2mp3_Bitrate']:
            choice_active=i
         combo_file2mp3.insert(i, "%s" %i, "%s" % item)

      combo_file2mp3.set_active(choice_active)
      combo_file2mp3.connect("changed", self.FILE2MP3BITRATE_COMBOBOX)


      hbox_file2mp3.pack_start(label_file2mp3, False, False, 0)
      hbox_file2mp3.pack_start(combo_file2mp3, False, False, 0)
      
      #hbox_youtube_dl.pack_start(update_youtube_dl, False, False, 0)


      grid.attach_next_to(hbox_file2mp3, hbox_coverter, Gtk.PositionType.BOTTOM, 1, 1)
      #grid.attach_next_to(hbox_youtube_dl, hbox_file2mp3, Gtk.PositionType.BOTTOM, 1, 1)



      #############################

      hbox_window = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      label_window = Gtk.Label("Window:", xalign=0)

      hbox_window.pack_start(label_window, False, False, 0)

      #grid.attach_next_to(hbox_window, hbox_youtube_dl, Gtk.PositionType.BOTTOM, 1, 1)
      grid.attach_next_to(hbox_window, hbox_file2mp3, Gtk.PositionType.BOTTOM, 1, 1)

      #############################

      hbox_window_sp = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)


      self.checkbutton_window_size = Gtk.CheckButton('Save Size')
      self.checkbutton_window_size.set_active(1)


      self.checkbutton_window_position = Gtk.CheckButton('Save Position')
      self.checkbutton_window_position.set_active(1)

      hbox_window_sp.pack_start(self.checkbutton_window_size, False, True, 0)
      hbox_window_sp.pack_start(self.checkbutton_window_position, True, True, 0)

      grid.attach_next_to(hbox_window_sp, hbox_window, Gtk.PositionType.BOTTOM, 1, 1)

      #############################


      # empty box for space
      hbox_space = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      grid.attach_next_to(hbox_space, hbox_window, Gtk.PositionType.BOTTOM, 1, 2)


      #############################

      hbox_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      
      self.button_save = Gtk.Button(label="Save")
      self.button_save.connect("clicked", self.SAVE_BUTTON)

      self.button_reset = Gtk.Button(label="Reset")
      self.button_reset.connect("clicked", self.RESET_BUTTON)

      hbox_buttons.pack_start(self.button_save, False, True, 0)
      hbox_buttons.pack_start(self.button_reset, False, True, 0)


      grid.attach_next_to(hbox_buttons, hbox_space, Gtk.PositionType.BOTTOM, 1, 1)


      #############################

      self.box.add(grid)




      """
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
      self.add_FILTER_TEXTCTRL = wx.TextCtrl(self, newid, '%s' % self.settings['Dlna_Filter'], pos=(0, 0), size=(180, 30), style=wx.SUNKEN_BORDER)
      self.Bind(wx.EVT_TEXT, None, id=newid)

      newid = wx.NewId()
      add_PORT_STATICTEXT = wx.StaticText(self, newid, label='Port:')
      newid = wx.NewId()
      self.add_PORT_TEXTCTRL = wx.TextCtrl(self, newid, '%s' % self.settings['Dlna_Port'], pos=(0, 0), size=(80, 30), style=wx.SUNKEN_BORDER)
      self.Bind(wx.EVT_TEXT, None, id=newid)



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

      if self.settings['Debug']==1:
         print ('def change_dlna_colour - colour: %s') % colour

      if colour=='red':
         self.Bind(wx.EVT_PAINT, self.Circle_Red)
      if colour=='orange':
         self.Bind(wx.EVT_PAINT, self.Circle_Orange)
      if colour=='green':
         self.Bind(wx.EVT_PAINT, self.Circle_Green) 

      self.Refresh()


   def START_DLNA_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def START_DLNA_BUTTON - start pulseaudio-dlna')

      self.add_START_DLNA_BUTTON.Disable()
      self.add_STOP_DLNA_BUTTON.Enable()

      # /usr/bin/pulseaudio-dlna --filter-device 'Chromecast' --port 10291

      dlna_filter=''
      cmd = []
      if bool(self.settings['Dlna_Filter']):
         cmd=['pulseaudio-dlna','--port','%s' % self.settings['Dlna_Port'], '--filter-device','%s' % self.settings['Dlna_Filter']]
      else:
         cmd=['pulseaudio-dlna','--port','%s' % self.settings['Dlna_Port']]


      cwd='/usr/bin'
      self.p3.process_starter(cmd=cmd, cwd=cwd, job='dlna', identifier='', source='')

      self.refresh_timer = wx.Timer(self)
      self.Bind(wx.EVT_TIMER, self.refresh_circle_timer, self.refresh_timer)
      self.refresh_timer.Start(1000)



   def STOP_DLNA_BUTTON(self, event):

      if self.settings['Debug']==1:
         print ('def STOP_DLNA_BUTTON - start')

      self.add_START_DLNA_BUTTON.Enable()
      self.add_STOP_DLNA_BUTTON.Disable()

      self.change_dlna_colour('red')
      self.refresh_timer.Stop()

      self.p3.process_job_killer(job='dlna')



   def refresh_circle_timer(self, event):

      if self.settings['Debug']==1:
         print ('def refresh_circle_timer start')


      for item in self.p3.process_database:

         if self.settings['Debug']==1:
            print ('def refresh_circle_timer process_database: %s') % str(self.p3.process_database[item])


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
                        
                        x1 = re.search('Using localhost.*%s' % self.settings['Dlna_Port'], out)
                        if x1:
                           self.change_dlna_colour('orange')
                        x2 = re.search('could not determine your host address', out)
                        if x2:
                           self.change_dlna_colour('red')
                        x3 = re.search('Added the device.*%s' % self.settings['Dlna_Filter'], out)
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

      """



   def FILE2MP3BITRATE_COMBOBOX(self, event):
      if self.settings['Debug']==1:
         print ('def FILE2MP3BITRATE_COMBOBOX - start')

      self.settings['File2mp3_Bitrate'] = event.get_active_text()


   def START_UPDATE_YOUTUBE_DL_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def START_UPDATE_YOUTUBE_DL_BUTTON - start')





   def SAVE_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def SAVE_BUTTON - start')

      self.settings['Directory_New'] = self.entry_input_dir_new.get_text()
      self.settings['Directory_Old'] = self.entry_input_dir_old.get_text()
      self.settings['Directory_Streamripper'] = self.entry_input_dir_st.get_text()
      #self.settings['Dlna_Port'] = self.add_PORT_TEXTCTRL.GetValue()
      #self.settings['Dlna_Filter'] = self.add_FILTER_TEXTCTRL.GetValue()



      if self.checkbutton_window_position.get_active()==True:
         self.settings['Position_X'] = self.settings['Temp_Position_X']
         self.settings['Position_Y'] = self.settings['Temp_Position_Y']

      if self.checkbutton_window_size.get_active()==True:
         self.settings['Size_X'] = self.settings['Temp_Size_X']
         self.settings['Size_Y'] = self.settings['Temp_Size_Y']



      if not os.path.exists('%s/.config/audok' % os.environ['HOME']):
         os.mkdir('%s/.config/audok' % os.environ['HOME'], 0o755);

      f = open('%s/.config/audok/settings.xml' % os.environ['HOME'], 'w')


      f.write('<?xml version="1.0"?>\n')
      f.write('<data>\n')
      for item1 in self.settings:
         f.write('\t<' + str(item1) + '>' + str(self.settings[item1]) + '</' + str(item1) + '>\n')
      f.write('</data>\n')

      f.close()




   def RESET_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def RESET_BUTTON - start')

      if os.path.exists('%s/.config/audok/settings.xml' % os.environ['HOME']):
         os.remove('%s/.config/audok/settings.xml' % os.environ['HOME'])

      self.main.on_reset_close()



   
