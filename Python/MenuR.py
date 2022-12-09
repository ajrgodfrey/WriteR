# 2022.12.08 This file needs careful checking to ensure it is for WriteR only
#    a corresponding file is required for QuartoWriter

import wx
# common menus
import EditMenu, ViewMenu, MathsMenu, InsertMenu, FormatMenu
# specific menus
import HelpMenu, StatsMenu, BuildMenuR

def MakeMenu(self):
    MainMenu = wx.MenuBar()
    self.SetMenuBar(MainMenu)

    # File Menu
    fileMenu = wx.Menu()
    for id, label, helpText, handler in \
                [(wx.ID_NEW, "New file\tCtrl+N", "Start a new file", self.OnNewFile),
                 (wx.ID_OPEN, "&Open\tCtrl+O", "Open an existing file", self.OnOpen),
                 (wx.ID_SAVE, "&Save\tCtrl+S", "Save the current file", self.OnSave),
                 (wx.ID_SAVEAS, "Save &As\tCtrl+Shift+S", "Save the file under a different name", self.OnSaveAs),
                 (None,) * 4,
                 (wx.ID_EXIT, "Quit && save\tCtrl+Q", "Saves the current file and closes the program", self.OnSafeExit)]:
        if id == None:
                fileMenu.AppendSeparator()
        else:
                item = fileMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
    MainMenu.Append(fileMenu, "&File")  # Add the fileMenu to the MenuBar


    # Edit Menu
    EditMenu.MakeEditMenu(self, MainMenu)

    # View Menu
#    ViewMenu.MakeViewMenu(self, MainMenu)


        # BuildR Menu
#    BuildRMenu.MakeBuildRMenu(self, MainMenu)

# Insert Menu
#    InsertMenu.MakeInsertMenu(self, MainMenu)

    # Format Menu
#    FormatMenu.MakeFormatMenu(self, MainMenu)


    # Maths Menu
    MathsMenu.MakeMathsMenu(self, MainMenu)

    # Stats Menu
#    StatsMenu.MakeStatsMenu(self, MainMenu)
# this one is bound to have some differences in the subordinate functions

    # Help Menu
    HelpMenu.MakeHelpMenu(self, MainMenu)

