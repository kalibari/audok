import os
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class TabAbout:

   def __init__(self, main, config, settings):

      self.main = main
      self.config = config
      self.settings = settings

      self.box = Gtk.Box()
      self.box.set_border_width(10)

      if self.config['debug']==1:
         print ('def acout - start')


      #############################
      box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

      label1 = Gtk.Label('Name: %s\nVersion: %s\nLicence: GNU GENERAL PUBLIC LICENSE Version 3\nCopyright: Copyright (c) 2021, kalibari\nWebSite: https://github.com/kalibari/audok' % (self.config['name'].upper(),self.config['version']), xalign=0)

      image3 = Gtk.Image()
      image3.set_from_file('%s/audok_large.png' % self.config['app_path'])

      image3.props.valign = Gtk.Align.CENTER


      box_outer.pack_start(label1, True, True, 0)

      box_outer.pack_start(image3, True, True, 0)
      self.box.add(box_outer)


