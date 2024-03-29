# 2022.11.29 This file is for insertions of R elements into the file content, not for processing
#    so that we can be sure it remains useful for WriteR and WriteQuarto


def OnRPipe(self, event):
    self.editor.WriteText(" |> ")


def OnRLAssign(self, event):
    self.editor.WriteText(" <- ")


def OnRRAssign(self, event):
    self.editor.WriteText(" -> ")


def OnPythonChunk(self, event):
    frm, to = self.editor.GetSelection()
    self.editor.SetInsertionPoint(to)
    self.editor.WriteText("\n```\n\n")
    self.editor.SetInsertionPoint(frm)
    self.editor.WriteText("\n```{python}\n")
    self.editor.SetInsertionPoint(frm + 14)


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
    self.editor.WriteText(
        '\n```{r , fig.height=5, fig.width=5, fig.alt=" ", fig.cap=""}\n'
    )
    self.editor.SetInsertionPoint(frm + 8)


def OnRCommand(self, event):
    frm, to = self.editor.GetSelection()
    self.editor.SetInsertionPoint(to)
    self.editor.WriteText("`")
    self.editor.SetInsertionPoint(frm)
    self.editor.WriteText("`r ")
    self.editor.SetInsertionPoint(frm + 3)


# end of file
