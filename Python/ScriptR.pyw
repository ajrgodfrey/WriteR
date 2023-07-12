# list the things I want to set in the head files as globals
AppName = "ScriptR"
SBText = "This program is for editing R scripts"

from FrontEnd  import *


# mandatory lines to get program running.
if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    app.MainLoop()
