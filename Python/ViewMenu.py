# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx
from IDTags  import *

def MakeViewMenu(self):
    viewMenu = wx.Menu()
    self.ShowStatusBar = viewMenu.Append(wx.ID_ANY, "Show status bar", 
        "Show Status bar", kind=wx.ITEM_CHECK)
    viewMenu.Check(self.ShowStatusBar.GetId(), True)
    self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.ShowStatusBar)
    self.IncreaseFont = viewMenu.Append(wx.ID_ANY, "Increase the font size\tCtrl+=", "Increase the font size")
    self.Bind(wx.EVT_MENU, self.OnIncreaseFontSize, self.IncreaseFont) 
    self.DecreaseFont = viewMenu.Append(wx.ID_ANY, "Decrease the font size\tCtrl+-", "Decrease the font size")
    self.Bind(wx.EVT_MENU, self.OnDecreaseFontSize, self.DecreaseFont) 
    self.ChooseFont = viewMenu.Append(wx.ID_ANY, "Choose font\tCtrl+D", "Choose the font size and other details")
    self.Bind(wx.EVT_MENU, self.OnSelectFont, self.ChooseFont )
    menuBar.Append(viewMenu, "View")  # Add the view Menu to the MenuBar

if __name__ == "__main__":
    MakeViewMenu(self)
