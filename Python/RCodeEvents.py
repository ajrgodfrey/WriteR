# 2022.11.29 This file is for insertions of R elements into the file content, not for processing
#    so that we can be sure it remains useful for WriteR and WriteQuarto


def OnRPipe(self, event):
    self.editor.WriteText(" |> ")


def OnRLAssign(self, event):
    self.editor.WriteText(" <- ")


def OnRRAssign(self, event):
    self.editor.WriteText(" -> ")


def OnPythonChunk(self, event):
    Add2bits(self, event, fromText="\n```{python}\n", toText="\n```\n\n", newPos=14)


def OnRChunk(self, event):
    Add2bits(self, event, fromText="\n```{r }\n", toText="\n```\n\n", newPos=8)


def OnRGraph(self, event):
    Add2bits(
        self,
        event,
        fromText='\n```{r , fig.height=5, fig.width=7, fig.alt=" ", fig.cap=""}\n',
        toText="\n```\n\n",
        newPos=8,
    )


def OnRCommand(self, event):
    Add2bits(self, event, fromText="`r ", toText="`", newPos=3)


def Add2bits(self, event, fromText="", toText="", newPos=0):
    frm, to = self.editor.GetSelection()
    self.editor.SetInsertionPoint(to)
    self.editor.WriteText(toText)
    self.editor.SetInsertionPoint(frm)
    self.editor.WriteText(fromText)
    self.editor.SetInsertionPoint(frm + newPos)


# end of file
