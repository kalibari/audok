import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GLib', '2.0')
from gi.repository import GLib
import math
import cairo


class TabStreamRipper:

   def __init__(self, main, settings, stationlist):
      self.main = main
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




      self.renderer = Gtk.CellRendererText()
      self.renderer.set_property("editable", True)
      column_text = Gtk.TreeViewColumn("Genre", self.renderer, text=3)
      self.renderer.connect("edited", self.text_edited_genre)
      self.treeview.append_column(column_text)





      renderer = Gtk.CellRendererText()
      renderer.set_property("editable", True)
      renderer.connect("edited", self.text_edited_station)
      column_text = Gtk.TreeViewColumn("Station", renderer, text=4)
      self.treeview.append_column(column_text)




      renderer = Gtk.CellRendererText()
      renderer.set_property("editable", True)
      renderer.connect("edited", self.text_edited_url)
      column_text = Gtk.TreeViewColumn("Url", renderer, text=5)
      self.treeview.append_column(column_text)



      self.scrollable_treelist = Gtk.ScrolledWindow()
      self.scrollable_treelist.set_vexpand(True)
      self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)


      button_selectall = Gtk.Button(label="Select All")
      button_selectall.connect("clicked", self.SELECT_ALL_BUTTON)

      button_deselectall = Gtk.Button(label="Deselect All")
      button_deselectall.connect("clicked", self.DESELECT_ALL_BUTTON)

      button_record_start = Gtk.Button(label="Record")
      button_record_start.connect("clicked", self.START_RECORD_BUTTON)

      button_record_stop = Gtk.Button(label="Stop")
      button_record_stop.connect("clicked", self.STOP_RECORD_BUTTON)

      self.button_save = Gtk.Button(label="Save")
      self.button_save.connect("clicked", self.SAVE_BUTTON)
      self.button_save.set_sensitive(False)


      button_reset = Gtk.Button(label="Reset")
      button_reset.connect("clicked", self.RESET_BUTTON)

      button_info = Gtk.Button(label="Info")
      button_info.connect("clicked", self.INFO_BUTTON)



      self.grid.attach_next_to(button_selectall, self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
      self.grid.attach_next_to(button_deselectall, button_selectall, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_record_start, button_deselectall, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_record_stop, button_record_start, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(self.button_save, button_record_stop, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_reset, self.button_save, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_info, button_reset, Gtk.PositionType.RIGHT, 1, 1)


      self.scrollable_treelist.add(self.treeview)
      self.hbox.pack_start(self.grid, True, True, 0)

      ###################################################################################




#   def my_title_cell_data_func(self, tree_column, cell, tree_model, iter, data):
#      """ Eine eigene cell_data_func für Item.title"""
#      obj = tree_model[iter][0]    # Objekt für aktuelle Zeile
#      #cell.set_property('text', obj.title)
#      print ('def kkkkkkkkkkkkkkkkk')





   def on_cell_toggled(self, widget, path):
      if self.settings['Debug']==1:
         print ('def on_cell_toggled start widget: %s path: %s' % (widget, path))
      self.station_liststore[path][1] = not self.station_liststore[path][1]




   def text_edited_genre(self, widget, path, text):
      if self.settings['Debug']==1:
         print ('def text_edited_genre start widget: %s path: %s text: %s' % (widget, path, text))
      self.station_liststore[path][3] = text
      self.stationlist[int(path)][0] = self.station_liststore[path][3]
      self.button_save.set_sensitive(True)



   def text_edited_station(self, widget, path, text):
      if self.settings['Debug']==1:
         print ('def text_edited_station start widget: %s path: %s text: %s' % (widget, path, text))
      self.station_liststore[path][4] = text
      self.stationlist[int(path)][1] = self.station_liststore[path][4]
      self.button_save.set_sensitive(True)



   def text_edited_url(self, widget, path, text):
      if self.settings['Debug']==1:
         print ('def text_edited_url start widget: %s path: %s text: %s' % (widget, path, text))
      self.station_liststore[path][5] = text
      self.stationlist[int(path)][2] = self.station_liststore[path][5]
      self.button_save.set_sensitive(True)






   def SELECT_ALL_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def SELECT_ALL_BUTTON start')

      for i, item in enumerate(self.station_liststore):
         self.station_liststore[i][1] = True



   def DESELECT_ALL_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def DESELECT_ALL_BUTTON start')

      for i, item in enumerate(self.station_liststore):
         self.station_liststore[i][1] = False





   def SAVE_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def SAVE_BUTTON start')

      self.button_save.set_sensitive(False)

      # Save new Stations
      if not os.path.exists('%s/.config/%s' % (os.environ['HOME'], self.settings['Name'])):
         os.mkdir('%s/.config/%s' % (os.environ['HOME'], self.settings['Name']), 0o755);
      f = open('%s/.config/%s/stations.xml' % (os.environ['HOME'], self.settings['Name']), 'w')
      f.write('<?xml version="1.0"?>\n')
      f.write('<data>\n')


      for i, item in enumerate(self.station_liststore):
         #print (self.stationlist[i][0])  # Alternative
         #print (self.stationlist[i][1])  # Radio freeFM Ulm
         #print (self.stationlist[i][2])  # http://stream.freefm.de:8100/listen.pls
         f.write('\t<station>\n' + '\t\t<name>' + str(self.stationlist[i][0]) + '</name>\n'  + '\t\t<genre>' + str(self.stationlist[i][1]) + '</genre>\n'  + '\t\t<url>' + str(self.stationlist[i][2]) +  '</url>\n' +  '\t</station>\n')

      f.write('</data>\n')

      f.close()




   def RESET_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def RESET_BUTTON - start')

      if os.path.exists('%s/.config/audok/stations.xml' % os.environ['HOME']):
         os.remove('%s/.config/audok/stations.xml' % os.environ['HOME'])

      self.main.on_reset_close()


   
   def INFO_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def INFO_BUTTON - start')

      #dlg = self.Info_Dialog()
      #dlg.ShowModal()
      #dlg.Destroy()



   """
   class Info_Dialog(wx.Dialog):
      def __init__(self):
         wx.Dialog.__init__(self, None, -1, 'Info', size=(450, 150))

         newid = wx.NewId()
         add_link_HyperlinkCtrl = wx.HyperlinkCtrl(self, id=newid, label='Get new stations at: http://www.shoutcast.com', url='http://www.shoutcast.com', pos=(10, 10), size=(400, 30), style=wx.HL_ALIGN_CENTRE|wx.HL_DEFAULT_STYLE)
   """





   def check_streamripper(self):

      self.count+=1


      if self.station_not_running:
         if self.settings['Debug']==1:
            print ('def check_streamripper record_station %s station_not_running: %s' % (self.record_station,self.station_not_running))


      if not bool(list(set(self.record_station) - set(self.station_not_running))):
         if self.settings['Debug']==1:
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
                     if self.settings['Debug']==1:
                        print ('def check_streamripper status: inactive output: %s' % self.main.process_database[num]['output'])
                     self.station_liststore[item][0]=0
                     self.station_not_running.extend([item])

                  else:
                     if self.settings['Debug']==1:
                        print ('def check_streamripper station: %s count: %s' % (item,self.station_liststore[item][0]))



      self.station_not_running = list(set(self.station_not_running))

      return True






   def START_RECORD_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def START_RECORD_BUTTON start')


      if not hasattr(self, 'glib_timer_streamripper'):
         self.glib_timer_streamripper = GLib.timeout_add_seconds(1, self.check_streamripper)


      if (os.path.exists(self.settings['Directory_Streamripper']))==False:
         os.mkdir(self.settings['Directory_Streamripper'])



      # reset
      self.record_station = []


      for i, item in enumerate(self.station_liststore):
         if self.station_liststore[i][1]==True:

            self.record_station.extend([i])

            if self.settings['Debug']==1:
               print ('def START_RECORD_BUTTON identifier: %s file: %s' % (i,self.stationlist[i]))

            # streamripper http://www.top100station.de/switch/r3472.pls -u WinampMPEG/5.0 -d /MyDisc/Audio/Neu/Streamtuner/

            cmd=['streamripper','%s' % self.station_liststore[i][5],'-u','WinampMPEG/5.0','-d','%s' % self.settings['Directory_Streamripper']]
            cwd=self.settings['Directory_Streamripper']
            self.main.process_starter(cmd=cmd, cwd=cwd, job='streamripper', identifier=str(i), source=self.station_liststore[i][5])
            ##item.set_property("editable", True)
            ##self.station_liststore[i].SetEditable(False)

         #identifier+=1

      self.record_station = list(set(self.record_station))


      #if checkbox_enabled==0:
      #   self.add_STOP_RECORD_BUTTON.set_sensitive(False)
      #   self.add_EDIT_BUTTON.Enable()
      #   self.add_RESET_BUTTON.Enable()




   def STOP_RECORD_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def STOP_RECORD_BUTTON start')

      #self.refresh_timer.Stop()

      #self.add_START_RECORD_BUTTON.set_sensitive(True)
      #self.add_STOP_RECORD_BUTTON.set_sensitive(False)

      #self.add_EDIT_BUTTON.Enable()
      #self.add_SAVE_BUTTON.Enable()
      #self.add_RESET_BUTTON.Enable()



      # reset
      self.station_not_running = []
      for i, item in enumerate(self.station_liststore):
         self.station_liststore[i][0]=0


      if hasattr(self, 'glib_timer_streamripper'):
         if self.settings['Debug']==1:
            print ('def STOP_RECORD_BUTTON remove glib timer')
         GLib.source_remove(self.glib_timer_streamripper)
         del self.glib_timer_streamripper


      #for item in self.checkbox:
      #   item.Enable()

      self.main.process_job_killer(job='streamripper')

