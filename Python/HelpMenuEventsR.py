# 2022.11.29 This file is for the R markdown implementation of WriteR ; a separate file exists for the Quarto implementation

import wx
from version import *



def OnAbout(self, event):
        Version = WriteR_version()
        Text = WriteRHelpText()
        CommonText = CommonHelpText()
        WholeText = Text + CommonText + "\nVersion: " + Version
        dialog = wx.MessageDialog(self, WholeText,
                                  "About this R Markdown Editor", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

