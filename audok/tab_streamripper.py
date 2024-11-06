import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('GLib', '2.0')
gi.require_version('GdkPixbuf', '2.0')
from gi.repository import Gtk, GLib, GdkPixbuf

class TabStreamRipper:

   def __init__(self, madmin, log, config, settings, stationlist):

      self.madmin = madmin
      self.log = log
      self.config = config
      self.settings = settings
      self.stationlist = stationlist

      self.obj_timer_streamripper=None

      self.record_status=False

      """
      Links:
      https://www.radiotop40.de/empfang
      https://www.radiofg.com/
      """


      self.pre_stationlist = [['Alternative', 'Radio freeFM Ulm', '', 'http://stream.freefm.de:7000/Studio'],
                              ['Alternative', 'Radio FM 4 at', '', 'https://orf-live.ors-shoutcast.at/fm4-q2a'],
                              ['Alternative', 'Zeilsteen Radio', '-u WinampMPEG/5.0', 'http://live.zeilsteen.com:80'],

                              ['Mix / Alternative', 'Gorilla FM', '', 'http://185.33.21.112:80/gorillafm_128'],

                              ['Electro', 'Radio Top 40 Clubsound', '', 'https://frontend.streamonkey.net/antthue-radiotop40clubsound/stream/mp3'],
                              ['Electro', 'Sunshine Live', '', 'http://sunsl.streamabc.net/sunsl-sslsimulcast-mp3-192-4434053'],

                              ['Charts', 'Radio Fg', '-u FreeAmp/2.x', 'https://n11a-eu.rcs.revma.com/wknqhm4yuchvv'],
                              ['Charts', 'Radio Top 40 Charts', '', 'https://frontend.streamonkey.net/antthue-radiotop40charts/stream/mp3'],
                              ['Charts', 'Top 100 Station', '', 'https://streams.rautemusik.fm/top100station/?ref=t100swebsite'],
                              ['Charts', 'Radio Top 40 Live', '', 'https://frontend.streamonkey.net/antthue-radiotop40/stream/mp3'],
                              ['Charts', 'Energy Bremen Germany Top40', '', 'https://edge63.streamonkey.net/energy-top40'],

                              ['Pop', 'Antenne Bayern Fresh4You', '', 'http://mp3channels.webradio.antenne.de/fresh'],

                              ['Rock', 'Antenne Bayern Rock', '', 'http://mp3channels.webradio.antenne.de/rockantenne']]


      self.grid = Gtk.Grid()
      self.grid.set_column_homogeneous(True)
      #self.grid.set_row_homogeneous(True)


      self.record_station = []

      self.pixbuf_record_active = GdkPixbuf.Pixbuf.new_from_file("%s/record_active.png" % self.config['app_path'])
      self.pixbuf_record_inactive = GdkPixbuf.Pixbuf.new_from_file("%s/record_inactive.png" % self.config['app_path'])

      # Rec | Sel | Del | Genre | Station | Ripper Options | Url
      self.liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, bool, str, str, str, str, str)
      self.update_listmodel()


      self.treeview = Gtk.TreeView.new_with_model(model=self.liststore)
      self.treeview.connect('row-activated', self.treeview_row_activated)
      self.treeview.set_activate_on_single_click(True)


      renderer_pixbuf_rec = Gtk.CellRendererPixbuf()
      renderer_pixbuf_rec.set_fixed_size(50, 30)
      self.column_delete = Gtk.TreeViewColumn('Rec', renderer_pixbuf_rec, pixbuf=0)
      self.treeview.append_column(self.column_delete)


      renderer_rec = Gtk.CellRendererToggle()
      renderer_rec.set_fixed_size(50, 30)
      column_rec = Gtk.TreeViewColumn('Sel', renderer_rec, active=1)
      renderer_rec.connect('toggled', self.on_cell_toggled)
      self.treeview.append_column(column_rec)


      renderer_pixbuf_del = Gtk.CellRendererPixbuf()
      renderer_pixbuf_del.set_fixed_size(50, 30)
      self.column_delete = Gtk.TreeViewColumn('Del', renderer_pixbuf_del, icon_name=2)
      self.treeview.append_column(self.column_delete)


      self.renderer_genre = Gtk.CellRendererText()
      self.renderer_genre.set_property('editable', True)
      self.renderer_genre.set_fixed_size(150, 30)
      column_genre = Gtk.TreeViewColumn('Genre', self.renderer_genre, text=3)
      self.renderer_genre.connect('edited', self.renderer_genre_edited)
      self.treeview.append_column(column_genre)


      self.renderer_stations = Gtk.CellRendererText()
      self.renderer_stations.set_property('editable', True)
      self.renderer_stations.set_fixed_size(250, 30)
      self.renderer_stations.connect('edited', self.renderer_stations_edited)
      column_station = Gtk.TreeViewColumn('Station', self.renderer_stations, text=4)
      self.treeview.append_column(column_station)


      self.renderer_ripper_options = Gtk.CellRendererText()
      self.renderer_ripper_options.set_property('editable', True)
      self.renderer_ripper_options.set_fixed_size(200, 30)
      self.renderer_ripper_options.connect('edited', self.renderer_ripper_options_edited)
      column_station = Gtk.TreeViewColumn('Ripper Options', self.renderer_ripper_options, text=5)
      self.treeview.append_column(column_station)


      self.renderer_url = Gtk.CellRendererText()
      self.renderer_url.set_property('editable', True)
      self.renderer_url.connect('edited', self.renderer_url_edited)
      column_url = Gtk.TreeViewColumn('Url', self.renderer_url, text=6)
      column_url.set_expand(True)
      self.treeview.append_column(column_url)



      self.scrolledwindow = Gtk.ScrolledWindow()
      self.scrolledwindow.set_vexpand(True)
      self.scrolledwindow.set_hexpand(True)
      self.scrolledwindow.set_child(self.treeview)
      self.scrolledwindow.set_child(self.treeview)
      self.scrolledwindow.set_margin_bottom(5)


      self.grid.attach(self.scrolledwindow, 1, 1, 1, 1)


      hbox_buttons = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)


      button_selectall = Gtk.Button(label='Select All')
      button_selectall.connect('clicked', self.button_selectall_clicked)

      button_deselectall = Gtk.Button(label='Deselect All')
      button_deselectall.connect('clicked', self.button_deselectall_clicked)

      button_record_start = Gtk.Button(label='Start Record')
      button_record_start.connect('clicked', self.button_record_clicked)

      button_record_stop = Gtk.Button(label='Stop Record')
      button_record_stop.connect('clicked', self.button_stop_clicked)

      button_new_station = Gtk.Button(label='New Station')
      button_new_station.connect('clicked', self.button_new_station_clicked)

      button_reset = Gtk.Button(label='Reset')
      button_reset.connect('clicked', self.button_reset_clicked)

      button_info = Gtk.Button(label='Info')
      button_info.connect('clicked', self.button_info_clicked)

      hbox_buttons.append(button_selectall)
      hbox_buttons.append(button_deselectall)
      hbox_buttons.append(button_record_start)
      hbox_buttons.append(button_record_stop)
      hbox_buttons.append(button_new_station)
      hbox_buttons.append(button_reset)
      hbox_buttons.append(button_info)
      hbox_buttons.set_margin_start(5)

      self.grid.attach_next_to(hbox_buttons, self.scrolledwindow, Gtk.PositionType.BOTTOM, 1, 1)


      self.hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      self.hbox.append(self.grid)
      self.hbox.set_margin_bottom(5)



   def on_cell_toggled(self, widget, row):

      self.log.debug('start row: %s' % row)

      toogle = widget.get_active()

      if toogle==True:
         self.liststore[row][1] = False
         if row in self.settings['stations_toogle_on']:
            self.settings['stations_toogle_on'].remove(row)

      else:
         self.liststore[row][1] = True
         if not row in self.settings['stations_toogle_on']:
            self.settings['stations_toogle_on'].extend([row])

      self.log.debug('stations_toogle_on: %s' % self.settings['stations_toogle_on'])



   def treeview_press_event(self, treeview, event):
      self.log.debug('start')



   def treeview_row_activated(self, tree, path, column):
      # Gtk.TreeView, 2, Gtk.TreeViewColumn
      self.log.debug('start')

      model, treeiter = tree.get_selection().get_selected()
      if treeiter is not None:
         path = model.get_path(treeiter)
         row = int(path.to_string())
         itr = self.liststore.get_iter(path)
         num = self.liststore.get_value(itr, 0)

         self.log.debug('row: %s len(self.stationlist): %s' % (row,len(self.stationlist)))


         if row>=len(self.stationlist):
            self.renderer_genre.set_property('editable', False)
            self.renderer_stations.set_property('editable', False)
            self.renderer_ripper_options.set_property('editable', False)
            self.renderer_url.set_property('editable', False)
         else:
            self.renderer_genre.set_property('editable', True)
            self.renderer_stations.set_property('editable', True)
            self.renderer_ripper_options.set_property('editable', True)
            self.renderer_url.set_property('editable', True)

            if column is self.column_delete:
               self.log.debug('delete: %s' % self.stationlist[row])
               if row <= len(self.stationlist):
                  del self.stationlist[row]
                  self.config['stations_changed'] = True

               self.update_listmodel()




   def update_listmodel(self):
      self.log.debug('start')

      self.liststore.clear()

      for i,stlist in enumerate(self.stationlist):
         toogle_on=False
         if str(i) in self.settings['stations_toogle_on']:
            toogle_on=True
         url=stlist[2]
         if self.record_status==False:
            self.liststore.append([self.pixbuf_record_inactive, toogle_on, 'list-remove', stlist[0], stlist[1], stlist[2], stlist[3]])
         else:
            self.liststore.append([self.pixbuf_record_inactive, toogle_on, '', stlist[0], stlist[1], stlist[2], stlist[3]])


      for i, stlist in enumerate(self.pre_stationlist):
         i=i+len(self.stationlist)
         toogle_on=False
         if str(i) in self.settings['stations_toogle_on']:
            toogle_on=True
         self.liststore.insert_with_values(i, (0, 1, 2, 3, 4, 5, 6), (self.pixbuf_record_inactive, toogle_on, '', stlist[0], stlist[1], stlist[2], stlist[3]))





   def renderer_genre_edited(self, widget, row, text):

      self.log.debug('start row: %s text: %s len(self.stationlist): %s' % (row, text, len(self.stationlist)))

      row=int(row)
      self.liststore[row][3] = text
      self.stationlist[row][0] = text
      self.config['stations_changed']=True




   def renderer_stations_edited(self, widget, row, text):

      self.log.debug('start row: %s text: %s len(self.stationlist): %s' % (row, text, len(self.stationlist)))

      row=int(row)
      self.liststore[row][4] = text
      self.stationlist[row][1] = text
      self.config['stations_changed']=True



   def renderer_ripper_options_edited(self, widget, row, text):

      self.log.debug('start row: %s text: %s len(self.stationlist): %s' % (row, text, len(self.stationlist)))

      row=int(row)
      self.liststore[row][5] = text
      self.stationlist[row][2] = text
      self.config['stations_changed']=True




   def renderer_url_edited(self, widget, row, text):

      self.log.debug('start row: %s text: %s len(self.stationlist): %s' % (row, text, len(self.stationlist)))

      row=int(row)
      self.liststore[row][6] = text
      self.stationlist[row][3] = text
      self.config['stations_changed']=True



   def button_selectall_clicked(self, event):

      self.log.debug('start')

      self.settings['stations_toogle_on']=[]
      for i, item in enumerate(self.liststore):
         self.liststore[i][1] = True
         self.settings['stations_toogle_on'].extend([str(i)])



   def button_deselectall_clicked(self, event):

      self.log.debug('start')

      for i, item in enumerate(self.liststore):
         self.liststore[i][1] = False

      self.settings['stations_toogle_on'] = []



   def button_reset_clicked(self, event):

      self.log.debug('start')

      if os.path.exists('%s/%s' % (self.settings['config_path'],self.settings['filename_stations'])):
         os.remove('%s/%s' % (self.settings['config_path'],self.settings['filename_stations']))

      self.madmin.on_reset_close()



   def button_info_clicked(self, event):

      self.log.debug('start')

      url=['https://directory.shoutcast.com']

      dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                                 buttons=Gtk.ButtonsType.CLOSE,
                                 text='Get new stations from: %s' % ', '.join(url))

      dialog.set_modal(True)
      dialog.set_transient_for(self.madmin.win)
      dialog.set_title('Info')
      dialog.connect('response', self.on_dialog_response)
      dialog.show()



   def on_dialog_response(self, widget, response_id):
      if response_id == Gtk.ResponseType.CLOSE:
         widget.destroy()



   def timer_streamripper_stop(self, debug=True):
      if debug==True:
         self.log.debug('start')

      if self.obj_timer_streamripper is not None:
         GLib.source_remove(self.obj_timer_streamripper)
         self.obj_timer_streamripper=None



   def check_streamripper(self):

      self.log.debug('record_station: %s' % self.record_station)

      if not self.record_station:
         self.log.debug('stop')

         self.timer_streamripper_stop()

         self.record_status=False
         self.update_listmodel()
         return False


      for i, item in enumerate(self.liststore):
         if i in self.record_station:
            self.liststore[i][0]=self.pixbuf_record_active


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
                  self.liststore[int(identifier)][0]=self.pixbuf_record_inactive
                  self.record_station.remove(int(identifier))


      for pnum in remove_pnum:
         del self.madmin.process_database[pnum]

      return True




   def button_record_clicked(self, event):

      self.log.debug('start')

      toogle_on = []
      for i, item in enumerate(self.liststore):
         if self.liststore[i][1]==True:
            toogle_on.extend([i])

      if toogle_on:

         if self.obj_timer_streamripper is None:
            self.obj_timer_streamripper = GLib.timeout_add(1000, self.check_streamripper)

         if not os.path.exists(self.config['music_path'] + '/' + self.settings['directory_str']):
            os.mkdir(self.config['music_path'] + '/' + self.settings['directory_str'])


         self.update_listmodel()


         self.log.debug('record_station: %s' % self.record_station)

         for i in toogle_on:
            if not i in self.record_station:

               self.record_station.extend([i])
               self.record_status=True

               self.log.debug('toogle_on i: %s' % i)

               options_streamripper = self.liststore[i][5].split()

               # streamripper [URL] -u WinampMPEG/5.0 -d /Music/Streamripper/
               cmd = [self.config['bin_streamripper'], self.liststore[i][6], *options_streamripper, '-d', '%s/%s' % (self.config['music_path'],self.settings['directory_str'])]
               cwd = self.config['music_path'] + '/' + self.settings['directory_str']
               self.madmin.process_starter(cmd=cmd, cwd=cwd, job='streamripper', identifier=str(i), source=self.liststore[i][5])

         self.update_listmodel()


   def stop_ripper_process(self):
      self.log.debug('start')

      toogle_on = []
      for i, item in enumerate(self.liststore):
         if self.liststore[i][1]==True:
            toogle_on.extend([i])

      for i in toogle_on:
         self.madmin.process_job_identifier_killer(job='streamripper', identifier=str(i))

      


   def button_stop_clicked(self, event):

      self.log.debug('start')
      self.stop_ripper_process()



   def button_new_station_clicked(self, event):
      
      self.log.debug('start')
      station='New Station %s' % (len(self.stationlist)+1)

      self.liststore.insert(position=0, row=[self.pixbuf_record_inactive, False, 'list-remove', '', station, '', ''])
      self.stationlist.insert(0, ['', station ,'',''])

      self.settings['stations_toogle_on'] = []
      self.config['stations_changed']=True
      self.treeview.set_cursor(0)

