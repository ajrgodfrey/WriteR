# 2022.11.29 This file is for the quarto implementation of WriteR ; a separate file exists for the WriteR implementation

import wx
def OnAbout(self, event):
        dialog = wx.MessageDialog(self, "WriteQuarto is built as a branch of WriteR 2022.2 , which  was an initial attempt  at developing an R Markdown editor\n"                                        "using wxPython. Development started by Jonathan Godfrey\n"
                                        "with assistance from (in order of contribution) James Curtis,\nTimothy Bilton, and Marshall Flax.\nThis new implementation would not have been possible without their assistance.\nPlease send all feedback to Jonathan Godfrey at a.j.godfrey@massey.ac.nz\nVersion: ",
                                  "About this Quarto markdown Editor", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

