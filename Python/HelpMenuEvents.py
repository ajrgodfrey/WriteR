# attempted combination help event file

import wx
from version import *
from GlobalSettings import * # for making sure the correct app is being opened.

## Basic help


def OnBasicHelp(self, event):
    if(AppName == "ScriptR"):
        OnBasicHelpS(self, event)
    elif(AppName == "WriteR"):
        OnBasicHelpR(self, event)
    else:
        OnBasicHelpQ(self, event)

def CommonBasicHelpText(): 
    return("""This editor was designed for use with a screen reader and has been tested with JAWS and NVDA.\n
            It makes extensive use of hot keys, many of which are in common use by other software.\n
            All hot keys are indicated in the menus.\n
            The file you create here will be converted to HTML if you press the f5 key.\n
            A new window will open which will tell you if the processing was successful.\n
            If you have success, then the resulting file will be read in your browser; 
            you may need to refresh the browser using the f5 key while in the browser.\n
            Once you review the processing, hit the f4 key to return to the original window.\n
            Use Alt+tab to switch between applications.""")




### some fixes below here

def OnBasicHelpQ(self, event):
    ScriptRBasicHelpText = """ScriptR has fewer features than WriteR and QuartoWriteR.\n
            It was designed to be used by people wanting to work with simple R scripts.\n
            You should move to using WriteR or QuartoWriteR when you want to take advantage of markdown.\n
            Each line of the file being edited must start with a # symbol if it is not valid R code.\n"""
    Text = CommonBasicHelpText() + ScriptRBasicHelpText
    dialog = wx.MessageDialog(self, Text, "Basic help for this R script Editor", wx.OK)
    dialog.ShowModal()
    dialog.Destroy()

def OnBasicHelpR(self, event):
    ScriptRBasicHelpText = """ScriptR has fewer features than WriteR and QuartoWriteR.\n
            It was designed to be used by people wanting to work with simple R scripts.\n
            You should move to using WriteR or QuartoWriteR when you want to take advantage of markdown.\n
            Each line of the file being edited must start with a # symbol if it is not valid R code.\n"""
    Text = CommonBasicHelpText() + ScriptRBasicHelpText
    dialog = wx.MessageDialog(self, Text, "Basic help for this R script Editor", wx.OK)
    dialog.ShowModal()
    dialog.Destroy()

def OnBasicHelpS(self, event):
    ScriptRBasicHelpText = """ScriptR has fewer features than WriteR and QuartoWriteR.\n
            It was designed to be used by people wanting to work with simple R scripts.\n
            You should move to using WriteR or QuartoWriteR when you want to take advantage of markdown.\n
            Each line of the file being edited must start with a # symbol if it is not valid R code.\n"""
    Text = CommonBasicHelpText() + ScriptRBasicHelpText
    dialog = wx.MessageDialog(self, Text, "Basic help for this R script Editor", wx.OK)
    dialog.ShowModal()
    dialog.Destroy()

## About the editors

def OnAbout(self, event):
    if(AppName == "ScriptR"):
        OnAboutS(self, event)
    elif(AppName == "WriteR"):
        OnAboutR(self, event)
    else:
        OnAboutQ(self, event)

AboutQuartoWriteR = "This new implementation of WriteR is designed to work with Quarto, the next generation of R markdown documents.\n"

AboutWriteR = "WriteR is an app for writing and processing R markdown documents.\n"

AboutScriptR = """ScriptR is an attempt  at developing an accessible editor for R scripts.\n
            This cut back version of WriteR was developed in 2023 due to ongoing accessibility issues with RStudio, 
            and user feedback on difficulty reading output in both the GUI and terminal.\n"""


CommonHelpText = """This software was created using wxPython. \nDevelopment started by Jonathan Godfrey and James Curtis in 2015.\n
            Development continued with Timothy Bilton in 2016.\n
            Marshall Flax then made major progress on the find/replace features and more in 2018.\n
            The assistance of these contributors is hugely appreciated. \n
            Send all feedback to Jonathan Godfrey at a.j.godfrey@massey.ac.nz\n"""

def OnAboutQ(self, event):
        Version = QuartoWriteR_version()
        WholeText = AboutQuartoWriteR + CommonHelpText + "\nVersion: " + Version
        dialog = wx.MessageDialog(self, WholeText, "About this R Markdown Editor", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

def OnAboutR(self, event):
        Version = WriteR_version()
        WholeText = AboutWriteR + CommonHelpText + "\nVersion: " + Version
        dialog = wx.MessageDialog(self, WholeText, "About this R Markdown Editor", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
              
def OnAboutS(self, event):
        Version = ScriptR_version()
        WholeText = AboutScriptR + CommonHelpText + "\nVersion: " + Version
        dialog = wx.MessageDialog(self, WholeText, "About this R script Editor", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()


