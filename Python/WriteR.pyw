# 2022.11.29 This file needs careful checking to remove content that should be totally independent of implementation
#    so that we can be sure it contains WriteR necessities, and nothing needed for WriteQuarto

# load modules
import wx 
import wx.adv
import sys
import re


# imports for all implementations
import IDTags # must come first
from IDTags  import *
# import FileMenuEvents # problems with this one
from EditMenuEvents import *
from ViewMenuEvents import *
from ViewMenu import *
from MarkdownEvents import * 
from MathInserts import *
import MyConsole 
from REvents import * 

# imports solely for WriteR
from RChunkEvents import * 
from HelpMenuEvents import * 
from RMarkdownEvents import *


# and yet more general imports
try:
    import winsound
except ImportError:
    print("Winsound module not found\n")
from wx.py.shell import Shell
from wx.aui import AuiManager, AuiPaneInfo
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT
from os.path import join, split, isdir, expanduser, realpath
from os import walk
from time import asctime, sleep
from six import iteritems

# set up global text strings
SBText = "This program is for editing R Markdown files"



#development options
print_option = False
display_rscript_cmd = True
beep = 'winsound' in sys.modules
system_tray = True



def dcf_dumps(data, sort_keys=True):
    string = ""
    for k, v in sorted(iteritems(data)):
        if v is None: v = 'None'
        string += "{:}: {:}\n".format(k, v.replace('\n', '\n '))
    return string


def dcf_loads(string):
    dictionary = {}
    last_key = None
    for l in string.split('\n'):
        if l == '': continue
        elif l[0] == ' ': dictionary[last_key] += "\n{:}".format(l[1:])
        else:
            k, v = l.split(': ')
            if v == 'None': v = None
            dictionary[k] = v
            last_key = k
    return dictionary


def printing(*args):
    if print_option: print (args)

class BashProcessThread(Thread):
    def __init__(self, flag, input_list, writelineFunc, doneFunc):
        Thread.__init__(self)
        busy = wx.BusyInfo("Please wait")
        self.flag = flag
        self.writelineFunc = writelineFunc
        self.setDaemon(True)
        self.input_list = input_list
        printing(input_list)
        try: 
            self.comp_thread = Popen(input_list, stdout=PIPE, stderr=STDOUT)
    
            if display_rscript_cmd:
               writelineFunc('\n'.join(input_list))
               writelineFunc('\n\n')
    
            for line in self.comp_thread.stdout:
                writelineFunc(line)
    
            returnCode = self.comp_thread.wait()
            del busy
            doneFunc(returnCode)
        except Exception as error:
            del busy
            doneFunc("\nCaught error {} for {}".format(error, input_list))

# get on with the program 
class MainWindow(wx.Frame):
    def __init__(self, parent=None, id=-1, title="", pos=wx.DefaultPosition,
                 size=(1200,700), style=wx.DEFAULT_FRAME_STYLE |
                                        wx.SUNKEN_BORDER |
                                        wx.CLIP_CHILDREN, filename="untitled.Rmd"):
        super(MainWindow, self).__init__(parent, id, title, pos, size, style)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self._mgr = AuiManager()
        self._mgr.SetManagedWindow(self)
        self.ChosenFontSize = 14
        self.font = wx.Font(self.ChosenFontSize, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        self.settings = {#'dirname': 'none',
#                         'templates': 'none',
                         'lastdir': '.',
                         'filename': 'none',
                         'newText': "Use WriteR to edit your R markdown files, perhaps by starting from a template file",
                         'RDirectory': "self.GetRDirectory()"}## couldn't see the function here so quoted it out
        if len(sys.argv) > 1:
            self.settings['lastdir'], self.settings['filename'] = split(realpath(sys.argv[-1]))
            self.filename = self.settings['filename']
            self.dirname = self.settings['lastdir']
            self.CreateExteriorWindowComponents()
            self.CreateInteriorWindowComponents()
            self.fileOpen(self.dirname, self.filename)
        elif self.settings['filename'] == 'none':
            self.filename = filename
            self.dirname = self.settings['lastdir']
            self.CreateExteriorWindowComponents()
            self.CreateInteriorWindowComponents()
            self.OnOpen(self)
            #  set the save flag to true if OnOpen is cancelled
        else:
            self.filename = self.settings['filename']
            self.dirname = self.settings['lastdir']
            self.CreateExteriorWindowComponents()
            self.CreateInteriorWindowComponents()
            self.fileOpen(self.dirname, self.filename)
        printing(self.settings['RDirectory'])
        self.x = 0
        # create a flag for exiting subthreads
        self.sub_flag = Event()
        self.comp_thread = None
        # for find and find/replace dialogues we need...
        self.Bind(wx.EVT_FIND, self.OnFind)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        self.Bind(wx.EVT_FIND_REPLACE, self.OnFind)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnFind)
        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)

    def CreateInteriorWindowComponents(self):
        self.editor = self.CreateTextCtrl(self.settings['newText'])
        self.console = MyConsole.MyConsole(self)
        self._mgr.AddPane(self.editor, AuiPaneInfo().Name('editor').
                          CenterPane().Hide())
        self._mgr.GetPane("editor").Show()
        self.editor.SetFocus()
        self.editor.SelectAll() 
        self.focusConsole = False 
        self.priorMatchCol = 0
        self.priorMatchRow = 0
        self._mgr.Update()
        # self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)


    def CreateExteriorWindowComponents(self):
        self.CreateMenu()
