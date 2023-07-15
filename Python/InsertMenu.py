# bits to find their way back into front.py


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

