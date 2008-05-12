#! /usr/bin/env python
# TuxTruck Main Frame - This is the root of everything, called from the App in main.py
# Time-stamp: "2008-05-12 10:24:37 jantman"
# $Id: TuxTruck_Main.py,v 1.1 2008-05-12 14:23:48 jantman Exp $ 
#
# Copyright 2008 Jason Antman. Licensed under GNU GPLv3 or latest version (at author's discretion).
# Jason Antman - jason@jasonantman.com - http://www.jasonantman.com
# Project web site at http://www.jasonantman.com/tuxtruck/

# application includes
from TuxTruck_Settings import * # import TuxTruck_Settings to get user settings
from TuxTruck_AudioPanel_Main import *
from TuxTruck_HomePanel_Clock import *

class TuxTruck_MainApp(wx.Frame):
    """
    This is the top-level frame/window/app for TuxTruck. It's the root of everything
    and everything happens (or is strated here). 
    This should just handle building the base GUI (blank main panel), and then instantiate
    child classes to do EVERYTHING else. Each part of the GUI should be its own class, that 
    holds a main panel and then does everything relating to that component (hopefully with 
    multiple child classes).
    NOTE: This should ONLY
      a) start the GUI, and init everything
      b) init TuxTruck_Settings to get user settings
      c) init any of the elements/categories that need to be constantly running (gps, phone, audio, obd)
      d) handle ALL of the communication/events that require interaction between categories, or
         require interrupts (GPS instructions, pop-ups, phone calls, etc.)
    """

    # variables holding state of the program
    _currentColorScheme = "day" # holds the name of the current color scheme
    _currentButton = "" # reference to the currently selected button, default to Home
    settings = TuxTruck_Settings()

    def __init__(self, parent, id):
        """
        This is the BIG function. It initiates EVERYTHING that gets initiated at start, 
        including settings, and all components that must run as long as the app is running.
        It SHOULD initiate GPS, Phone, and anything else that could take a while to start,
        as soon as possible.
        """
        wx.Frame.__init__(self, parent, id, '', style=wx.NO_BORDER) # init the main frame

        # setup the settings
        print "Loaded skin "+self.settings.skin.currentSkinName+" from file "+self.settings.skin.currentSkinFile

        # setup the main frame
        self.SetPosition(self.settings.skin.topWindowPos) # set the main window position
        self.SetSize(self.settings.skin.topWindowSize) # set the main window size
        if self.settings.skin.topWindowCentered == 1:
            # check whether to center the window or not
            self.CenterOnScreen()
        self.SetWindowStyle(wx.NO_BORDER) # set window style to have no border

        # create each of the buttons individually
        # NOTE: buttons must be explicitly added to SetButtonImages
        b_width = self.settings.skin.butn.width # button width
        b_height = self.settings.skin.butn.height # button height
        self.butn_home = wx.BitmapButton(self, size = (b_width, b_height))
        self.butn_gps = wx.BitmapButton(self, size = (b_width, b_height))
        self.butn_audio = wx.BitmapButton(self, size = (b_width, b_height))
        self.butn_obd = wx.BitmapButton(self, size = (b_width, b_height))
        self.butn_phone = wx.BitmapButton(self, size = (b_width, b_height))
        self.butn_tools = wx.BitmapButton(self, size = (b_width, b_height))
        self.butn_weather = wx.BitmapButton(self, size = (b_width, b_height))

        # set button images
        self.SetButtonImages(self._currentColorScheme)

        # TODO: how do we set the correct image for the active button?

        self.box = wx.BoxSizer(wx.HORIZONTAL) # TODO: give this a meaningful name
        self.box.Add(self.butn_home, proportion=0)
        self.box.Add(self.butn_gps, proportion=0)
        self.box.Add(self.butn_audio, proportion=0)
        self.box.Add(self.butn_obd, proportion=0)
        self.box.Add(self.butn_phone, proportion=0)
        self.box.Add(self.butn_tools, proportion=0)
        self.box.Add(self.butn_weather, proportion=0)

        self.SetAutoLayout(True)
        self.SetSizer(self.box)
        self.Layout()

        # DEBUG
        print self.box.GetSizeTuple()
        print self.box.GetPositionTuple()

        # bind each of the buttons to its' click handler
        self.butn_home.Bind(wx.EVT_BUTTON, self.OnClick_home)
        self.butn_gps.Bind(wx.EVT_BUTTON, self.OnClick_gps)
        self.butn_audio.Bind(wx.EVT_BUTTON, self.OnClick_audio)
        self.butn_obd.Bind(wx.EVT_BUTTON, self.OnClick_obd)
        self.butn_phone.Bind(wx.EVT_BUTTON, self.OnClick_phone)
        self.butn_tools.Bind(wx.EVT_BUTTON, self.OnClick_tools)
        self.butn_weather.Bind(wx.EVT_BUTTON, self.OnClick_weather)

        self._currentButton = self.butn_home # set butn_home to be our initial button

        # add main audio panel
        self.audioPanel_main = TuxTruck_AudioPanel_Main(self, -1)
        # add home clock panel
        # TODO: figure out how to skin this
        self.homePanel_clock = TuxTruck_HomePanel_Clock(self, -1)

        # now SET THE SKINS on EVERYTHING
        self.reSkin("day")
        
    def OnClick_gps(self, event):
        """ Handles click of the GPS button, switching to the GPS screen"""
        print "GPS clicked" # DEBUG
        self._currentButton = self.butn_gps

    def OnClick_audio(self, event):
        """ Handles click of the Audio button, switching to the audio screen (panel/frame)"""
        # TODO: update the docs for proper use of words application, window, panel, frame
        print "Audio clicked" # DEBUG
        self._currentButton = self.butn_audio
        self.switchToModePanel(self.audioPanel_main) # show the main audio panel

    def OnClick_home(self, event):
        """ Handles click of the home button, switching to the home screen"""
        print "Home clicked" # DEBUG
        self._currentButton = self.butn_home # update reference to current button
        # DEBUG - testing only since we only have one panel
        self.audioPanel_main.Hide()
        # TODO: what do we show at startup? default? selection from settings? last?
        self.homePanel_clock.Show()

    def OnClick_obd(self, event):
        """Handles click of the OBD button, switching to the OBD screen"""
        print "obd clicked" # DEBUG
        self._currentButton = self.butn_obd

    def OnClick_phone(self, event):
        """ Handles click of the phone button, switching to the phone screen"""
        print "phone clicked" # DEBUG
        self._currentButton = self.butn_phone

    def OnClick_tools(self, event):
        """Handles click of the tools button, switching to the tools screen"""
        print "tools clicked" # DEBUG
        self._currentButton = self.butn_tools
        self.switchColorScheme() # DEBUG

    def OnClick_weather(self, event):
        """Handles click of the weather button, switching to the weather screen"""
        print "weather clicked" # DEBUG
        self._currentButton = self.butn_weather

    def SetButtonImages(self, colorSchemeName):
        """
        This method sets the images of all of the buttons to the correct images
        for the selected color scheme (day/night within a specific skin). 
        """
        if colorSchemeName == "day":
            print "setting day button images" # DEBUG
            self.butn_home.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.day_home, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_gps.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.day_gps, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_audio.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.day_audio, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_obd.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.day_obd, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_phone.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.day_phone, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_tools.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.day_tools, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_weather.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.day_weather, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
        else:
            # set night images
            print "setting night button images" # DEBUG
            self.butn_home.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.night_home, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_gps.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.night_gps, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_audio.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.night_audio, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_obd.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.night_obd, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_phone.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.night_phone, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_tools.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.night_tools, wx.BITMAP_TYPE_ANY).ConvertToBitmap())
            self.butn_weather.SetBitmapLabel(wx.Image(self.settings.skin.buttonImagePath+self.settings.skin.butn.night_weather, wx.BITMAP_TYPE_ANY).ConvertToBitmap())

    def switchColorScheme(self):
        """
        This method does everything needed to toggle between day/night modes
        in the current skin
        """

        # DEBUG
        print "in main.py switching color scheme from "+self._currentColorScheme
        # END DEBUG
        
        if self._currentColorScheme == "day":
            self.reSkin("night")
        else:
            self.reSkin("day")


    def reSkin(self, colorSchemeName):
        if self._currentColorScheme == "day":
            # reskin myself
            self.SetBackgroundColour(self.settings.skin.night_bgColor) # reskin myself
            self.SetButtonImages("night")

            # reskin EVERYTHING else
            self.audioPanel_main.reSkin(self, "night")
            self.homePanel_clock.reSkin(self, "night")

            self._currentColorScheme = "night" # keep track of what skin I'm using now

        else:
            # reskin myself
            self.SetBackgroundColour(self.settings.skin.day_bgColor)
            self.SetButtonImages("day")

            # reskin EVERYTHING else
            self.audioPanel_main.reSkin(self, "day")
            self.homePanel_clock.reSkin(self, "day")

            self._currentColorScheme = "day" # keep track of what skin I'm using now

        # refresh myself
        self.Refresh()        
        
    def switchToModePanel(self, activePanel):
        """Hides all of the top-level mode panels and then shows the one we want"""
        # hide all of the top-level mode panels
        self.audioPanel_main.Hide()
        self.homePanel_clock.Hide()
        activePanel.Show()
