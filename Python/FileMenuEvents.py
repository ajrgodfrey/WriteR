# module for file menu events, created July 2023

from os.path import join
from time import asctime

import wx


def OnOpen(self, event):
    if self.askUserForFilename(style=wx.FD_OPEN, **self.defaultFileDialogOptions()):
        self.fileOpen(self.dirname, self.filename)


def OnClose(self, event):
    self.settings["filename"] = self.filename
    self.settings["lastdir"] = self.dirname
    if event.CanVeto() and self.editor.IsModified():
        hold = wx.MessageBox(
            "Would you like to save your work?",
            "Save before exit?",
            wx.ICON_QUESTION | wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT,
        )
        if hold == wx.YES:
            self.OnSave(event)
            self.Destroy()
        elif hold == wx.NO:
            self.Destroy()
        else:
            event.Veto()
    else:
        self.Destroy()


def fatalError(self, message):
    dialog = wx.MessageDialog(self, message, "Fatal Error", wx.OK)
    dialog.ShowModal()
    dialog.Destroy()
    self.OnExit()


def fileOpen(self, dirname, filename):
    path = join(dirname.strip(), filename)
    try:
        with open(path, "r") as textfile:
            self.editor.SetValue(textfile.read())
    except Exception as error:
        self.fatalError(f"An error occurred with file '{path}': {error}")
        self.OnExit()


def OnNewFile(self, event):
    self.olddirname = self.dirname
    self.dirname = ".\\templates"
    self.OnOpen(event)
    self.dirname = self.olddirname
    if self.filename == "Blank.Rmd":
        self.editor.WriteText("% file created on " + asctime() + "\n\n")
    self.OnSaveAs(event)


def OnSaveAs(self, event):
    if self.askUserForFilename(
        defaultFile=self.filename, style=wx.FD_SAVE, **self.defaultFileDialogOptions()
    ):
        self.OnSave(event)


def OnSave(self, event):
    try:
        with open(join(self.dirname, self.filename), "w", encoding="utf-8") as textfile:
            textfile.write(self.editor.GetValue())
    except Exception as error:
        self.fatalError(f"An error occurred while saving the file: {error}")


def OnExit(self):
    if self._mgr:
        self._mgr.UnInit()
    self.Close()  # Close the main window.


def OnSafeExit(self, event):
    self.OnSave(event)
    self.OnExit()
