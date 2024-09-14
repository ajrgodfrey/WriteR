# this file has the settings needed for all the apps.

from wx import App

AppName = App(False).GetAppName()

GlobalSettings = {}

AppSettings = {
    "extension": {
        "WriteR": "Rmd",
        "QuartoWriter": "Qmd",
        "mdWriter": "md",
        "ScriptR": "R",
    },
    "blank": {"WriteR": "", "QuartoWriter": "", "mdWriter": "", "ScriptR": ""},
    "startingText": {
        "WriteR": "# Use WriteR to edit and process your R markdown documents.",
        "QuartoWriter": "# Use QuartoWriter to edit and process your Quarto markdown documents. These can include R or Python code chunks",
        "mdWriter": "# Use mdWriter to edit and process your markdown documents.",
        "ScriptR": "#' Use ScriptR to edit and process your R scripts",
    },
    "statusBarText": {
        "WriteR": "This program is for editing R markdown files",
        "QuartoWriter": "This program is for editing Quarto markdown files",
        "mdWriter": "This program is for editing plain markdown files",
        "ScriptR": "This program is for editing R scripts",
    },
}
