
# this file has the settings bneeded for all the apps.

import wx

AppName = wx.App(False).GetAppName()

if AppName == "QuartoWriter":
    StatusBarText = "This program is for editing Quarto markdown files"
    FileExtension = "Qmd"
    StartingText = "# Use QuartoWriter to edit and process your Quarto markdown documents. These can include R or Python code chunks"

elif AppName == "WriteR":
    StatusBarText = "This program is for editing R markdown files"
    FileExtension = "Rmd"
    StartingText = "# Use WriteR to edit and process your R markdown documents."

elif AppName == "mdWriter":
    StatusBarText = "This program is for editing plain markdown files"
    FileExtension = "md"
    StartingText = "# Use mdWriter to edit and process your markdown documents."

elif AppName == "ScriptR":
    StatusBarText = "This program is for editing R scripts"
    FileExtension = "R"
    StartingText = "#' Use ScriptR to edit and process your R scripts"
