# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx
from REvents import *
import REvents
from RChunkEvents import *
import RChunkEvents
from RMarkdownEvents import *
import RMarkdownEvents 


def MakeStatsMenu(self, MainMenu):
        statsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 ("ID", "Insert inline R command\tAlt+c", "insert an in-line R command", OnRCommand),
                 ("ID", "Insert R code chunk\tAlt+R", "insert standard R code chunk", OnRChunk),
                 ("ID", "Insert R code chunk for a graph\tAlt+G", "insert R code chunk for a graph", OnRGraph),
                 ("ID", "Comment out a selection\tAlt+q", "Comment out some selected text or insert the delimiters for a comment", OnRmdComment),
                 ("ID", "Insert a left assignment\tCtrl+<", "insert R code for the left assignment <-", OnRLAssign),
                 ("ID", "Insert a right assignment\tCtrl+>", "insert R code for the right assignment ->", OnRRAssign),
                 ("ID", "Insert a pipe operator\tCtrl+Shift+P", "insert R code for the pipe operator %>%", OnRPipe)]:
            if id == None:
                statsMenu.AppendSeparator()
            else:
                item = statsMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        MainMenu.Append(statsMenu, "Stats")  # Add the stats Menu to the MenuBar