#        self.StatusBar() ## want this back
        self.SetTitle()

    def CreateMenu(self):
        menuBar = wx.MenuBar()  # create the menu bar object
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
                [(wx.ID_NEW, "New file\tCtrl+N", "Start a new file", self.OnNewFile),
                 (wx.ID_OPEN, "&Open\tCtrl+O", "Open an existing file", self.OnOpen),
                 (wx.ID_SAVE, "&Save\tCtrl+S", "Save the current file", self.OnSave),
                 (wx.ID_SAVEAS, "Save &As\tCtrl+Shift+S", "Save the file under a different name", self.OnSaveAs),
                 (None,) * 4,
                 (wx.ID_EXIT, "Quit && save\tCtrl+Q", "Saves the current file and closes the program", self.OnSafeExit)]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(fileMenu, "&File")  # Add the fileMenu to the MenuBar


        import EditMenu
        import ViewMenu
        import BuildMenuR
        import InsertMenu
        import FormatMenu
        import MathsMenu
        import StatsMenu
        import HelpMenu

        self.SetMenuBar(menuBar)  # Add the menuBar to the Frame

    def CreateTextCtrl(self, text):
        text = wx.TextCtrl(self, -1, text, wx.Point(0, 0), wx.Size(150, 90),
                           # wx.NO_BORDER | wx.TE_MULTILINE)
                           wx.TE_MULTILINE)

        text.SetFont(self.font)
        return text

    def SetTitle(self, *args, **kwargs):
        # MainWindow.SetTitle overrides wx.Frame.SetTitle, so we have to
        # call it using super:
        super(MainWindow, self).SetTitle("WriteR -  %s" % self.filename)

    # Helper methods:
    def defaultFileDialogOptions(self):
        return dict(message="Choose a file", defaultDir=self.dirname, wildcard="*.*")

    def askUserForFilename(self, **dialogOptions):
        dialog = wx.FileDialog(self, **dialogOptions)
        if dialog.ShowModal() == wx.ID_OK:
            userProvidedFilename = True
            self.filename = dialog.GetFilename()
            self.dirname = dialog.GetDirectory()
            self.SetTitle()  # Update the window title with the new filename
        else:
            userProvidedFilename = False
        dialog.Destroy()
        return userProvidedFilename

