from wx.aui import AuiPaneInfo


class MyConsole:
    """This is the second window that shows how processing went."""

    def __init__(self, parent):
        self.console = parent.CreateTextCtrl("")
        self.console.SetEditable(True)
        self.parent = parent
        parent._mgr.AddPane(
            self.console,
            AuiPaneInfo()
            .Name("console")
            .Caption("Console")
            .Bottom()
            .Layer(1)
            .Position(1)
            .CloseButton(True)
            .MinimizeButton(True),
        )
        self.console.SetValue("")
        self.console.write("Render output goes here\n\n")

    def Reset(self):
        self.console.SetValue("")

    #    def write(self, text):
    #        self.console.write(text)

    def CreateWriteText(self, text):
        self.console.write(text)

    def SetFocus(self):
        self.console.SetFocus()

    def DoneFunc(self, retcode):
        self.console.write(f"Done {retcode}")
        self.parent.SetFocusConsole(True)
