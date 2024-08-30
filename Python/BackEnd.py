# backend  functions
# first set are needed for processing
# second set are for development only


## processing functions

## development functions

print_option = False
system_tray = True


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
            pass
