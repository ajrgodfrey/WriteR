# 2023.07.12 This file is for the ScriptR implementation of WriteR ; a separate file exists for the WriteR implementation

import wx
from version import *



def OnAbout(self, event):
        Version = ScriptR_version()
        Text = ScriptRHelpText()
        CommonText = CommonHelpText()
        WholeText = Text + CommonText + "\nVersion: " + Version
        dialog = wx.MessageDialog(self, WholeText,
                                  "About this R Markdown Editor", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

