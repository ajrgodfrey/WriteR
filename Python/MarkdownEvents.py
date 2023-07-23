# 2022.11.29 this file is for the processing of files using markdown
#      It is therefore intended for both WriteR, and WriteQuarto
# N.B. need to bring standard markdown actions into here; Might still be lurking in WriteR.pyw

# N.B. some of the following imports are almost certainly redundant

import wx
import sys
from wx.py.shell import Shell
from wx.aui import AuiManager, AuiPaneInfo
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT
from os.path import join, split, isdir, expanduser, realpath
from os import walk
from time import asctime, sleep

from GlobalSettings import *


def OnSquareBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("]")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("[")
        self.editor.SetInsertionPoint(to + 2)

def OnCurlyBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("}")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("{")
        self.editor.SetInsertionPoint(to + 2)

def OnRoundBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText(")")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("(")
        self.editor.SetInsertionPoint(to + 2)

def OnAddHeadBlock(self, event):
        self.editor.SetInsertionPoint(0)
        self.editor.WriteText('---\ntitle: ""\nauthor: ""\ndate: ""\noutput: html_document\n---\n') 
        self.editor.SetInsertionPoint(13)

def OnAddReference(self, event):
        self.editor.WriteText(" [@ref] ") 

def OnAddURL(self, event):
        self.editor.WriteText(" [alt text](http://) ") 

def OnAddEMail(self, event):
        self.editor.WriteText(" [name](Mailto:) ") 

def OnAddFigure(self, event):
        self.editor.WriteText(" ![alt tag](filename) ") 

def OnHeading1(self, event):
        self.editor.WriteText("\n")
        if AppName == "ScriptR":
            self.editor.WriteText("#' ")
        self.editor.WriteText("# ") 

def OnHeading2(self, event):
        self.editor.WriteText("\n## ") 

def OnHeading3(self, event):
        self.editor.WriteText("\n### ") 

def OnHeading4(self, event):
        self.editor.WriteText("\n#### ") 

def OnHeading5(self, event):
        self.editor.WriteText("\n##### ") 

def OnHeading6(self, event):
        self.editor.WriteText("\n###### ")

def OnMath(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("$")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("$")
        self.editor.SetInsertionPoint(to + 2)

def OnItalic(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("*")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("*")
        self.editor.SetInsertionPoint(to + 2)


def OnBold(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("**")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("**")
        self.editor.SetInsertionPoint(to + 4)

def OnCode(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("`")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("`")
        self.editor.SetInsertionPoint(to + 2)

def OnHTMLComment(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText(" -->\n\n")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("\n<!-- ")
        self.editor.SetInsertionPoint(to + 15)

def OnAddSeparator(self, event):
        self.editor.WriteText("\n")
        if AppName == "ScriptR":
            self.editor.WriteText("#' ")
        self.editor.WriteText("--- \n")



# end of file