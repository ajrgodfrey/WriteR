# 2022.11.29 This file is for insertions of R elements into the file content, not for processing
#    so that we can be sure it remains useful for WriteR and WriteQuarto

from Settings import AppName
from MarkdownEvents import Add2bits


def OnRPipe(self, event):
    self.editor.WriteText(" |> ")


def OnRLAssign(self, event):
    self.editor.WriteText(" <- ")


def OnRRAssign(self, event):
    self.editor.WriteText(" -> ")


def OnPythonChunk(self, event):
    if AppName == "mdWriter":
        Add2bits(self, event, fromText="\n```python\n", toText="\n```\n\n", newPos=12)
    elif AppName == "WriteR":
        Add2bits(self, event, fromText="\n```{python}\n", toText="\n```\n\n", newPos=14)
    elif AppName == "QuartoWriter":
        Add2bits(self, event, fromText="\n```{python}\n", toText="\n```\n\n", newPos=14)


def OnRChunk(self, event):
    if AppName == "mdWriter":
        Add2bits(self, event, fromText="\n```r\n", toText="\n```\n\n", newPos=8)
    elif AppName == "WriteR":
        Add2bits(self, event, fromText="\n```{r }\n", toText="\n```\n\n", newPos=8)
    elif AppName == "QuartoWriter":
        Add2bits(
            self,
            event,
            fromText="\n```{r}\n#| label: \n#| include: true\n",
            toText="\n```\n\n",
            newPos=20,
        )


def OnRGraph(self, event):
    if AppName == "WriteR":
        Add2bits(
            self,
            event,
            fromText='\n```{r , fig.height=5, fig.width=7, fig.alt=" ", fig.cap=""}\n',
            toText="\n```\n\n",
            newPos=8,
        )
    elif AppName == "QuartoWriter":
        Add2bits(
            self,
            event,
            fromText="\n```{r}\n#| label: \n#| include: false\n#| fig.height: 5\n#| fig.width: 7\n#|  fig.alt: \n#| fig.cap: \n",
            toText="\n```\n\n",
            newPos=20,
        )


def OnRCommand(self, event):
    Add2bits(self, event, fromText="`r ", toText="`", newPos=3)


# end of file
