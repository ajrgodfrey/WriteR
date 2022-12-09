# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx
from EditMenuEvents import *

def MakeEditMenu(self, MainMenu):
    editMenu = wx.Menu()
    for id, label, helpText, handler in \
                 [(wx.ID_CUT, "Cu&t\tCtrl+X", "Cut highlighted text to clipboard", OnCut),
                 (wx.ID_COPY, "&Copy\tCtrl+C", "Copy highlighted text to clipboard", OnCopy),
                 (wx.ID_PASTE, "&Paste\tCtrl+V", "Paste text from clipboard", OnPaste),
                 (wx.ID_SELECTALL, "Select all\tCtrl+A", "Highlight entire text", OnSelectAll),
                 (wx.ID_DELETE, "&Delete", "Delete highlighted text", OnDelete),
                 ("ID_WORDCOUNT", "Word count\tCtrl+w", "get a word count of the entire text", OnWordCount),
                 (None,) * 4,
                 ("ID_FINDONLY", "Find\tCtrl+F", "Open a standard find dialog box", OnShowFind),
                 ("ID_FINDNEXT", "FindNext\tF3", "FindNext", F3Next),
                 ("ID_FINDPREV", "FindPrevious\tShift+F3", "FindPrev", ShiftF3Previous),
                 ("ID_GOTO", "Go to line\tCtrl+g", "Open a dialog box to choose a line number", OnGoToLine),
                 ("ID_FINDREPLACE", "Find/replace\tCtrl+H", "Open a find/replace dialog box", OnShowFindReplace),
                 ("ID_SETMARK", "Set Mark\tCtrl+SPACE", "Set Mark", OnSetMark),
                 ("ID_SELECTTOMARK", "Select To Mark\tAlt+Ctrl+SPACE", "Select To Mark", OnSelectToMark),
                 ("ID_ALTERNATE_FOCUS", "Alternate Focus\tF4", "Alternate Focus", AlternateFocus),
                 (None,) * 4,
                 ("ID_SETTINGS", 'Settings', "Setup the editor to your liking", OnSettings)]:
            if id == None:
                 editMenu.AppendSeparator()
            else:
                 item = editMenu.Append(wx.ID_ANY, label, helpText)
                 self.Bind(wx.EVT_MENU, handler, item)
    MainMenu.Append(editMenu, "&Edit")  # Add the editMenu to the MenuBar
