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

      self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

      label1 = Gtk.Label(label='Name: %s' % self.config['name'].title())
      label1.set_valign(Gtk.Align.CENTER)
      label1.set_margin_top(5)

      label2 = Gtk.Label(label='Version: %s' % self.config['version'])
      label2.set_valign(Gtk.Align.CENTER)

      image1 = Gtk.Image()
      image1.set_from_file('%s/audok_large.png' % self.config['app_path'])
      image1.set_pixel_size(300)
      image1.props.valign = Gtk.Align.CENTER


      label3 = Gtk.Label(label='Licence: GNU GENERAL PUBLIC LICENSE Version 3')
      label3.set_valign(Gtk.Align.CENTER)

      label4 = Gtk.Label(label='Copyright: Copyright (c) 2020 - 2021, kalibari')
      label4.set_valign(Gtk.Align.CENTER)

      label5 = Gtk.Label(label='WebSite: https://github.com/kalibari/audok')
      label5.set_valign(Gtk.Align.CENTER)
      label5.set_margin_bottom(5)

      self.box.append(label1)
      self.box.append(label2)
      self.box.append(image1)
      self.box.append(label3)
      self.box.append(label4)
      self.box.append(label5)
