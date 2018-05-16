import wx

class MyConsole:
    def __init__(self, parent):
        self.lines = []
        self.parent = parent

    def Reset(self):
        self.lines = []

    def write(self, text):
        self.lines.append(text)

    def CreateWriteText(self, text):
        self.lines.append(text)

    def DoneFunc(self, retcode):
        self.lines.append("ReturnCode: {}".format(retcode))
        dialog = wx.MessageDialog(self.parent, "\n".join(self.lines), "CommandResult", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        self.lines = []

