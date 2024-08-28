# combination help event file

import wx
from version import (
    mdWriter_version,
    QuartoWriter_version,
    ScriptR_version,
    WriteR_version,
)
from Settings import AppName

# Basic help


def OnBasicHelp(self, event):
    if AppName == "ScriptR":
        Text = CommonBasicHelpText + BasicTextS
    elif AppName == "mdWriter":
        Text = CommonBasicHelpText + BasicTextM
    elif AppName == "WriteR":
        Text = CommonBasicHelpText + BasicTextR
    else:
        Text = CommonBasicHelpText + BasicTextQ
    dialog = wx.MessageDialog(self, Text, f"Basic help for the {AppName} Editor", wx.OK)
    dialog.ShowModal()
    dialog.Destroy()


CommonBasicHelpText = """This editor was designed for use with a screen reader and has been tested with JAWS and NVDA.\n
            It makes extensive use of hot keys, many of which are in common use by other software.\n
            All hot keys are indicated in the menus.\n
            The file you create here will be converted to HTML if you press the f5 key.\n
            A new window will open which will tell you if the processing was successful.\n
            If you have success, then the resulting file will be read in your browser; 
            you may need to refresh the browser using the f5 key while in the browser.\n
            Once you review the processing, hit the f4 key to return to the original window.\n
            Use Alt+tab to switch between applications."""

BasicTextM = """mdWriter has fewer features than WriteR and QuartoWriter.\n
            It was designed to be used by people wanting to work with simple markdown. \n
            You should move to using WriteR or QuartoWriter when you want to take advantage of code embedded in your markdown.\n"""

BasicTextQ = "QuartoWriter is designed for people wanting to process R and Python commands in their markdown files.\n"

BasicTextR = "WriteR was designed specifically for processing R markdown files.\n"

BasicTextS = """ScriptR has fewer features than WriteR and QuartoWriter.\n
            It was designed to be used by people wanting to work with simple R scripts.\n
            You should move to using WriteR or QuartoWriter when you want to take advantage of markdown.\n
            Each line of the file being edited must start with a # symbol if it is not valid R code.\n"""


# About the editors


def OnAbout(self, event):
    if AppName == "ScriptR":
        WholeText = AboutScriptR + CommonHelpText + "\nVersion: " + ScriptR_version
    elif AppName == "mdWriter":
        WholeText = AboutMDWriter + CommonHelpText + "\nVersion: " + mdWriter_version
    elif AppName == "WriteR":
        WholeText = AboutWriteR + CommonHelpText + "\nVersion: " + WriteR_version
    else:
        WholeText = (
            AboutQuartoWriter + CommonHelpText + "\nVersion: " + QuartoWriter_version
        )
    dialog = wx.MessageDialog(self, WholeText, "About this R script Editor", wx.OK)
    dialog.ShowModal()
    dialog.Destroy()


AboutMDWriter = (
    "This cut back version of WriteR is designed for use with plain markdown files.\n"
)

AboutQuartoWriter = "This new implementation of WriteR is designed to work with Quarto, the next generation of R markdown documents.\n"

AboutWriteR = "WriteR is an app for writing and processing R markdown documents.\n"

AboutScriptR = """ScriptR is an attempt  at developing an accessible editor for R scripts.\n
            This cut back version of WriteR was developed in 2023 due to ongoing accessibility issues with RStudio, 
            and user feedback on difficulty reading output in both the GUI and terminal.\n"""


CommonHelpText = """This software was created using wxPython. \nDevelopment started by Jonathan Godfrey and James Curtis in 2015.\n
            Development continued with Timothy Bilton in 2016.\n
            Marshall Flax then made major progress on the find/replace features and more in 2018.\n
            The assistance of these contributors is hugely appreciated. \n
            Send all feedback to Jonathan Godfrey at a.j.godfrey@massey.ac.nz\n"""
