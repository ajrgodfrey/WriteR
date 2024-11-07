# This file is for functions relating to processing of files, not for file content.

from os.path import join, split, isdir
from os import walk
from time import sleep

import wx

from Settings import AppName

from BackEnd import BashProcessThread, printing

quiet = "TRUE"  # or 'FALSE', since these are 'R' constants

RcmdSettings = {
    "rendercommand": """rmarkdown::render("{}",quiet={})""",
    "renderallcommand": """rmarkdown::render("{}", output_format="all",quiet={})""",
    "renderslidycommand": """rmarkdown::render("{}", output_format=slidy_presentation(),quiet={})""",
    "renderpdfcommand": """rmarkdown::render("{}", output_format=pdf_document(),quiet={})""",
    "renderwordcommand": """rmarkdown::render("{}", output_format=word_document(),quiet={})""",
    "renderhtmlcommand": """rmarkdown::render("{}", output_format="html_document",quiet={})""",
    "knit2mdcommand": """knitr::knit("{}",quiet={})""",
    "knit2htmlcommand": """knitr::knit2html("{}",quiet={})""",
    "knit2pdfcommand": """knitr::knit2pdf("{}",quiet={})""",
}


def OnRProcess(self, event, whichcmd):
    StartThread(
        self,
        [
            self.settings["RDirectory"],
            "-e",
            "{if (!require(rmarkdown)){"
            + "chooseCRANmirror(ind=1); install.packages('rmarkdown')}; require(rmarkdown);"
            + RcmdSettings[whichcmd].format(
                join(self.dirname, self.filename).replace("\\", "\\\\"), quiet
            )
            + "}",
        ],
    )


def OnQProcess(self, event, whichcmd):
    FullFilename = join(self.dirname, self.filename)
    StartThread(self, ["quarto", "render", FullFilename])


def OnPProcess(self, event, whichcmd):
    FullFilename = join(self.dirname, self.filename)
    NewFilename = FullFilename.replace(".md", ".html")
    StartThread(self, ["pandoc", FullFilename, "-o", NewFilename])


#    return


def OnProcess(self, event, whichcmd):
    self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
    self._mgr.Update()
    self.SetFocusConsole(False)
    self.OnSave(event)  # This ensures the file is up to date for the build
    if AppName == "QuartoWriter":
        OnQProcess(self, event, whichcmd)
    elif AppName == "mdWriter":
        OnPProcess(self, event, whichcmd)
    else:
        OnRProcess(self, event, whichcmd)


def OnFixR(self, event):
    cmd = "if(!require(rmarkdown)){chooseCRANmirror(ind=1); install.packages('rmarkdown')}"
    self.StartThread([self.settings["RDirectory"], "-e", cmd])


def OnRenderNull(self, event):
    OnProcess(self, event, whichcmd="rendercommand")


def OnRenderHtml(self, event):
    OnProcess(self, event, whichcmd="renderhtmlcommand")


def OnRenderAll(self, event):
    OnProcess(self, event, whichcmd="renderallcommand")


def OnRenderWord(self, event):
    OnProcess(self, event, whichcmd="renderwordcommand")


def OnRenderPdf(self, event):
    OnProcess(self, event, whichcmd="renderpdfcommand")


def OnRenderSlidy(self, event):
    OnProcess(self, event, whichcmd="renderslidycommand")


def OnKnit2html(self, event):
    OnProcess(self, event, whichcmd="knit2htmlcommand")


def OnKnit2pdf(self, event):
    OnProcess(self, event, whichcmd="knit2pdfcommand")


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


STATE_NORMAL = "in text"
STATE_START_HEADER = "start header"
STATE_IN_HEADER = "in header"
STATE_END_HEADER = "end header"
STATE_START_CODEBLOCK = "start codeblock"
STATE_IN_CODEBLOCK = "in codeblock"
STATE_END_CODEBLOCK = "end codeblock"
STATE_SINGLE_LINE_LATEX = "single line latex"
STATE_START_LATEX_DOLLAR = "start latex"
STATE_IN_LATEX_DOLLAR = "in latex"
STATE_END_LATEX_DOLLAR = "end latex"
STATE_START_LATEX_BRACKET = "start  latex"  # note: more spaces between words than corresponding "DOLLAR" constant
STATE_IN_LATEX_BRACKET = (
    "in  latex"  # note: more spaces between words than corresponding "DOLLAR" constant
)
STATE_END_LATEX_BRACKET = (
    "end  latex"  # note: more spaces between words than corresponding "DOLLAR" constant
)


