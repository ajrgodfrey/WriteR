# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx

        insertMenu = wx.Menu()
        AddHeadBlock = insertMenu.Append(-1, "header/preamble\tCtrl+Shift+H")
        self.Bind(wx.EVT_MENU, self.OnAddHeadBlock, AddHeadBlock)
        AddURL = insertMenu.Append(-1, "URL\tCtrl+Shift+U")
        self.Bind(wx.EVT_MENU, self.OnAddURL, AddURL)
        AddEMail = insertMenu.Append(-1, "e-mail\tCtrl+Shift+E")
        self.Bind(wx.EVT_MENU, self.OnAddEMail, AddEMail)
        AddFigure = insertMenu.Append(-1, "Figure\tCtrl+Shift+F")
        self.Bind(wx.EVT_MENU, self.OnAddFigure, AddFigure)
        AddReference = insertMenu.Append(-1, "Reference\tCtrl+Shift+R")
        self.Bind(wx.EVT_MENU, self.OnAddReference, AddReference)
        headingsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_H1, "level &1\tAlt+1", "insert heading level 1", self.OnHeading1), 
                 (ID_H2, "level &2\tAlt+2", "insert heading level 2", self.OnHeading2), 
                 (ID_H3, "level &3\tAlt+3", "insert heading level 3", self.OnHeading3), 
                 (ID_H4, "level &4\tAlt+4", "insert heading level 4", self.OnHeading4), 
                 (ID_H5, "level &5\tAlt+5", "insert heading level 5", self.OnHeading5), 
                 (ID_H6, "level &6\tAlt+6", "insert heading level 6", self.OnHeading6)]:
            if id == None:
                headingsMenu.AppendSeparator()
            else:
                item = headingsMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        insertMenu.Append(-1, "Heading", headingsMenu)
        menuBar.Append(insertMenu, "Insert")  # Add the Insert Menu to the MenuBar

