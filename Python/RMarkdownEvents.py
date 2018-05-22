import wx
import sys
from wx.py.shell import Shell
from wx.aui import AuiManager, AuiPaneInfo
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT
from os.path import join, split, isdir, expanduser, realpath
from os import walk
from time import asctime, sleep

quiet = 'TRUE' # or 'FALSE', since these are 'R' constants

hardsettings = {
                             'rendercommand': '''rmarkdown::render("{}",quiet={})''',
                             'renderallcommand': '''rmarkdown::render("{}", output_format="all",quiet={})''',
                             'renderslidycommand': '''rmarkdown::render("{}", output_format=slidy_presentation(),quiet={})''',
                             'renderpdfcommand': '''rmarkdown::render("{}", output_format=pdf_document(),quiet={})''',
                             'renderwordcommand': '''rmarkdown::render("{}", output_format=word_document(),quiet={})''',
                             'renderhtmlcommand': '''rmarkdown::render("{}", output_format="html_document",quiet={})''',
                             'knit2mdcommand': '''knitr::knit("{}",quiet={})''',
                             'knit2htmlcommand': '''knitr::knit2html("{}",quiet={})''',
                             'knit2pdfcommand': '''knitr::knit2pdf("{}",quiet={})'''}

def OnProcess(self, event, whichcmd):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        self.SetFocusConsole(False)
        self.OnSave(event) # This allows the file to be up to date for the build
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.settings['repo']) +
                          hardsettings[whichcmd].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'),
                              quiet)])

def OnRenderNull(self, event):
    OnProcess(self, event, whichcmd='rendercommand')
def OnRenderHtml(self, event):
    OnProcess(self, event, whichcmd='renderhtmlcommand')
def OnRenderAll(self, event):
    OnProcess(self, event, whichcmd='renderallcommand')
def OnRenderWord(self, event):
    OnProcess(self, event, whichcmd='renderwordcommand')
def OnRenderPdf(self, event):
    OnProcess(self, event, whichcmd='renderpdfcommand')
def OnRenderSlidy(self, event):
    OnProcess(self, event, whichcmd='renderslidycommand')
def OnKnit2html(self, event):
    OnProcess(self, event, whichcmd='knit2htmlcommand')
def OnKnit2pdf(self, event):
    OnProcess(self, event, whichcmd='knit2pdfcommand')

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
def OnSelectRenderSlidy(self, event):
    self.Bind(wx.EVT_MENU, self.OnRenderSlidy, self.Render)

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

def OnRmdComment(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText(" -->\n\n")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("\n<!-- ")
        self.editor.SetInsertionPoint(to + 15)

def OnRPipe(self, event):
    self.editor.WriteText(" %>% ") 
def OnRLAssign(self, event):
    self.editor.WriteText(" <- ") 
def OnRRAssign(self, event):
    self.editor.WriteText(" -> ") 