def CurrentMarkdown(self):
    _, _, currentRow = self.editor.PositionToXY(self.editor.GetInsertionPoint())
    state = STATE_NORMAL
    for i in range(0, currentRow + 1):
        line = self.editor.GetLineText(i)
        if (
            state is STATE_NORMAL
            or state is STATE_END_HEADER
            or state is STATE_END_CODEBLOCK
            or state is STATE_END_LATEX_DOLLAR
            or state is STATE_END_LATEX_BRACKET
            or state is STATE_SINGLE_LINE_LATEX
        ):
            if line.startswith("---"):
                state = STATE_START_HEADER
            elif line.startswith("```"):
                state = STATE_START_CODEBLOCK
            elif line.startswith("$$") and line[2:].endswith("$$"):
                state = STATE_SINGLE_LINE_LATEX
            elif line.startswith("$$"):
                state = STATE_START_LATEX_DOLLAR
            elif line.startswith("\\["):
                state = STATE_START_LATEX_BRACKET
            else:
                state = STATE_NORMAL
        elif state is STATE_START_HEADER or state is STATE_IN_HEADER:
            if line.startswith("---"):
                state = STATE_END_HEADER
            else:
                state = STATE_IN_HEADER
        elif state is STATE_START_CODEBLOCK or state is STATE_IN_CODEBLOCK:
            if line.startswith("```"):
                state = STATE_END_CODEBLOCK
            else:
                state = STATE_IN_CODEBLOCK
        elif state is STATE_START_LATEX_DOLLAR or state is STATE_IN_LATEX_DOLLAR:
            if line.startswith("$$") or line.endswith("$$"):
                state = STATE_END_LATEX_DOLLAR
            else:
                state = STATE_IN_LATEX_DOLLAR
        elif state is STATE_START_LATEX_BRACKET or state is STATE_IN_LATEX_BRACKET:
            if line.startswith("\\]"):
                state = STATE_END_LATEX_BRACKET
            else:
                state = STATE_IN_LATEX_BRACKET
    return state


def splitter(path, interest):
    look = split(path)
    if interest in look[1]:
        return look[1]
    if len(look[0]) == 0:
        return None
    return splitter(look[0], interest)


def GetRDirectory(self):
    if AppName == "QuartoWriter":
        return ""
    if AppName == "mdWriter":
        return ""
    rscript = "Rscript.exe"
    warn = f"Cannot find {rscript} in default install location."
    version = "R-0.0.0"
    choice = None
    if isdir("C:\\Program Files\\R"):
        hold = "C:\\Program Files\\R"
    else:
        print(warn)
        return ""
    options = [join(r, rscript) for r, d, f in walk(hold) if rscript in f]
    printing("options", options)
    if len(options) > 0:
        choice = options[0]
        for op in options[1:]:
            vv = splitter(op, "R-")
            if vv >= version:
                if "x64" in op:
                    choice = op
                    version = vv
                elif "i386" in op and "x64" not in choice:
                    choice = op
                    version = vv
                elif "i386" not in choice and "x64" not in choice:
                    choice = op
                    version = vv
    else:
        print(warn)
        return ""
    return choice


def StartThread(self, input_object):
    if self.sub_flag.isSet():
        return
    if self.comp_thread is not None:
        self.sub_flag.set()
        while self.comp_thread.is_alive():
            sleep(1)
        self.sub_flag.clear()
        self.console.Reset()
    self.comp_thread = BashProcessThread(
        self.sub_flag,
        input_object,
        self.console.CreateWriteText,
        self.console.DoneFunc,
    )
    self.comp_thread.start()
