# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx

def MakeStatsMenu(self):
        statsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_RCOMMAND, "Insert inline R command\tAlt+c", "insert an in-line R command", self.OnRCommand),
                 (ID_RCHUNK, "Insert R code chunk\tAlt+R", "insert standard R code chunk", self.OnRChunk),
                 (ID_RGRAPH, "Insert R code chunk for a graph\tAlt+G", "insert R code chunk for a graph", self.OnRGraph),
                 (ID_COMMENTOUT, "Comment out a selection\tAlt+q", "Comment out some selected text or insert the delimiters for a comment", self.OnRmdComment),
                 (ID_RLASSIGN, "Insert a left assignment\tCtrl+<", "insert R code for the left assignment <-", self.OnRLAssign),
                 (ID_RRASSIGN, "Insert a right assignment\tCtrl+>", "insert R code for the right assignment ->", self.OnRRAssign),
                 (ID_RPIPE, "Insert a pipe operator\tCtrl+Shift+P", "insert R code for the pipe operator %>%", self.OnRPipe)]:
            if id == None:
                statsMenu.AppendSeparator()
            else:
                item = statsMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(statsMenu, "Stats")  # Add the stats Menu to the MenuBar

