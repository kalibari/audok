import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GLib', '2.0')
from gi.repository import GLib

class TabStreamRipper:

   def __init__(self, madmin, log, config, settings, stationlist):

      self.madmin = madmin
      self.log = log
      self.config = config
      self.settings = settings
      self.stationlist = stationlist

      self.obj_timer_streamripper=None

      self.count=0

      self.pre_stationlist = [['Alternative', 'Radio freeFM Ulm', 'http://stream.freefm.de:7000/Studio'],
                              ['Alternative', 'Radio FM 4 at', 'https://orf-live.ors-shoutcast.at/fm4-q2a'],
                              ['Alternative', 'Zeilsteen Radio', 'http://live.zeilsteen.com:80'],

                              ['Mix', '1.FM - Gorilla FM', 'http://185.33.21.112:80/gorillafm_128'],

                              ['Electro', 'radio Top 40 Elekcro', 'http://antenne-th.divicon-stream.net/antth_top40electro_JlSz-mp3-192?sABC=58p2q700%230%232pn8rp1qoro76pp9n0r46nspn714s714%23fgernz.enqvbgbc40.qr'],
                              ['Electro', 'Sunshine Live','http://sunshinelive.hoerradar.de/sunshinelive-live-mp3-hq'],

                              ['Charts', 'radio Top 40 Weimar Charts', 'http://antenne-th.divicon-stream.net/antth_top40char_0f6x-mp3-192?sABC=58p2q6s8%230%232pn8rp1qoro76pp9n0r46nspn714s714%23fgernz.enqvbgbc40.qr'],
                              ['Charts', 'Top 100 Station','http://www.top100station.de/switch/r3472.pls'],
                              ['Charts', 'radio Top 40 Weimar Live', 'http://antenne-th.divicon-stream.net/antth_top40live_SeJx-mp3-192?sABC=58p2q6rq%230%232pn8rp1qoro76pp9n0r46nspn714s714%23fgernz.enqvbgbc40.qr'],

                              ['Mix', 'Gizmo New 102 (The Mixx)', 'http://206.190.135.28:8302/stream'],
                              ['Pop', 'Antenne Bayern Fresh4You', 'http://mp3channels.webradio.antenne.de/fresh'],

                              ['Rock', 'PureRock.US', 'http://167.114.64.181:8524/stream']]




      #############################
      self.grid = Gtk.Grid()
      self.grid.set_column_homogeneous(True)
      #self.grid.set_row_homogeneous(True)


      self.record_station = []

      toogle_num=0

      self.station_liststore = Gtk.ListStore(int, bool, bool, str, str, str)
      for stlist in self.stationlist:
         toogle_on=False
         if str(toogle_num) in self.settings['stations_toogle_on']:
            toogle_on=True
         toogle_num+=1
         self.station_liststore.append([0, toogle_on, False, stlist[0], stlist[1], stlist[2]])


      for i, stlist in enumerate(self.pre_stationlist):
         toogle_on=False
         if str(toogle_num) in self.settings['stations_toogle_on']:
            toogle_on=True
         toogle_num+=1
         self.station_liststore.append([0, toogle_on, False, stlist[0], stlist[1], stlist[2]])



      self.treeview = Gtk.TreeView.new_with_model(model=self.station_liststore)
      self.treeview.connect('button-press-event', self.treeview_press_event)


      self.renderer_spinner = Gtk.CellRendererSpinner()  
      self.column_spinner = Gtk.TreeViewColumn('', self.renderer_spinner, active=0)
      self.treeview.append_column(self.column_spinner)
      self.column_spinner.add_attribute(self.renderer_spinner, 'pulse' , 0)



      renderer_toggle = Gtk.CellRendererToggle()
      column_toggle = Gtk.TreeViewColumn('Toggle', renderer_toggle, active=1)
      renderer_toggle.connect('toggled', self.on_cell_toggled)
      self.treeview.append_column(column_toggle)
      self.treeview.set_activate_on_single_click(True)


      self.renderer_genre = Gtk.CellRendererText()
      self.renderer_genre.set_property('editable', True)
      column_text = Gtk.TreeViewColumn('Genre', self.renderer_genre, text=3)
      self.renderer_genre.connect('edited', self.renderer_genre_edited)
      self.treeview.append_column(column_text)



      self.renderer_stations = Gtk.CellRendererText()
      self.renderer_stations.set_property('editable', True)
      self.renderer_stations.connect('edited', self.renderer_stations_edited)
      column_text = Gtk.TreeViewColumn('Station', self.renderer_stations, text=4)
      self.treeview.append_column(column_text)



      self.renderer_url = Gtk.CellRendererText()
      self.renderer_url.set_property('editable', True)
      self.renderer_url.connect('edited', self.renderer_url_edited)
      column_text = Gtk.TreeViewColumn('Url', self.renderer_url, text=5)
      self.treeview.append_column(column_text)


      scrollable_treelist = Gtk.ScrolledWindow()
      scrollable_treelist.set_vexpand(True)
      scrollable_treelist.add(self.treeview)
      self.grid.attach(scrollable_treelist, 0, 0, 8, 10)



      button_selectall = Gtk.Button(label='Select All')
      button_selectall.connect('clicked', self.button_selectall_clicked)

      button_deselectall = Gtk.Button(label='Deselect All')
      button_deselectall.connect('clicked', self.button_deselectall_clicked)

      button_record_start = Gtk.Button(label='Record')
      button_record_start.connect('clicked', self.button_record_clicked)

      button_record_stop = Gtk.Button(label='Stop')
      button_record_stop.connect('clicked', self.button_stop_clicked)

      button_new_station = Gtk.Button(label='New Station')
      button_new_station.connect('clicked', self.button_new_station_clicked)

      button_delete_station = Gtk.Button(label='Delete Station')
      button_delete_station.connect('clicked', self.button_delete_station_clicked)

      button_reset = Gtk.Button(label='Reset')
      button_reset.connect('clicked', self.button_reset_clicked)

      button_info = Gtk.Button(label='Info')
      button_info.connect('clicked', self.button_info_clicked)

      self.grid.attach_next_to(button_selectall, scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
      self.grid.attach_next_to(button_deselectall, button_selectall, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_record_start, button_deselectall, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_record_stop, button_record_start, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_new_station, button_record_stop, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_delete_station, button_new_station, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_reset, button_delete_station, Gtk.PositionType.RIGHT, 1, 1)
      self.grid.attach_next_to(button_info, button_reset, Gtk.PositionType.RIGHT, 1, 1)


      self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      self.hbox.pack_start(self.grid, True, True, 0)



   def on_cell_toggled(self, widget, row):

      self.log.debug('start row: %s' % row)

      toogle = widget.get_active()

      if toogle==True:
         self.station_liststore[row][1] = False
         if row in self.settings['stations_toogle_on']:
            self.settings['stations_toogle_on'].remove(row)

      else:
         self.station_liststore[row][1] = True
         if not row in self.settings['stations_toogle_on']:
            self.settings['stations_toogle_on'].extend([row])

      self.log.debug('stations_toogle_on: %s' % self.settings['stations_toogle_on'])





   def treeview_press_event(self, treeview, event):

      self.log.debug('start')

      model, treeiter = treeview.get_selection().get_selected()
      if treeiter is not None:
         path = model.get_path(treeiter)
         num = int(path.to_string())

         self.log.debug('num: %s' % num)

         if num>=len(self.stationlist):
            self.renderer_genre.set_property('editable', False)
            self.renderer_stations.set_property('editable', False)
            self.renderer_url.set_property('editable', False)
         else:
            self.renderer_genre.set_property('editable', True)
            self.renderer_stations.set_property('editable', True)
            self.renderer_url.set_property('editable', True)



   def renderer_genre_edited(self, widget, row, text):

      self.log.debug('start row: %s text: %s len(self.stationlist): %s' % (row, text, len(self.stationlist)))

      row=int(row)
      self.station_liststore[row][3] = text
      self.stationlist[row][0] = text
      self.config['stations_changed']=True




   def renderer_stations_edited(self, widget, row, text):

      self.log.debug('start row: %s text: %s len(self.stationlist): %s' % (row, text, len(self.stationlist)))

      row=int(row)
      self.station_liststore[row][4] = text
      self.stationlist[row][1] = text
      self.config['stations_changed']=True




   def renderer_url_edited(self, widget, row, text):

      self.log.debug('start row: %s text: %s len(self.stationlist): %s' % (row, text, len(self.stationlist)))

      row=int(row)
      self.station_liststore[row][5] = text
      self.stationlist[row][2] = text
      self.config['stations_changed']=True




   def button_selectall_clicked(self, event):

      self.log.debug('start')

      self.settings['stations_toogle_on']=[]
      for i, item in enumerate(self.station_liststore):
         self.station_liststore[i][1] = True
         self.settings['stations_toogle_on'].extend([str(i)])




   def button_deselectall_clicked(self, event):

      self.log.debug('start')

      for i, item in enumerate(self.station_liststore):
         self.station_liststore[i][1] = False

      self.settings['stations_toogle_on'] = []



   def button_reset_clicked(self, event):

      self.log.debug('start')

      if os.path.exists('%s/%s' % (self.settings['config_path'],self.settings['filename_stations'])):
         os.remove('%s/%s' % (self.settings['config_path'],self.settings['filename_stations']))

      self.madmin.on_reset_close()



   def button_info_clicked(self, event):

      self.log.debug('start')

      url=['https://directory.shoutcast.com','https://radio.alltrack.org']

      dialog = Gtk.MessageDialog(parent=None,
                                 message_type=Gtk.MessageType.INFO,
                                 flags=Gtk.DialogFlags.MODAL,
                                 buttons=('Ok',Gtk.ButtonsType.OK),
                                 text='Get new stations from: %s' % ', '.join(url))

      dialog.set_title('Info')
      dialog.show()
      dialog.run()
      dialog.destroy()



   def check_streamripper(self):

      self.count+=1

      self.log.debug('record_station: %s' % self.record_station)


      if not self.record_station:
         self.log.debug('stop')

         if self.obj_timer_streamripper is not None:
            GLib.source_remove(self.obj_timer_streamripper)
            self.obj_timer_streamripper=None

         return False


      for i, item in enumerate(self.station_liststore):
         if i in self.record_station:
            self.station_liststore[i][0]=self.count


      remove_pnum=[]

      # find stations that are not running
      for pnum in self.madmin.process_database:
         if self.madmin.process_database[pnum]['job']=='streamripper':

            identifier = self.madmin.process_database[pnum]['identifier']

            if int(identifier) in self.record_station:

               # set status inactive
               if self.madmin.process_database[pnum]['todo']=='result':
                  self.madmin.process_database[pnum]['status']='inactive'

               if self.madmin.process_database[pnum]['status']=='killed':
                  self.madmin.process_database[pnum]['status']='inactive'


               if self.madmin.process_database[pnum]['status']=='inactive':
                  remove_pnum.extend([pnum])
                  self.station_liststore[int(identifier)][0]=0
                  self.record_station.remove(int(identifier))


      for pnum in remove_pnum:
         del self.madmin.process_database[pnum]

      return True




   def button_record_clicked(self, event):

      self.log.debug('start')

      toogle_on = []
      for i, item in enumerate(self.station_liststore):
         if self.station_liststore[i][1]==True:
            toogle_on.extend([i])

      if toogle_on:

         if self.obj_timer_streamripper is None:
            self.obj_timer_streamripper = GLib.timeout_add(1000, self.check_streamripper)


         if not os.path.exists(self.settings['music_path'] + '/' + self.settings['directory_str']):
            os.mkdir(self.settings['music_path'] + '/' + self.settings['directory_str'])


         self.log.debug('record_station: %s' % self.record_station)


         for i in toogle_on:
            if not i in self.record_station:

               self.record_station.extend([i])

               self.log.debug('toogle_on i: %s' % i)

               # streamripper http://www.top100station.de/switch/r3472.pls -u WinampMPEG/5.0 -d /Music/Streamtuner/
               cmd=[self.config['bin_streamripper'], self.station_liststore[i][5],'-u','WinampMPEG/5.0','-d','%s/%s' % (self.settings['music_path'],self.settings['directory_str'])]
               cwd=self.settings['music_path'] + '/' + self.settings['directory_str']
               self.madmin.process_starter(cmd=cmd, cwd=cwd, job='streamripper', identifier=str(i), source=self.station_liststore[i][5])





   def stop_ripper_process(self):
      self.log.debug('start')

      toogle_on = []
      for i, item in enumerate(self.station_liststore):
         if self.station_liststore[i][1]==True:
            toogle_on.extend([i])

      for i in toogle_on:
         self.madmin.process_job_identifier_killer(job='streamripper', identifier=str(i))




   def button_stop_clicked(self, event):

      self.log.debug('start')
      self.stop_ripper_process()




   def button_delete_station_clicked(self, event):

      len_stationlist=len(self.stationlist)
      len_pre_stationlist=len(self.pre_stationlist)

      self.log.debug('len_stationlist: %s len_pre_stationlist: %s' % (len_stationlist,len_pre_stationlist))


      self.stop_ripper_process()


      remove_iter = []
      remove_stationlist = []
      for i, item in enumerate(self.station_liststore):
         if self.station_liststore[i][1]==True:
            x = self.station_liststore.get_iter(i)
            if i<len_stationlist:
               remove_iter.extend([x])
               remove_stationlist.extend([i])


      if remove_iter:
         for x in remove_iter:
            self.station_liststore.remove(x)


      if remove_stationlist:
         new_playlist=[]
         for i,item in enumerate(self.stationlist):
            if not i in remove_stationlist:
               new_playlist.extend([item])
         self.stationlist=new_playlist


      self.settings['stations_toogle_on'] = []
      self.config['stations_changed'] = True

      self.log.debug('len(stationlist): %s' % len(self.stationlist))





   def button_new_station_clicked(self, event):
      
      self.log.debug('start')

      self.station_liststore.insert(position=0, row=[0, False, False, '','New Station', ''])
      self.stationlist.extend([['','New Station','']])

      self.settings['stations_toogle_on'] = []
      self.config['stations_changed']=True

