import os
import re
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class TabAbout:

   def __init__(self, madmin, log, config, settings):

      self.madmin = madmin
      self.log = log
      self.config = config
      self.settings = settings

      self.log.debug('start')

      self.box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)

      label1 = Gtk.Label(label='Name: %s\nVersion: %s\nLicence: GNU GENERAL PUBLIC LICENSE Version 3\nCopyright: Copyright (c) 2020 - 2021, kalibari\nWebSite: https://github.com/kalibari/audok' % (self.config['name'].title(),self.config['version']))
      label1.set_margin_start(5)
      label1.set_xalign(0)

      image3 = Gtk.Image()
      image3.set_from_file('%s/audok_large.png' % self.config['app_path'])
      image3.set_pixel_size(300)

      image3.props.valign = Gtk.Align.CENTER

      self.box.append(label1)
      self.box.append(image3)

