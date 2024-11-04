# backend  functions
# first set are needed for processing
# second set are for development only

from threading import Thread
from subprocess import Popen, PIPE, STDOUT

import wx

display_rscript_cmd = False  # change this for checking we get it right


## processing functions


class BashProcessThread(Thread):
    """This is the main document processing workhorse of the apps."""

    def __init__(self, flag, input_list, writelineFunc, doneFunc):
        Thread.__init__(self)
        busy = wx.BusyInfo("Please wait")
        self.flag = flag
        self.writelineFunc = writelineFunc
        self.daemon = True
        self.input_list = input_list
        printing(input_list)
        try:
            self.comp_thread = Popen(input_list, stdout=PIPE, stderr=STDOUT)
            if display_rscript_cmd:
                writelineFunc("\n".join(input_list))
                writelineFunc("\n\n")
            for line in self.comp_thread.stdout:
                writelineFunc(line)
            returnCode = self.comp_thread.wait()
            del busy
            doneFunc(returnCode)
        except Exception as error:
            del busy
            doneFunc(f"\nCaught error {error} for {input_list}")


## development functions

# these sswitches are only needed in testing
print_option = True  # for checking details
system_tray = False  # for notifications which are pop ups


def printing(*args):
    if print_option:
        print(args)


def TellUser(self, text):
    """Displays a status message in the status bar and optionally as a system tray notification."""
    self.SetStatusText(text)
    if system_tray:
        try:
            nm = wx.adv.NotificationMessage()
            nm.SetMessage(text)
            nm.SetParent(self)
            nm.SetTitle("")
            nm.SetFlags(wx.ICON_INFORMATION)
            nm.Show(timeout=1)
        except wx.PyNoAppError as error:
            print(f"wxPython app is not initialized properly: {error}")
        except Exception as error:
            print(f"Unexpected problem setting notification: {error}")
