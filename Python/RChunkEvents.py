# 2022.11.29 This file is for insertions of R content, not for processing
# N.B. some imports are almost certainly redundant
#     This file needs careful checking to ensure it contains valid Rmd chunks
#    so that we can be sure it remains useful for WriteR 



import wx
import sys
from wx.py.shell import Shell
from wx.aui import AuiManager, AuiPaneInfo
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT
from os.path import join, split, isdir, expanduser, realpath
from os import walk
from time import asctime, sleep

def OnRChunk(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("\n```\n\n")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("\n```{r}\n\#| \n\#| ")
        self.editor.SetInsertionPoint(frm + 15)

def OnRGraph(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("\n```\n\n")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("\n```{r}\n\#| ,\n\#| fig.height=5,\n\#| fig.width=5,\n\#| fig.alt=\" text \",\n\#| fig.cap=\"\"}\n")
        self.editor.SetInsertionPoint(frm + 15)
