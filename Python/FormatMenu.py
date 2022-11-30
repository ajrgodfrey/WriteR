# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx


# format menu items
ID_BOLD = wx.Window.NewControlId()
ID_ITALIC = wx.Window.NewControlId()
ID_MATH = wx.Window.NewControlId()
ID_CODE = wx.Window.NewControlId()
ID_RNDBRK = wx.Window.NewControlId()
ID_SQBRK = wx.Window.NewControlId()
ID_CRLBRK = wx.Window.NewControlId()
ID_BRNDBRK = wx.Window.NewControlId()
ID_BSQBRK = wx.Window.NewControlId()
ID_BCRLBRK = wx.Window.NewControlId()



def MakeMenu(self):
        formatMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_BOLD, "Bold\tCtrl+B", "move to bold face font", self.OnBold),
                 (ID_ITALIC, "Italic\tCtrl+I", "move to italic face font", self.OnItalic),
                 (ID_CODE, "Code\tCtrl+`", "present using a typewriter font commonly seen when showing code", self.OnCode),
                 (ID_MATH, "Maths mode\tCtrl+4", "move text to maths mode", self.OnMath),
                 (ID_RNDBRK, "Round brackets\tAlt+Shift+(", "Wrap text in round () brackets", self.OnRoundBrack),
                 (ID_SQBRK, "Square brackets\tAlt+[", "Wrap text in square brackets", self.OnSquareBrack),
                 (ID_CRLBRK, "Curly brackets\tAlt+Shift+{", "Wrap text in curly brackets", self.OnCurlyBrack),
                 (ID_BRNDBRK, "Round brackets (math)\tAlt+Shift+)", "Wrap math in round () brackets", self.OnMathRoundBrack),
                 (ID_BSQBRK, "Square brackets (math)\tAlt+]", "Wrap math in square brackets", self.OnMathSquareBrack),
                 (ID_BCRLBRK, "Curly brackets (math)\tAlt+Shift+}", "Wrap math in curly brackets", self.OnMathCurlyBrack)]:
            if id == None:
                formatMenu.AppendSeparator()
            else:
                item = formatMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(formatMenu, "F&ormat")  # Add the format Menu to the MenuBar

