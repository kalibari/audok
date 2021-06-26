import os
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class TabAbout:

   def __init__(self, main, settings):
      self.main = main
      self.settings = settings

      self.box = Gtk.Box()
      self.box.set_border_width(10)
      #self.box.add(Gtk.Label('Default Page!'))

      if self.settings['Debug']==1:
         print ('def ABOUT_BUTTON - start')


      #############################
      box_outer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
      #box_outer = Gtk.WindowPosition.CENTER;


      label1 = Gtk.Label('Name: %s\nVersion: %s\nLicence: GNU GENERAL PUBLIC LICENSE Version 3\nCopyright: Copyright (c) 2018, kalibari\nWebSite: https://github.com/kalibari/audok' % (self.settings['Name'].upper(),self.settings['Version']), xalign=0)

      image3 = Gtk.Image()
      image3.set_from_file('%s/audok.png' % self.settings['Path'])

      image3.props.valign = Gtk.Align.CENTER


      box_outer.pack_start(label1, True, True, 0)

      box_outer.pack_start(image3, True, True, 0)
      self.box.add(box_outer)



      """
      info = wx.AboutDialogInfo()
      info.Name = self.settings['Name']
      info.Version = self.settings['Version']
      info.Licence = 'GNU GENERAL PUBLIC LICENSE Version 3\n'
      info.Icon = wx.Icon('%s/audok.ico' % self.settings['Path'] , wx.BITMAP_TYPE_ICO)
      info.Copyright = 'Copyright (c) 2017\nkalibari\n'
      info.Description = 'Music Player'
      info.WebSite = ("https://github.com/kalibari/audok", "Audok")
      wx.AboutBox(info)

      """
