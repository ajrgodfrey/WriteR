# 2022.11.29 This file is for insertions of R content, not for processing
# N.B. some imports are almost certainly redundant
#     This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto



import wx

def OnRPipe(self, event):
    self.editor.WriteText(" |> ") 

def OnRLAssign(self, event):
    self.editor.WriteText(" <- ") 

def OnRRAssign(self, event):
    self.editor.WriteText(" -> ") 

# end of file