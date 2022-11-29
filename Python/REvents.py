# 2022.11.29 This file is for insertions of R content, not for processing
# N.B. some imports are almost certainly redundant
#     This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto



import wx
import sys
from wx.py.shell import Shell
from wx.aui import AuiManager, AuiPaneInfo
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT
from os.path import join, split, isdir, expanduser, realpath
from os import walk
from time import asctime, sleep



def OnRCommand(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("`")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("`r ")
        self.editor.SetInsertionPoint(frm + 3)




def OnRPipe(self, event):
    self.editor.WriteText(" |> ") 
def OnRLAssign(self, event):
    self.editor.WriteText(" <- ") 
def OnRRAssign(self, event):
    self.editor.WriteText(" -> ") 