# Event handlers:
    # file menu events
    def OnOpen(self, event):
        if self.askUserForFilename(style=wx.FD_OPEN, **self.defaultFileDialogOptions()):
            self.fileOpen(self.dirname, self.filename)

    def fatalError(self, message):
        dialog = wx.MessageDialog(self, message, "Fatal Error", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
        self.OnExit()

    def fileOpen(self, dirname, filename):
        path = join(dirname.strip(), filename)
        try: 
           textfile = open(path, "r")
        except Exception as error:
           self.fatalError("Unable to open {} because {}".format(path, error))
           self.OnExit()

        try: 
           self.editor.SetValue(textfile.read())
        except Exception as error:
           self.fatalError("Unable to read {} into editor because {}".format(path, error))
           self.OnExit()

        try: 
           textfile.close()
        except Exception as error:
           self.fatalError("Unable to close {} because {}".format(path, error))
           self.OnExit()

    def OnNewFile(self, event):
        self.olddirname = self.dirname
        self.dirname = ".\\templates"
        self.OnOpen(event)
        self.dirname = self.olddirname
        if self.filename == "Blank.Rmd":
            self.editor.WriteText("% file created on " + asctime() + "\n\n")
        self.OnSaveAs(event)

    def OnSaveAs(self, event):
        if self.askUserForFilename(defaultFile=self.filename, style=wx.FD_SAVE, **self.defaultFileDialogOptions()):
            self.OnSave(event)

    def OnSave(self, event):
        textfile = open(join(self.dirname, self.filename), "w")
        textfile.write(self.editor.GetValue())
        textfile.close()

    def OnExit(self):
        if self._mgr:
           self._mgr.UnInit()
        self.Close()  # Close the main window.

    def OnSafeExit(self, event):
        self.OnSave(event)
        self.OnExit()






# general events
    def StartThread(self, input_object):
        if self.sub_flag.isSet(): return
        if self.comp_thread is not None:
            self.sub_flag.set()
            while self.comp_thread.isAlive():
                sleep(1)
            self.sub_flag.clear()
            self.console.Reset()
        self.comp_thread = BashProcessThread(self.sub_flag, input_object, self.console.CreateWriteText, self.console.DoneFunc)
        self.comp_thread.start()




    def OnClose(self, event):
        self.settings['filename'] = self.filename
        self.settings['lastdir'] = self.dirname
        if event.CanVeto() and self.editor.IsModified():
            hold = wx.MessageBox("Would you like to save your work?",
                                 "Save before exit?",
                                 wx.ICON_QUESTION | wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT)
            if hold == wx.YES:
                self.OnSave(event)
                self.Destroy()
            elif hold == wx.NO:
                self.Destroy()
            else:
                event.Veto()
        else:
            self.Destroy()


    def GetStartPosition(self):
        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))
        return wx.Point(pt.x + x, pt.y + x)

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

    def SetFocusConsole(self, toConsole):
        if toConsole != self.focusConsole:
           self.ActuallyAlternateFocus()

    def AlternateFocus(self, event):
        self.ActuallyAlternateFocus()

    def TellUser(self, text):
        self.SetStatusText(text)
        if system_tray:
           try:
              nm = wx.adv.NotificationMessage()
              nm.SetMessage(text)
              nm.SetParent(self)
              nm.SetTitle("")
              nm.SetFlags(wx.ICON_INFORMATION)
              nm.Show(1)
           except Exception as error:
              print ("Problem setting notification {}".format(error))
              pass

    def OnWordCount(self, event):
        text=self.editor.GetValue()
        word_count=len(text.split())
        (on, x, y) = self.editor.PositionToXY(self.editor.GetInsertionPoint())
        line_count = self.editor.GetNumberOfLines()
        markdownState = RMarkdownEvents.CurrentMarkdown(self)
        self.TellUser("Line {}/{}. WordCount {}. State {}".format(y, line_count, word_count, markdownState))

    def ActuallyAlternateFocus(self):
        if self.focusConsole:
           self.editor.SetFocus()
           self.TellUser('editor')
           if beep:
              winsound.Beep(2000, 250)
        else:
           self.console.SetFocus()
           self.TellUser('console')
           if beep:
              winsound.Beep(3000, 250)
        self.focusConsole = not self.focusConsole

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

    def OnShowFindReplace(self, event):
        data = wx.FindReplaceData()
        data.SetFlags(wx.FR_DOWN)
        dlg = wx.FindReplaceDialog(self, data, "Find & Replace", wx.FR_REPLACEDIALOG)
        dlg.data = data  # save a reference to it...
        dlg.Show(True)

    def ComputeFindString(self, event):
        if event.GetFlags() & wx.FR_WHOLEWORD:
           return "".join([r"\b", re.escape(event.GetFindString()), r"\b"])
        else:
           return "".join([re.escape(event.GetFindString())])

    def ComputeReFlags(self, event):
        if event.GetFlags() & wx.FR_MATCHCASE:
           return 0
        else:
           return re.IGNORECASE

    def ComputeReplacementString(self, event):
        return event.GetReplaceString()

    def MoveTo(self, row, col):
       self.priorMatchRow = row
       self.priorMatchCol = col
       message = "Line {} Col {}".format(row, col)
       self.TellUser(message)
       position = self.editor.XYToPosition(col, row)
       self.editor.SetInsertionPoint(position)
       self.editor.ShowPosition(position)
       if beep:
          winsound.Beep(1000, 250)

    def FindFrom(self, currentColumn, currentRow, reverseDirection):
        # Special logic for checking just part of current line
        currentLine = self.editor.GetLineText(currentRow)
        searchForward = self.forward != reverseDirection
        if searchForward:
           matchObject = self.regex.search(currentLine[currentColumn+1:])
           if matchObject:
               self.MoveTo(currentRow, currentColumn + 1 + matchObject.start())
               return
        else:
           matchObject = self.regex.search(currentLine[:currentColumn])
           if matchObject:
               for matchObject in self.regex.finditer(currentLine[:currentColumn]):
                   pass
               self.MoveTo(currentRow, matchObject.start())
               return

        # General case for checking whole lines
        if searchForward:
           lineRange = range(currentRow+1, self.editor.GetNumberOfLines())
        else:
           lineRange = reversed(range(0, currentRow)) 

        for i in lineRange:
            line = self.editor.GetLineText(i)
            matchObject = self.regex.search(line)
            if matchObject:
               if not searchForward:
                  for matchObject in self.regex.finditer(line):
                      pass

               self.MoveTo(i, matchObject.start())
               return

        if beep:
           winsound.Beep(500, 500)

    def ReplaceNext(self, event):
        return

    def ReplaceAll(self, event):
        findString = self.ComputeFindString(event)
        reFlags = self.ComputeReFlags(event)
        replaceString = self.ComputeReplacementString(event)
        oldText = self.editor.GetValue()
        newText = re.sub(findString, replaceString, oldText, flags=reFlags)

        insertionPoint = self.editor.GetInsertionPoint()
        self.editor.SetValue(newText)
        self.editor.SetInsertionPoint(insertionPoint)

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

# mandatory lines to get program running.
if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    app.MainLoop()
