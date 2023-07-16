# For this app to run properly, the GlobalSettings.py must be replaced by GlobalSettingsQ.py 

from FrontEnd  import *

# mandatory lines to get program running.
if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    app.MainLoop()
