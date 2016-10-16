import wx

def OnCut(self, event):
        self.editor.Cut()

def OnCopy(self, event):
        self.editor.Copy()

def OnPaste(self, event):
        self.editor.Paste()

def OnDelete(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.Remove(frm, to)

def OnSelectAll(self, event):
        self.editor.SelectAll()


