# backend  functions
# first set are needed for processing
# second set are for development only

import wx


## processing functions

## development functions

# these sswitches are only needed in testing
print_option = True  # for checking details
system_tray = False  # for notifications which are pop ups


def printing(*args):
    if print_option:
        print(args)


def TellUser(self, text):
    self.SetStatusText(text)
    if system_tray:
        try:
            nm = wx.adv.NotificationMessage()
            nm.SetMessage(text)
            nm.SetParent(self)
            nm.SetTitle("")
            nm.SetFlags(wx.ICON_INFORMATION)
            nm.Show(1)
        except Exception as error:
            print(f"Problem setting notification {error}")
