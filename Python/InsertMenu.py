# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx
from MarkdownEvents import *
import MarkdownEvents 

def MakeInsertMenu(self, MainMenu):
        insertMenu = wx.Menu()
        AddHeadBlock = insertMenu.Append(-1, "header/preamble\tCtrl+Shift+H")
        self.Bind(wx.EVT_MENU, OnAddHeadBlock, AddHeadBlock)
        AddURL = insertMenu.Append(-1, "URL\tCtrl+Shift+U")
        self.Bind(wx.EVT_MENU, OnAddURL, AddURL)
        AddEMail = insertMenu.Append(-1, "e-mail\tCtrl+Shift+E")
        self.Bind(wx.EVT_MENU, OnAddEMail, AddEMail)
        AddFigure = insertMenu.Append(-1, "Figure\tCtrl+Shift+F")
        self.Bind(wx.EVT_MENU, OnAddFigure, AddFigure)
        AddReference = insertMenu.Append(-1, "Reference\tCtrl+Shift+R")
        self.Bind(wx.EVT_MENU, OnAddReference, AddReference)
        headingsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_H1, "level &1\tAlt+1", "insert heading level 1", OnHeading1), 
                 (ID_H2, "level &2\tAlt+2", "insert heading level 2", OnHeading2), 
                 (ID_H3, "level &3\tAlt+3", "insert heading level 3", OnHeading3), 
                 (ID_H4, "level &4\tAlt+4", "insert heading level 4", OnHeading4), 
                 (ID_H5, "level &5\tAlt+5", "insert heading level 5", OnHeading5), 
                 (ID_H6, "level &6\tAlt+6", "insert heading level 6", OnHeading6)]:
            if id == None:
                headingsMenu.AppendSeparator()
            else:
                item = headingsMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        insertMenu.Append(-1, "Heading", headingsMenu)
        MainMenu.Append(insertMenu, "Insert")  # Add the Insert Menu to the MenuBar

