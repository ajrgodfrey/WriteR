# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx
import wx.stc # needed for word count and go to line

def OnGoToLine(self, event):
        (x, y) = self.editor.PositionToXY(self.editor.GetInsertionPoint())
        maxLine=self.editor.GetNumberOfLines()
        dialog = wx.NumberEntryDialog(self, caption="GoToLine", message="Go to line",prompt="Line",value=y,min=0,max=maxLine)
        if dialog.ShowModal() == wx.ID_OK:
            line=dialog.GetValue()
            line=max(0,min(self.editor.GetNumberOfLines(),line))
            self.editor.SetInsertionPoint(self.editor.XYToPosition(0, dialog.GetValue()))
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

def OnSettings(self, event): # not properly implemented
        wx.MessageBox("You wanted to see the settings, but this is not properly implemented yet")

def OnWordCount(self, event):
        text=self.editor.GetValue()
        word_count=len(text.split())
        (on, x, y) = self.editor.PositionToXY(self.editor.GetInsertionPoint())
        line_count = self.editor.GetNumberOfLines()
        markdownState = RMarkdownEvents.CurrentMarkdown(self)
        self.TellUser("Line {}/{}. WordCount {}. State {}".format(y, line_count, word_count, markdownState))
def OnShowFind(self, event):
        data = wx.FindReplaceData()
        data.SetFlags(wx.FR_DOWN)
        dlg = wx.FindReplaceDialog(self, data, "Find")
        dlg.data = data  # save a reference to it...
        dlg.Show(True)

def OnSetMark(self, event):
        self.mark = self.editor.GetInsertionPoint()
        if beep:
           winsound.Beep(1000, 250)

def F3Next(self, event):
        self.FindFrom(self.priorMatchCol, self.priorMatchRow, False)

def ShiftF3Previous(self, event):
        self.FindFrom(self.priorMatchCol, self.priorMatchRow, True)

def OnFind(self, event):
        et = event.GetEventType()
        self.regex = re.compile(self.ComputeFindString(event), self.ComputeReFlags(event))
        self.forward = event.GetFlags() & wx.FR_DOWN
        if et == wx.wxEVT_COMMAND_FIND:
            (ok, col, row) = self.editor.PositionToXY(self.editor.GetInsertionPoint())
            self.FindFrom(col, row, False)
        elif et == wx.wxEVT_COMMAND_FIND_NEXT:
            self.FindFrom(self.priorMatchCol, self.priorMatchRow, False)
        elif et == wx.wxEVT_COMMAND_FIND_REPLACE:
            self.ReplaceNext(event)
        elif et == wx.wxEVT_COMMAND_FIND_REPLACE_ALL:
            self.ReplaceAll(event)
        else:
            self.console.write("unexpected eventType %s -- %s\n" % (et, event))

def OnFindClose(self, event):
        event.GetDialog().Destroy()

def OnShowFindReplace(self, event):
        data = wx.FindReplaceData()
        data.SetFlags(wx.FR_DOWN)
        dlg = wx.FindReplaceDialog(self, data, "Find & Replace", wx.FR_REPLACEDIALOG)
        dlg.data = data  # save a reference to it...
        dlg.Show(True)

def OnSelectToMark(self, event):
        insertionPoint = self.editor.GetInsertionPoint()
        if (self.mark < insertionPoint):
           self.editor.SetSelection(self.mark, insertionPoint)
           if beep:
              winsound.Beep(750, 250)
        elif (self.mark > insertionPoint):
           self.editor.SetSelection(insertionPoint, self.mark)
           if beep:
              winsound.Beep(1500, 250)

def AlternateFocus(self, event):
        self.ActuallyAlternateFocus()



# the following are not implemented yet and might be moved to different module

def duplicateline(self,e):
        self.control.SelectionDuplicate()

def lineup(self,e):
        self.control.MoveSelectedLinesUp()

def linedown(self,e):
        self.control.MoveSelectedLinesDown()

def uppercase(self,e):
        self.control.UpperCase()

def lowercase(self,e):
        self.control.LowerCase()

def unindent(self,e):
        self.control.BackTab()

def indent(self,e):
        self.control.Tab()

