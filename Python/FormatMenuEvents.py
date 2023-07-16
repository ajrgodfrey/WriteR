# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx

# format menu events

def OnSquareBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("]")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("[")
        self.editor.SetInsertionPoint(to + 2)

def OnCurlyBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("}")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("{")
        self.editor.SetInsertionPoint(to + 2)


def OnRoundBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText(")")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("(")
        self.editor.SetInsertionPoint(to + 2)

def OnAddHeadBlock(self, event):
        self.editor.SetInsertionPoint(0)
        self.editor.WriteText('---\ntitle: ""\nauthor: ""\ndate: ""\noutput: html_document\n---\n') 
        self.editor.SetInsertionPoint(13)

