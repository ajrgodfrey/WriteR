import wx
import sys
from wx.py.shell import Shell
from wx.aui import AuiManager, AuiPaneInfo
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT
from os.path import join, split, isdir, expanduser, realpath
from os import walk
from time import asctime, sleep

def OnRenderNull(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['rendercommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])


def OnRenderHtml(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['renderhtmlcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])

def OnRenderAll(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['renderallcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])

def OnRenderWord(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['renderwordcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])

def OnRenderPdf(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['renderpdfcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])


def OnSelectRenderNull(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderNull, self.Render)

def OnSelectRenderHtml(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderHtml, self.Render)

def OnSelectRenderAll(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderAll, self.Render)

def OnSelectRenderWord(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderWord, self.Render)

def OnSelectRenderPdf(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderPdf, self.Render)


def OnKnit2html(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('knitr', installed.packages()[,1])){{'''.format() +
                          '''install.packages('knitr', repos="{0}")}};require(knitr);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['knit2htmlcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])

def OnKnit2pdf(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('knitr', installed.packages()[,1])){{'''.format() +
                          '''install.packages('knitr', repos="{0}")}};require(knitr);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['knit2pdfcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])


def OnRCommand(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("`")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("`r ")
        self.editor.SetInsertionPoint(frm + 3)

def OnRChunk(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("\n```\n\n")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("\n```{r }\n")
        self.editor.SetInsertionPoint(frm + 8)

def OnRGraph(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("\n```\n\n")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("\n```{r , fig.height=5, fig.width=5, fig.cap=\"\"}\n")
        self.editor.SetInsertionPoint(frm + 8)

def OnRPipe(self, event):
        self.editor.WriteText(" %>% ") 

def OnRLAssign(self, event):
        self.editor.WriteText(" <- ") 

def OnRRAssign(self, event):
        self.editor.WriteText(" -> ") 

