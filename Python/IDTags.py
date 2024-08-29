# 2022.11.29 This file contains all ID tags so that we can be completely sure there are no clashes between WriteR and the other apps
# it should become redundant as wx.ID_ANY gets rolled out
# N.B. we should be able to eliminate the creation of these ID tags with wx.ID_ANY in the main place the ID is used, probably FrontEnd.py

import wx


# wx.Window.NewControlId()

# set up some ID tags

ID_SETTINGS = wx.Window.NewControlId()

ID_FINDONLY = wx.Window.NewControlId()
ID_FINDNEXT = wx.Window.NewControlId()
ID_FINDPREV = wx.Window.NewControlId()
ID_FINDREPLACE = wx.Window.NewControlId()
ID_GOTO = wx.Window.NewControlId()
ID_WORDCOUNT = wx.Window.NewControlId()

ID_SETMARK = wx.Window.NewControlId()
ID_SELECTTOMARK = wx.Window.NewControlId()

ID_ALTERNATE_FOCUS = wx.Window.NewControlId()


ID_DIRECTORY_CHANGE = wx.NewIdRef()
ID_CRAN = wx.NewIdRef()

ID_KNIT2PDF_COMMAND = wx.NewIdRef()
ID_NEWTEXT = wx.NewIdRef()


# set up some ID tags
# ID_SETTINGS = wx.NewIdRef()
# ID_FINDONLY = wx.NewIdRef()
# ID_FINDNEXT = wx.NewIdRef()
# ID_FINDPREV = wx.NewIdRef()
# ID_FINDREPLACE = wx.NewIdRef()
# ID_GOTO = wx.NewIdRef()
# ID_WORDCOUNT = wx.NewIdRef()
# ID_SETMARK = wx.NewIdRef()
# ID_SELECTTOMARK = wx.NewIdRef()
# ID_ALTERNATE_FOCUS = wx.NewIdRef()
