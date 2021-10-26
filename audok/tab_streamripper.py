import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GLib', '2.0')
from gi.repository import GLib
import main


class TabStreamRipper:

   def __init__(self, main, config, settings, stationlist):

      self.main = main
      self.config = config
      self.settings = settings
      self.stationlist = stationlist

      self.count=0

      #############################
      self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

      self.grid = Gtk.Grid()
      self.grid.set_column_homogeneous(True)
      self.grid.set_row_homogeneous(True)


      self.record_station = []

      self.station_not_running = []

      #print (repr(self.stationlist))

      self.station_liststore = Gtk.ListStore(int, bool, bool, str, str, str)
      for i, stlist in enumerate(self.stationlist):
         self.station_liststore.append([0, False, False, stlist[0], stlist[1], stlist[2]])


      self.treeview = Gtk.TreeView.new_with_model(model=self.station_liststore)

      self.renderer_spinner = Gtk.CellRendererSpinner()  
      self.column_spinner = Gtk.TreeViewColumn("", self.renderer_spinner, active=0)
      self.treeview.append_column(self.column_spinner)
      self.column_spinner.add_attribute(self.renderer_spinner, "pulse" , 0)




      renderer_toggle = Gtk.CellRendererToggle()
      column_toggle = Gtk.TreeViewColumn("Toggle", renderer_toggle, active=1)
      renderer_toggle.connect("toggled", self.on_cell_toggled)
      self.treeview.append_column(column_toggle)




      renderer = Gtk.CellRendererText()
      renderer.set_property("editable", True)
      column_text = Gtk.TreeViewColumn("Genre", renderer, text=3)
      renderer.connect("edited", self.renderer_genre_edited)
      self.treeview.append_column(column_text)





      renderer = Gtk.CellRendererText()
      renderer.set_property("editable", True)
      renderer.connect("edited", self.renderer_stations_edited)
      column_text = Gtk.TreeViewColumn("Station", renderer, text=4)
      self.treeview.append_column(column_text)




      renderer = Gtk.CellRendererText()
      renderer.set_property("editable", True)
      renderer.connect("edited", self.renderer_url_edited)
      column_text = Gtk.TreeViewColumn("Url", renderer, text=5)
      self.treeview.append_column(column_text)



      scrollable_treelist = Gtk.ScrolledWindow()
      scrollable_treelist.set_vexpand(True)
      self.grid.attach(scrollable_treelist, 0, 0, 8, 10)


      button_selectall = Gtk.Button(label="Select All")
      button_selectall.connect("clicked", self.button_selectall_clicked)

      button_deselectall = Gtk.Button(label="Deselect All")
      button_deselectall.connect("clicked", self.button_deselectall_clicked)

      button_record_start = Gtk.Button(label="Record")
      button_record_start.connect("clicked", self.button_record_clicked)

      button_record_stop = Gtk.Button(label="Stop")
      button_record_stop.connect("clicked", self.button_stop_clicked)

      button_reset = Gtk.Button(label="Reset")
      button_reset.connect("clicked", self.button_reset_clicked)

      button_info = Gtk.Button(label="Info")
      button_info.connect("clicked", self.button_info_clicked)



      self.grid.attach_next_to(button_selectall, scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
      self.grid.attach_next_to(button_deselectall, button_selectall, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_record_start, button_deselectall, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_record_stop, button_record_start, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_reset, button_record_stop, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_info, button_reset, Gtk.PositionType.RIGHT, 1, 1)


      scrollable_treelist.add(self.treeview)
      self.hbox.pack_start(self.grid, True, True, 0)

      ###################################################################################




   def on_cell_toggled(self, widget, path):
      if self.config['debug']==1:
         print ('def on_cell_toggled start widget: %s path: %s' % (widget, path))
      self.station_liststore[path][1] = not self.station_liststore[path][1]




   def renderer_genre_edited(self, widget, path, text):
      if self.config['debug']==1:
         print ('def renderer_genre_edited start widget: %s path: %s text: %s' % (widget, path, text))
      self.station_liststore[path][3] = text
      self.stationlist[int(path)][0] = self.station_liststore[path][3]
      self.config['stationlist_changed']=True


   def renderer_stations_edited(self, widget, path, text):
      if self.config['debug']==1:
         print ('def renderer_stations_edited start widget: %s path: %s text: %s' % (widget, path, text))
      self.station_liststore[path][4] = text
      self.stationlist[int(path)][1] = self.station_liststore[path][4]
      self.config['stationlist_changed']=True



   def renderer_url_edited(self, widget, path, text):
      if self.config['debug']==1:
         print ('def renderer_url_edited start widget: %s path: %s text: %s' % (widget, path, text))
      self.station_liststore[path][5] = text
      self.stationlist[int(path)][2] = self.station_liststore[path][5]
      self.config['stationlist_changed']=True



   def button_selectall_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_selectall_clicked start')

      for i, item in enumerate(self.station_liststore):
         self.station_liststore[i][1] = True



   def button_deselectall_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_deselectall_clicked start')

      for i, item in enumerate(self.station_liststore):
         self.station_liststore[i][1] = False




   def button_reset_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_reset_clicked - start')

      if os.path.exists('%s/%s' % (self.settings['config_path'],self.settings['filename_stations'])):
         os.remove('%s/%s' % (self.settings['config_path'],self.settings['filename_stations']))

      self.main.on_reset_close()



   
   def button_info_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_info_clicked - start')

      #button = Gtk.LinkButton("https://www.shoutcast.com", label=Shoutcast")

      dialog = Gtk.MessageDialog(parent=None,
                                 message_type=Gtk.MessageType.INFO,
                                 flags=Gtk.DialogFlags.MODAL,
                                 buttons=("Ok",Gtk.ButtonsType.OK),
                                 text="Get new stations from: https://www.shoutcast.com")


      dialog.set_title('Info')
      dialog.show()
      dialog.run()
      dialog.destroy()





   def check_streamripper(self):

      self.count+=1

      if self.station_not_running:
         if self.config['debug']==1:
            print ('def check_streamripper record_station %s station_not_running: %s' % (self.record_station,self.station_not_running))

      if not bool(list(set(self.record_station) - set(self.station_not_running))):
         if self.config['debug']==1:
            print ('def check_streamripper stop')
         del self.glib_timer_streamripper
         return False




      station_update_counter = []

      for i in self.record_station:
         not_runing=0
         for z in self.station_not_running:
            if i==z:
               not_runing=1
         if not_runing==0:
            station_update_counter.extend([i])


      for i, item in enumerate(self.station_liststore):
         for z in station_update_counter:
            if i==z:
               self.station_liststore[i][0]=self.count




      # find stations that are not running
      for item in self.record_station:

         for num in self.main.process_database:
            if self.main.process_database[num]['job']=='streamripper':

               if int(self.main.process_database[num]['identifier'])==item:

                  # set status inactive
                  if self.main.process_database[num]['todo']=='result':
                     self.main.process_database[num]['status']='inactive'

                  if self.main.process_database[num]['status']=='killed':
                     self.main.process_database[num]['status']='inactive'



                  if self.main.process_database[num]['status']=='inactive':
                     if self.config['debug']==1:
                        print ('def check_streamripper status: inactive output: %s' % self.main.process_database[num]['output'])
                     self.station_liststore[item][0]=0
                     self.station_not_running.extend([item])

                  else:
                     if self.config['debug']==1:
                        print ('def check_streamripper station: %s count: %s' % (item,self.station_liststore[item][0]))



      self.station_not_running = list(set(self.station_not_running))

      return True






   def button_record_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_record_clicked start')


      if not hasattr(self, 'glib_timer_streamripper'):
         self.glib_timer_streamripper = GLib.timeout_add_seconds(1, self.check_streamripper)


      if not os.path.exists(self.settings['music_path'] + '/' + self.settings['directory_str']):
         os.mkdir(self.settings['music_path'] + '/' + self.settings['directory_str'])



      # reset
      self.record_station = []


      for i, item in enumerate(self.station_liststore):
         if self.station_liststore[i][1]==True:

            self.record_station.extend([i])

            if self.config['debug']==1:
               print ('def button_record_clicked identifier: %s file: %s' % (i,self.stationlist[i]))

            # streamripper http://www.top100station.de/switch/r3472.pls -u WinampMPEG/5.0 -d /MyDisc/Audio/Neu/Streamtuner/

            cmd=[self.settings['bin_streamripper'], self.station_liststore[i][5],'-u','WinampMPEG/5.0','-d','%s/%s' % (self.settings['music_path'],self.settings['directory_str'])]
            cwd=self.settings['music_path'] + '/' + self.settings['directory_str']
            self.main.process_starter(cmd=cmd, cwd=cwd, job='streamripper', identifier=str(i), source=self.station_liststore[i][5])

      self.record_station = list(set(self.record_station))




   def button_stop_clicked(self, event):
      if self.config['debug']==1:
         print ('def button_stop_clicked start')


      # reset
      self.station_not_running = []
      for i, item in enumerate(self.station_liststore):
         self.station_liststore[i][0]=0


      if hasattr(self, 'glib_timer_streamripper'):
         if self.config['debug']==1:
            print ('def button_stop_clicked remove glib timer')
         GLib.source_remove(self.glib_timer_streamripper)
         del self.glib_timer_streamripper

      self.main.process_job_killer(job='streamripper')
