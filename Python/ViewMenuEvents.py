# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx


# view menu events

def ToggleStatusBar(self, event):
        if self.statusbar.IsShown():
            self.statusbar.Hide()
        else:
            self.statusbar.Show()
            self.SetStatusText(SBText)

def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-5, -2, -1])
        self.SetStatusText(SBText)
       
def OnIncreaseFontSize(self, event):
        self.font.SetPointSize(self.font.GetPointSize()+1)
        self.UpdateUI()

def OnDecreaseFontSize(self, event):
        self.font.SetPointSize(self.font.GetPointSize()-1)
        self.UpdateUI()

def UpdateUI(self):
        self.editor.SetFont(self.font)
        #self.editor.SetForegroundColour(self.curClr)
        #self.ps.SetLabel(str(self.font.GetPointSize()))
        #self.family.SetLabel(self.font.GetFamilyString())
        #self.style.SetLabel(self.font.GetStyleString())
        #self.weight.SetLabel(self.font.GetWeightString())
        #self.face.SetLabel(self.font.GetFaceName())
        #self.nfi.SetLabel(self.font.GetNativeFontInfo().ToString())
        self.Layout()


def OnSelectFont(self, evt):
        data = wx.FontData()
        data.EnableEffects(False)
        #data.SetColour(self.curClr)         # set colour
        data.SetInitialFont(self.font)
        dlg = wx.FontDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            data = dlg.GetFontData()
            font = data.GetChosenFont()
            #colour = data.GetColour()
            self.font = font
            #self.curClr = colour
            self.UpdateUI()
        # Don't destroy the dialog until you get everything you need from the
        # dialog!
        dlg.Destroy()

