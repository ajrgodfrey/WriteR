# 2022.11.29 This file is for the quarto implementation of WriteR ; a separate file exists for the WriteR implementation


import wx
from version import *



def OnAbout(self, event):
        Version = QuartoWriteR_version()
        Text = QuartoWriteRHelpText()
        CommonText = CommonHelpText()
        WholeText = Text + CommonText + "\nVersion: " + Version
        dialog = wx.MessageDialog(self, WholeText,
                                  "About this R Markdown Editor", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

