import wx
import wx.stc # needed for word count and go to line


def OnWordCount(self, event):
        text=self.editor.GetText()
        word_count=len(text.split())
        dialog=wx.MessageDialog(self,"%d words" % word_count,"Word count",wx.ICON_INFORMATION|wx.OK)
        dialog.Centre()
        result=dialog.ShowModal()
        dialog.Destroy()
    
    
def OnGoToLine(self, event):
        dialog = wx.NumberEntryDialog(self, "Go to line","","Line",self.editor.GetCurrentLine(),0,2**30)
        if dialog.ShowModal() == wx.ID_OK:
            line=dialog.GetValue()
            line=max(0,min(self.editor.GetNumberOfLines(),line))
#            self.editor.GotoLine(dialog.GetValue()) # needs wx.stc to be used
        dialog.Destroy()
    
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


