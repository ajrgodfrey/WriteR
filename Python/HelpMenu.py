# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx
import HelpMenuEvents 


def MakeHelpMenu(self, MainMenu):
        helpMenu = wx.Menu()
        for id, label, helpText, handler in \
                [(wx.ID_ABOUT, "About", "Information about this program", HelpMenuEvents .OnAbout)]:
            if id == None:
                helpMenu.AppendSeparator()
            else:
                item = helpMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        MainMenu.Append(helpMenu, "&Help")  # Add the helpMenu to the MenuBar
