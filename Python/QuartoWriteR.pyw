# This is QuartoWriteR
## change settings in settings.py or version number in version.py
## everything else uses the name of this Python script to select functionality

from FrontEnd  import *

# mandatory lines to get program running.
if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    app.MainLoop()
