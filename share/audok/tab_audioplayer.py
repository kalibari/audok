import os
import re
import sys
import random
import threading
import signal
import time
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
gi.require_version('GLib', '2.0')
from gi.repository import GLib
gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

class TabAudioPlayer:


   def __init__(self, main, settings):

      self.main = main
      self.settings = settings


      ##################
      # initialize GStreamer
      Gst.init(None)

      self.state = Gst.State.NULL
      self.duration = None
      self.start_time_s = 0


      # PLAYBIN
      if self.settings['gst_player']=='playbin':

         self.player = Gst.ElementFactory.make("playbin", "player2")
         if not self.player:
            print('ERROR: Could not create player')
            sys.exit(1)

         # play only audio files
         fakesink = Gst.ElementFactory.make('fakesink', 'fakesink')
         self.player.set_property('video-sink', fakesink)

         self.player.connect("video-tags-changed", self.player_tag_changed)
         self.player.connect("audio-tags-changed", self.player_tag_changed)
         self.player.connect("text-tags-changed", self.player_tag_changed)

         bus = self.player.get_bus()
         bus.add_signal_watch()
         bus.enable_sync_message_emission()
         bus.connect("message::error", self.player_error)
         bus.connect("message::eos", self.player_eos)
         bus.connect("message::state-changed", self.player_state_changed)
         bus.connect("message::application", self.player_application_message)
         bus.connect('message::buffering', self.on_buffering)
         bus.connect("sync-message::element", self.on_sync_message)
   


      # Pipeline
      elif self.settings['gst_player']=='pipeline':

         self.player = Gst.Pipeline.new("player")
         if not self.player:
            print('ERROR: Could not create player')
            sys.exit(1)


         self.source = Gst.ElementFactory.make('filesrc', 'file-source')
         self.sink = Gst.ElementFactory.make('pulsesink','asink')
         self.conv = Gst.ElementFactory.make('audioconvert', 'audioconvert')
         self.queue = Gst.ElementFactory.make('queue', 'queue')
         #self.audioresample = Gst.ElementFactory.make('audioresample', 'audioresample')
         #self.inputselector = Gst.ElementFactory.make('input-selector', 'input-selector')
         #self.streamsynchronizer = Gst.ElementFactory.make('streamsynchronizer', 'streamsynchronizer')
         #self.identity = Gst.ElementFactory.make('identity', 'identity')
         #self.tee = Gst.ElementFactory.make('tee', 'tee')

         #self.mad_decoder = Gst.ElementFactory.make('mad', 'mad')
         #self.mp3_demuxer = Gst.ElementFactory.make('id3demux', 'id3demux')
         #self.mp3v2_demuxer = Gst.ElementFactory.make('id3v2mux', 'id3v2mux')
         #self.mp3v2_demuxer.connect('pad-added', self.mp3v2_demuxer_callback)
         #self.ogg_demuxer = Gst.ElementFactory.make('oggdemux', 'oggdemux')
         #self.ogg_demuxer.connect('pad-added', self.ogg_demuxer_callback)
   
         self.lame_decoder = Gst.ElementFactory.make('lamemp3enc', 'lamemp3enc')
         #self.lame_decoder.set_property('quality', 0)
         self.mpg123_decoder = Gst.ElementFactory.make('mpg123audiodec', 'mpg123audiodec')
         self.vorbis_decoder = Gst.ElementFactory.make('vorbisdec','vorbisdec')

         #self.decodebin = Gst.ElementFactory.make('decodebin', 'decodebin')
         #self.mpegaudioparse = Gst.ElementFactory.make('mpegaudioparse', 'mpegaudioparse')


         #self.player.add(self.audioresample)
         self.player.add(self.queue)
         #self.player.add(self.mpegaudioparse)

         #self.player.add(self.ogg_demuxer)
         #self.player.add(self.mp3v2_demuxer)
         self.player.add(self.source)
         #self.player.add(self.mad_decoder)
         self.player.add(self.lame_decoder)
         self.player.add(self.vorbis_decoder)
         #self.player.add(self.decodebin)
         self.player.add(self.conv)
         self.player.add(self.sink)
         #self.player.add(self.inputselector)
         #self.player.add(self.streamsynchronizer)
         #self.player.add(self.identity)
         #self.player.add(self.tee)
         #self.player.add(self.mp3_demuxer)


         #self.source.link(self.mad_decoder)
         #self.source.link(self.lame_decoder)
         self.source.link(self.mpg123_decoder)
         #self.source.link(self.decodebin)
         #self.source.link(self.mpegaudioparse)
         #self.source.link(self.inputselector)
         #self.source.link(self.streamsynchronizer)
         #self.source.link(self.identity)
         #self.source.link(self.tee)
         #self.source.link(self.mp3_demuxer)

         self.conv.link(self.sink)
         #self.mad_decoder.link(self.conv)
         self.vorbis_decoder.link(self.conv)
         #self.lame_decoder.link(self.conv)
         #self.decodebin.link(self.conv)


         bus = self.player.get_bus()
         bus.add_signal_watch()
         bus.connect("message::error", self.player_error)
         bus.connect("message::eos", self.player_eos)
         bus.connect("message::state-changed", self.player_state_changed)
         bus.connect("message::application", self.player_application_message)
         bus.connect('message::info', self.on_info)
         bus.connect('message::buffering', self.on_buffering)
 

   def init_gui(self, playlist):

      self.playlist = playlist

      self.box = Gtk.Box()
      self.box.set_border_width(10)


      #############################
      box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

      row1 = Gtk.ListBoxRow()
      hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row1.add(hbox1)


      label1 = Gtk.Label("Play Time", xalign=0)
      self.combo_play_time = Gtk.ComboBoxText()
      choice_play_time=self.settings['Choice_Play_Time']
      for i,item in enumerate(choice_play_time):
         self.combo_play_time.insert(i, "%s" %i, "%s" % item)
      self.combo_play_time.connect("changed", self.PLAY_TIME_COMBOBOX)
      self.combo_play_time.set_active(0)


      label2 = Gtk.Label("Random Start", xalign=0)
      self.combo_random = Gtk.ComboBoxText()
      choice_random_time=self.settings['Choice_Random_Time']
      for i,item in enumerate(choice_random_time):
         self.combo_random.insert(i, "%s" % item, "%s" % item) 
      self.combo_random.connect("changed", self.RANDOM_COMBOBOX)
      self.combo_random.set_active(0)


      image3 = Gtk.Image()
      image3.set_from_file('%s/loop_small.png' % self.settings['Share_Path'])
      self.checkbutton_loop = Gtk.CheckButton()

      image4 = Gtk.Image()
      image4.set_from_file('%s/auto_olddir_small.png' % self.settings['Share_Path'])
      self.checkbutton_auto_move = Gtk.CheckButton()

      button5 = Gtk.Button(label="Scan")
      button5.connect("clicked", self.SCAN_BUTTON)


      image6 = Gtk.Image()
      image6.set_from_file('%s/streamripperdir_small.png' % self.settings['Share_Path'])
      self.checkbutton_str = Gtk.CheckButton()
      self.checkbutton_str.set_active(1)


      image7 = Gtk.Image()
      image7.set_from_file('%s/newdir_small.png' % self.settings['Share_Path'])
      self.checkbutton_new = Gtk.CheckButton()

      image8 = Gtk.Image()
      image8.set_from_file('%s/olddir_small.png' % self.settings['Share_Path'])
      self.checkbutton_old = Gtk.CheckButton()


      self.entry_file_sum = Gtk.Entry()
      self.entry_file_sum.set_text("")


      hbox1.pack_start(label1, False, False, 0)
      hbox1.pack_start(self.combo_play_time, False, False, 0)
      hbox1.pack_start(label2, False, False, 0)
      hbox1.pack_start(self.combo_random, False, False, 0)
      hbox1.pack_start(image3, False, False, 0)
      hbox1.pack_start(self.checkbutton_loop, False, False, 0)
      hbox1.pack_start(image4, False, False, 0)
      hbox1.pack_start(self.checkbutton_auto_move, False, False, 0)
      hbox1.pack_start(button5, False, False, 0)
      hbox1.pack_start(image6, False, False, 0)
      hbox1.pack_start(self.checkbutton_str, False, False, 0)
      hbox1.pack_start(image7, False, False, 0)
      hbox1.pack_start(self.checkbutton_new, False, False, 0)
      hbox1.pack_start(image8, False, False, 0)
      hbox1.pack_start(self.checkbutton_old, False, False, 0)
      hbox1.pack_start(self.entry_file_sum, False, False, 0)


      #############################
      row2 = Gtk.ListBoxRow()
      hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row2.add(hbox2)


      image2 = Gtk.Image()
      image2.set_from_file('%s/back_white.png' % self.settings['Share_Path'])
      self.button_back = Gtk.Button()
      self.button_back.connect("clicked", self.BACK_BUTTON)
      self.button_back.set_image(image2)


      image3 = Gtk.Image()
      image3.set_from_file('%s/play_white.png' % self.settings['Share_Path'])
      self.button_play = Gtk.Button()
      self.button_play.connect("clicked", self.PLAY_BUTTON)
      self.button_play.set_image(image3)

      image4 = Gtk.Image()
      image4.set_from_file('%s/pause_white.png' % self.settings['Share_Path'])
      self.button_pause = Gtk.Button()
      self.button_pause.connect("clicked", self.PAUSE_BUTTON)
      self.button_pause.set_image(image4)

      image5 = Gtk.Image()
      image5.set_from_file('%s/next_white.png' % self.settings['Share_Path'])


      self.button_next = Gtk.Button()
      self.button_next.connect("clicked", self.NEXT_BUTTON)
      self.button_next.set_image(image5)


      image6 = Gtk.Image()
      image6.set_from_file('%s/olddir.png' % self.settings['Share_Path'])
      self.button_move_old = Gtk.Button()
      self.button_move_old.connect("clicked", self.MOVE_OLD_BUTTON)
      self.button_move_old.set_image(image6)

      image7 = Gtk.Image()
      image7.set_from_file('%s/newdir.png' % self.settings['Share_Path'])
      self.button_move_new = Gtk.Button()
      self.button_move_new.connect("clicked", self.MOVE_NEW_BUTTON)
      self.button_move_new.set_image(image7)


      hbox2.pack_start(self.button_back, False, False, 0)
      hbox2.pack_start(self.button_play, False, False, 0)
      hbox2.pack_start(self.button_pause, False, False, 0)
      hbox2.pack_start(self.button_next, False, False, 0)
      hbox2.pack_start(self.button_move_old, False, False, 0)
      hbox2.pack_start(self.button_move_new, False, False, 0)



      #############################
      row3 = Gtk.ListBoxRow()
      hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row3.add(hbox3)

      self.h_scale1 = Gtk.HScale.new_with_range(0, 300, 1)
      self.h_scale1.set_digits(0)
      self.h_scale1.set_hexpand(True)
      self.h_scale1_update = self.h_scale1.connect("value-changed", self.slider_change)



      hbox3.pack_start(self.h_scale1, True, True, 0)


      #############################
      row4 = Gtk.ListBoxRow()
      hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row4.add(hbox4)

      label1 = Gtk.Label("Play File")
      self.label_play_file = Gtk.Label("")

      self.infobar_play_file = Gtk.InfoBar()
      #self.infobar_play_file.connect("response", self.on_infobar_response)
      self.infobar_play_file.add(self.label_play_file)
 

      hbox4.pack_start(label1, False, False, 0)
      hbox4.pack_start(self.infobar_play_file, False, False, 0)


      #############################
      row5 = Gtk.ListBoxRow()
      hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
      row5.add(hbox5)


      #textview1 = Gtk.TextView.new()
      #textview1.set_editable(False)


      columns = ["Num",
                 "Filename"]

      self.scrolledwindow1 = Gtk.ScrolledWindow()
      self.listmodel1 = Gtk.ListStore(str, str)

      treeview1 = Gtk.TreeView(model=self.listmodel1)

      for i, column in enumerate(columns):
         cell = Gtk.CellRendererText()
         col = Gtk.TreeViewColumn(column, cell, text=i)
         treeview1.append_column(col)


      #treeview1.get_selection().connect("changed", self.treeview_selection_changed)
      treeview1.connect('size-allocate', self.treeview_size_changed)


      treeview1.set_property('rules-hint', True)  # Zeilenfarbe wechselnd
      self.scrolledwindow1.add(treeview1)


      hbox5.pack_start(self.scrolledwindow1, True, True, 0)


      #self.statusbar1 = Gtk.Statusbar()
      #self.context_id = self.statusbar1.get_context_id("status")
      #self.statusbar1.push(self.context_id, "Der Ordner wurde noch nicht eingelesen.")
      #hbox5.pack_start(self.statusbar1, True, True, 0)


      box_outer.pack_start(row1, False, False, 2)
      box_outer.pack_start(row2, False, False, 2)
      box_outer.pack_start(row3, True, True, 0)
      box_outer.pack_start(row4, False, False, 0)
      box_outer.pack_start(row5, True, True, 2)
      self.box.add(box_outer)

      ###################################################################################


      if len(self.playlist)==0:
         self.button_next.set_sensitive(False)
         self.button_back.set_sensitive(False)
         self.button_play.set_sensitive(False)
         self.button_pause.set_sensitive(False)



   def on_message(self, bus, message):
      t = message.type
      if t == Gst.MessageType.EOS:
         #logger.debug("Received EOS, setting pipeline to NULL.")
         self.player.set_state(Gst.State.NULL)
         #logger.debug("Emitting flush-done.")
         self.emit("flush-done")
      elif t == Gst.MessageType.ERROR:
         print ("Received an error message: %s", message.parse_error()[1])
         pass



   def slider_change(self, range):
      value = self.h_scale1.get_value()

      if self.settings['Debug']==1:
         print('def slider_change - value: %s' % value)

      self.player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, value * Gst.SECOND)
      #self.player.seek_simple(Gst.Format.TIME,Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT, value * Gst.SECOND)




   def ogg_demuxer_callback(self, demuxer, pad):
      adec_pad = self.ogg_decoder.get_static_pad("sink")
      pad.link(adec_pad)


   def mp3v2_demuxer_callback(self, demuxer, pad):
      adec_pad = self.mad_decoder.get_static_pad("sink")
      pad.link(adec_pad)



   def player_tag_changed(self, player, stream):
      if self.settings['Debug']==1:
         print('def player_tag_changed - start')

      self.player.post_message(Gst.Message.new_application(self.player,Gst.Structure.new_empty("tags-changed")))



   def on_buffering(self, player, stream):
      if self.settings['Debug']==1:
         print('def on_buffering - start')


   def on_sync_message(self, bus, message):
      if self.settings['Debug']==1:
         print('def on_sync_message - start')



   def refresh_slider(self):

      if self.state == Gst.State.NULL or self.state == Gst.State.READY or self.state == Gst.State.PAUSED:
         return True

      else:

         if self.duration is None:

            ret, drt = self.player.query_duration(Gst.Format.TIME)
            if ret:
               self.duration=drt
               set_range = self.duration / Gst.SECOND
               if self.settings['Debug']==1:
                  print('def refresh_slider - set range: %s' % set_range)

               self.h_scale1.set_range(0, set_range)
            else:
               self.h_scale1.set_range(0, 300)
               self.h_scale1.set_value(self.start_time_s)


         else:

            ret, drt = self.player.query_position(Gst.Format.TIME)
            if ret:

               set_slider = drt / Gst.SECOND
               self.h_scale1.handler_block(self.h_scale1_update)
               self.h_scale1.set_value(set_slider)
               self.h_scale1.handler_unblock(self.h_scale1_update)

         return True




   def player_error(self, bus, msg):
      if self.settings['Debug']==1:
         print('player_error - start')

      err, dbg = msg.parse_error()
      if self.settings['Debug']==1:
         print("ERROR:", msg.src.get_name(), ":", err.message)






   def player_eos(self, bus, msg):
      if self.settings['Debug']==1:
         print('player_eos - start')

      if self.checkbutton_auto_move.get_active():
         self.move_old()

      self.player.set_state(Gst.State.READY)

      if self.checkbutton_loop.get_active():
         self.choose_song(choose='keep')
      elif len(self.playlist)>=2:
         self.choose_song(choose='next')



   def on_info(self, bus, message):
      print('info message -> {}'.format(message))



   def player_state_changed(self, bus, msg):

      (old, new, pending) = msg.parse_state_changed()

      if msg.src == self.player:

         if self.settings['Debug']==1:
            print('def player_state_changed old: %s new: %s' % (old,new))

         self.state = new


         if old == Gst.State.PAUSED and new == Gst.State.PLAYING:
            if self.settings['Debug']==1:
               print('def player_state_changed refresh slider (play/back/next button + random start)')
            # refresh slider as soons as possible
            self.refresh_slider()


      else:

         #if self.settings['Debug']==1:
         #   print('def player_state_changed msg.src: %s' % msg.src)


         """
         def player_state_changed player_style: playbin msg.src: <__gi__.GstPlaySinkAudioConvert object at 0x7f87bf77c480 (GstPlaySinkAudioConvert at 0x55ff2f825020)>
         def player_state_changed player_style: playbin msg.src: <Gst.Bin object at 0x7f87bf77c480 (GstBin at 0x7f87a004e090)>
         def player_state_changed player_style: playbin msg.src: <__gi__.GstPlaySink object at 0x7f87bf77c480 (GstPlaySink at 0x55ff2f576210)>
         def player_state_changed player_style: playbin msg.src: <__gi__.GstTypeFindElement object at 0x7f87bf77c4c8 (GstTypeFindElement at 0x55ff2f784990)>
         def player_state_changed player_style: playbin msg.src: <__gi__.GstDecodeBin object at 0x7f87bf77c4c8 (GstDecodeBin at 0x55ff2fb5a1e0)>
         def player_state_changed player_style: playbin msg.src: <__gi__.GstURIDecodeBin object at 0x7f87bf77c4c8 (GstURIDecodeBin at 0x55ff2f9449f0)>
         """
         pass



   # extract metadata from all the streams and write it to the text widget
   # in the GUI
   def analyze_streams(self):

      if self.settings['Debug']==1:
         print('def analyze_streams - start')


      # clear current contents of the widget
      #buffer = self.streams_list.get_buffer()
      #buffer.set_text("")

      # read some properties
      nr_audio = self.player.get_property("n-audio")
      nr_text = self.player.get_property("n-text")


      """
      for i in range(nr_audio):
         tags = None
         # retrieve the stream's audio tags
         tags = self.player.emit("get-audio-tags", i)
         if tags:
            buffer.insert_at_cursor("\naudio stream {0}\n".format(i))
            ret, str = tags.get_string(Gst.TAG_AUDIO_CODEC)
            if ret:
               buffer.insert_at_cursor(
                 "  codec: {0}\n".format(
                     str or "unknown"))

            ret, str = tags.get_string(Gst.TAG_LANGUAGE_CODE)
            if ret:
               buffer.insert_at_cursor(
                 "  language: {0}\n".format(
                     str or "unknown"))

            ret, str = tags.get_uint(Gst.TAG_BITRATE)
            if ret:
               buffer.insert_at_cursor(
                 "  bitrate: {0}\n".format(
                     str or "unknown"))

      for i in range(nr_text):
         tags = None
         # retrieve the stream's subtitle tags
         tags = self.player.emit("get-text-tags", i)
         if tags:
            buffer.insert_at_cursor("\nsubtitle stream {0}\n".format(i))
            ret, str = tags.get_string(Gst.TAG_LANGUAGE_CODE)
            if ret:
               buffer.insert_at_cursor(
                 "  language: {0}\n".format(
                     str or "unknown"))
      """



   # this function is called when an "application" message is posted on the bus
   # here we retrieve the message posted by the player_tag_changed callback
   def player_application_message(self, bus, msg):

      if self.settings['Debug']==1:
         print('def player_application_message - start')

      if msg.get_structure().get_name() == "tags-changed":
          # if the message is the "tags-changed", update the stream info in
          # the GUI
          self.analyze_streams()



   # this function is called when new metadata is discovered in the stream
   def player_tag_changed(self, player, stream):
      # we are possibly in a GStreamer working thread, so we notify
      # the main thread of this event through a message in the bus

      if self.settings['Debug']==1:
         print('def player_tag_changed - start')


      self.player.post_message(
          Gst.Message.new_application(
              self.player,
              Gst.Structure.new_empty("tags-changed")))


      
   def play_timer_stop(self):
      if hasattr(self, 't'):
         if self.t.is_alive():
            if self.settings['Debug']==1:
               print ('def play_timer_stop - cancel')
            self.t.cancel()



   def play_timer_end(self):
      if self.settings['Debug']==1:
         print ('def play_timer_end - start')

      if self.checkbutton_auto_move.get_active():
         self.move_old()

      os.kill(self.settings['Pid'], signal.SIGUSR2)



   def play_timer_start(self):
      if self.settings['Debug']==1:
         print ('def play_timer_start - start with play_time: %s' % self.settings['Play_Time'])

      self.play_timer_stop()
      self.t = threading.Timer(int(self.settings['Play_Time']), self.play_timer_end)
      self.t.start()




   def playlist_filescan(self):

      if self.settings['Debug']==1:
         print ('def playlist_filescan - start')


      allfiles = set()

      if self.checkbutton_new.get_active()==True:

         if self.settings['Debug']==1:
            print ('def playlist_filescan - scan dir: %s/%s' % (self.settings['Music_Path'],self.settings['Directory_New']))

         for root, dirs, files in os.walk(self.settings['Music_Path'] + '/' + self.settings['Directory_New']):
            for item in files:
               if re.search('^%s/%s' % (self.settings['Music_Path'],self.settings['Directory_Old']), root):
                  pass
               elif re.search('^%s/%s' % (self.settings['Music_Path'],self.settings['Directory_Streamripper']), root):
                  pass
               else:
                  allfiles.add('%s/%s' % (root,item))



      if self.checkbutton_old.get_active()==True:

         if self.settings['Debug']==1:
            print ('def playlist_filescan - scan dir: %s/%s' % (self.settings['Music_Path'],self.settings['Directory_Old']))

         for root, dirs, files in os.walk(self.settings['Music_Path'] + '/' + self.settings['Directory_Old']):
            for item in files:
               if re.search('^%s/%s' % (self.settings['Music_Path'],self.settings['Directory_New']), root):
                  pass
               elif re.search('^%s/%s' % (self.settings['Music_Path'],self.settings['Directory_Streamripper']), root):
                  pass
               else:
                  allfiles.add('%s/%s' % (root,item))



      if self.checkbutton_str.get_active()==True:

         if self.settings['Debug']==1:
            print ('def playlist_filescan - scan dir: %s/%s' % (self.settings['Music_Path'],self.settings['Directory_Streamripper']))

         for root, dirs, files in os.walk(self.settings['Music_Path'] + '/' + self.settings['Directory_Streamripper']):
            for item in files:
               if re.search('^%s/%s' % (self.settings['Music_Path'],self.settings['Directory_Old']), root):
                  pass
               elif re.search('^%s/%s' % (self.settings['Music_Path'],self.settings['Directory_New']), root):
                  pass
               elif 'incomplete' in root:
                  pass
               else:
                  allfiles.add('%s/%s' % (root,item))


      # reverse
      allfiles=list(allfiles)
      allfiles=allfiles[::-1]

      # reset
      self.playlist = []

      for item in allfiles:
         self.playlist.extend([item])


      self.button_next.set_sensitive(False)
      self.button_back.set_sensitive(False)
      if len(self.playlist)>=1:
         self.label_play_file.set_text('%s - %s' % ((self.settings['Play_Num']+1),self.playlist[self.settings['Play_Num']]))


      if self.settings['Debug']==1:
         print ('def playlist_filescan - len(playlist): %s' % len(self.playlist))





   def choose_song(self, choose='next'):

      self.duration=None

      len_playlist = len(self.playlist)


      if self.settings['Debug']==1:
         print ('def choose_song - start choose %s len_playlist: %s play_num: %s' % (choose,len_playlist,self.settings['Play_Num']))



      if choose=='next' and (self.settings['Play_Num']+1)>=len_playlist:
         if self.settings['Debug']==1:
            print ('def choose_song last file -> rescan')
         self.playlist_filescan()
         self.settings['Play_Num']=0

      elif choose=='back' and self.settings['Play_Num']<=0:
         if self.settings['Debug']==1:
            print ('def choose_song - goto last file')
         self.playlist_filescan()
         self.settings['Play_Num']=(len_playlist-1)

      elif choose=='next':
         self.settings['Play_Num']+=1

      elif choose=='back':
         self.settings['Play_Num']-=1

      elif choose=='keep':
         pass



      # change scrolled window
      if len_playlist>0:
         adj = self.scrolledwindow1.get_vadjustment()
         upper_size = adj.get_upper()
         page_size = adj.get_page_size()
         set_size = (upper_size / len_playlist) * self.settings['Play_Num']
         if self.settings['Debug']==1:
            print ('def choose_song set_size: %s play_num: %s upper_size: %s page_size: %s' % (set_size,self.settings['Play_Num'],upper_size,page_size))
         adj.set_value(set_size)


      self.play_file()




   def play_file(self, newplaylist=[]):

      if self.settings['Debug']==1:
         print ('def play_file start - newplaylist: %s' % newplaylist)


      if not hasattr(self, 'glib_timer_refresh_slider'):
         self.glib_timer_refresh_slider = GLib.timeout_add_seconds(1, self.refresh_slider)


      if newplaylist:
         self.settings['Play_Num'] = 0
         self.playlist = list(newplaylist)


      if len(self.playlist)==1:
         self.play_timer_stop()
         self.button_next.set_sensitive(False)
         self.button_back.set_sensitive(False)


      elif len(self.playlist)>1:
         self.button_next.set_sensitive(True)
         self.button_back.set_sensitive(True)


      if self.settings['Debug']==1:
         print ('def play_file play_num: %s state: %s len(self.playlist): %s' % (self.settings['Play_Num'],self.state,len(self.playlist)))


      if self.state == Gst.State.PAUSED:
         pass
      else:

         self.entry_file_sum.set_text('%s' % len(self.playlist))
         self.player.set_state(Gst.State.NULL)

         if len(self.playlist)==0:
            self.label_play_file.set_text('')

         elif len(self.playlist)>=1:

            filepath = os.path.realpath(self.playlist[self.settings['Play_Num']])

            if self.settings['gst_player']=='playbin':
               self.player.set_property("uri", "file://%s" % self.playlist[self.settings['Play_Num']])
            elif self.settings['gst_player']=='pipeline':
               self.player.get_by_name('file-source').set_property("location", filepath)
            self.label_play_file.set_text('%s - %s' % ((self.settings['Play_Num']+1),self.playlist[self.settings['Play_Num']]))



      if len(self.playlist)>=1:

         if self.settings['Debug']==1:
           print ('def play_file start playing')


         self.button_pause.set_sensitive(True)

         self.start_time_s = 0

         if self.settings['Random_Time']!='0':
            self.player.set_state(Gst.State.PAUSED)

            (random_t1,random_t2) = self.settings['Random_Time'].split('-')
            if self.settings['Debug']==1:
               print ('def play_file random_t1: %s random_t1: %s' % (random_t1,random_t2))
            self.start_time_s=random.randint(int(random_t1),int(random_t2))
            if self.settings['Debug']==1:
               print ('def play_file - start-time: %s s' % self.start_time_s)

            time.sleep(0.5)
            self.player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, self.start_time_s * Gst.SECOND)

         self.player.set_state(Gst.State.PLAYING)

         if self.settings['Debug']==1:
            print ('def play_file set state: Gst.State.PLAYING')





   def pause(self):
      if self.settings['Debug']==1:
         print ('def pause start')

      self.play_timer_stop()
      self.player.set_state(Gst.State.PAUSED)




   def move_old(self):

      play_num = self.settings['Play_Num']
      path_filename = self.playlist[self.settings['Play_Num']]

      if self.settings['Debug']==1:
         print ('def move_old - start - play_num: %s path_filename: %s' % ((self.settings['Play_Num']+1),path_filename))

      self.listmodel1.clear()

      try:
         filename = os.path.basename(path_filename)
         if not os.path.exists(self.settings['Music_Path'] + '/' + self.settings['Directory_Old']):
            os.mkdir(self.settings['Music_Path'] + '/' + self.settings['Directory_Old'])
         os.rename(path_filename,'%s/%s/%s' % (self.settings['Music_Path'],self.settings['Directory_Old'],filename))
         self.playlist_filescan()
      except Exception as e:
         if self.settings['Debug']==1:
            print ('def move_old error: %s' % str(e))


      for i,item in enumerate(self.playlist):
         i+=1
         self.listmodel1.append([str(i),str(item)])




   def move_new(self):
      if self.settings['Debug']==1:
         print ('def move_new - start')

      filename = os.path.basename(self.playlist[self.settings['Play_Num']])
      try:
         if not os.path.exists(self.settings['Music_Path'] + '/' + self.settings['Directory_New']):
            os.mkdir(self.settings['Music_Path'] + '/' + self.settings['Directory_New'])
         os.rename(self.playlist[self.settings['Play_Num']], '%s/%s/%s' % (self.settings['Music_Path'],self.settings['Directory_New'],filename))
         self.playlist_filescan()
      except Exception as e:
         if self.settings['Debug']==1:
            print ('def move_new error: %s' % str(e))




   def treeview_size_changed(self, event1, event2):
      #if self.settings['Debug']==1:
      #   print ('def treeview_size_changed start')
      pass





   ###### COMBOBOX ######
   def PLAY_TIME_COMBOBOX(self, event):
      if self.settings['Debug']==1:
         print ('def combo_play_time - start - active_text: %s' % event.get_active_text())
      self.settings['Play_Time'] = event.get_active_text()

      if int(self.settings['Play_Time'])==0:
         self.play_timer_stop()
      else:
         if self.state == Gst.State.PLAYING:
            self.play_timer_start()



   def RANDOM_COMBOBOX(self, event):
      if self.settings['Debug']==1:
         print ('def RANDOM_COMBOBOX - start - active_text: %s' % event.get_active_text())
      self.settings['Random_Time'] = event.get_active_text()




   ###### BUTTON ######
   def SCAN_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def SCAN_BUTTON - start')

      self.settings['Play_Num'] = 0

      self.listmodel1.clear()

      self.play_timer_stop()


      # set state to Ready
      if self.state == Gst.State.PLAYING:
         if self.settings['Debug']==1:
            print ('def SCAN_BUTTON - try to set state: %s' % Gst.State.PAUSED)
         self.player.set_state(Gst.State.PAUSED)
         if self.settings['Debug']==1:
            print ('def SCAN_BUTTON - try to set state: %s' % Gst.State.READY)
         self.player.set_state(Gst.State.READY)


      elif self.state == Gst.State.PAUSED:
         if self.settings['Debug']==1:
            print ('def SCAN_BUTTON - try to set state: %s' % Gst.State.READY)
         self.player.set_state(Gst.State.READY)


      self.playlist_filescan()

      self.entry_file_sum.set_text(str(len(self.playlist)))

      if len(self.playlist)>=1:
         self.checkbutton_auto_move.set_sensitive(True)
         self.checkbutton_loop.set_sensitive(True)
         self.button_play.set_sensitive(True)

         for i,item in enumerate(self.playlist):
            i+=1
            self.listmodel1.append([str(i),str(item)])





   def PLAY_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def PLAY_BUTTON - start')
      self.button_play.set_sensitive(False)
      self.play_file()



   def NEXT_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def NEXT_BUTTON - start')
      self.choose_song(choose='next')


   def BACK_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def BACK_BUTTON - start')
      self.choose_song(choose='back')



   def PAUSE_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def PAUSE_BUTTON - start')
      self.pause()

      self.button_pause.set_sensitive(False)
      self.button_play.set_sensitive(True)
      self.button_back.set_sensitive(False)
      self.button_next.set_sensitive(False)



   def MOVE_OLD_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def MOVE_OLD_BUTTON start')
      self.move_old()
      self.choose_song(choose='keep')



   def MOVE_NEW_BUTTON(self, event):
      if self.settings['Debug']==1:
         print ('def MOVE_NEW_BUTTON start')
      self.move_new()
      self.choose_song(choose='keep')

