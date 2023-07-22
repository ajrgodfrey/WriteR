# 2022.11.29 This file contains all ID tags so that we can be completely sure there are no clashes between WriteR and WriteQuarto
# it should become redundant as wx.ID_ANY gets rolled out
### N.B. we should be able to eliminate the creation of these ID tags with wx.ID_ANY in the main place the ID is used, probably FrontEnd.py

import wx


# wx.Window.NewControlId()

# set up some ID tags
ID_BUILD = wx.Window.NewControlId()
ID_KNIT2HTML = wx.Window.NewControlId()
ID_KNIT2PDF = wx.Window.NewControlId()
ID_SETTINGS = wx.Window.NewControlId()

ID_FINDONLY = wx.Window.NewControlId()
ID_FINDNEXT = wx.Window.NewControlId()
ID_FINDPREV = wx.Window.NewControlId()
ID_FINDREPLACE = wx.Window.NewControlId()
ID_GOTO  = wx.Window.NewControlId()
ID_WORDCOUNT = wx.Window.NewControlId()

ID_SETMARK = wx.Window.NewControlId()
ID_SELECTTOMARK = wx.Window.NewControlId()

ID_ALTERNATE_FOCUS = wx.Window.NewControlId()


ID_RCOMMAND = wx.Window.NewControlId()
ID_COMMENTOUT = wx.Window.NewControlId()
ID_RCHUNK = wx.Window.NewControlId()
ID_RGRAPH = wx.Window.NewControlId()
ID_RPIPE = wx.Window.NewControlId()
ID_RLASSIGN = wx.Window.NewControlId()
ID_RRASSIGN = wx.Window.NewControlId()


# format menu items
ID_BOLD = wx.Window.NewControlId()
ID_ITALIC = wx.Window.NewControlId()
ID_MATH = wx.Window.NewControlId()
ID_CODE = wx.Window.NewControlId()
ID_RNDBRK = wx.Window.NewControlId()
ID_SQBRK = wx.Window.NewControlId()
ID_CRLBRK = wx.Window.NewControlId()
ID_BRNDBRK = wx.Window.NewControlId()
ID_BSQBRK = wx.Window.NewControlId()
ID_BCRLBRK = wx.Window.NewControlId()

# IDs for headings
ID_H1 = wx.Window.NewControlId() 
ID_H2 = wx.Window.NewControlId() 
ID_H3 = wx.Window.NewControlId() 
ID_H4 = wx.Window.NewControlId() 
ID_H5 = wx.Window.NewControlId() 
ID_H6 = wx.Window.NewControlId()

ID_DIRECTORY_CHANGE = wx.Window.NewControlId()
ID_CRAN = wx.Window.NewControlId()
ID_R_PATH = wx.Window.NewControlId()
ID_BUILD_COMMAND = wx.Window.NewControlId()
ID_KNIT2HTML_COMMAND = wx.Window.NewControlId()
ID_KNIT2PDF_COMMAND = wx.Window.NewControlId()
ID_NEWTEXT = wx.Window.NewControlId()




