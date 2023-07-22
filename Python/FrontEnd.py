# import external modules
import wx 
import wx.adv
import sys
import re
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


# import our modules
# first bring in modules used for all versions
from GlobalSettings import *
from IDTags import *
import EditMenuEvents
import ViewMenuEvents
import MyConsole
import RMarkdownEvents 
import RCodeEvents
import MarkdownEvents 
import MathInserts 

# then modules for specific versions (conditioning to come later)
import HelpMenuEventsQ
import HelpMenuEventsR
import HelpMenuEventsS



print_option = False
display_rscript_cmd = True
beep = 'winsound' in sys.modules
system_tray = True

# set up some ID tags
ID_BUILD = wx.NewIdRef()
ID_KNIT2HTML = wx.NewIdRef()
ID_KNIT2PDF = wx.NewIdRef()
ID_SETTINGS = wx.NewIdRef()

ID_FINDONLY = wx.NewIdRef()
ID_FINDNEXT = wx.NewIdRef()
ID_FINDPREV = wx.NewIdRef()
ID_FINDREPLACE = wx.NewIdRef()
ID_GOTO  = wx.NewIdRef()
ID_WORDCOUNT = wx.NewIdRef()

ID_SETMARK = wx.NewIdRef()
ID_SELECTTOMARK = wx.NewIdRef()

ID_ALTERNATE_FOCUS = wx.NewIdRef()



D_RCOMMAND = wx.NewIdRef()
ID_COMMENTOUT = wx.NewIdRef()





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

ID_DIRECTORY_CHANGE = wx.NewIdRef()
ID_CRAN = wx.NewIdRef()
ID_R_PATH = wx.NewIdRef()
ID_BUILD_COMMAND = wx.NewIdRef()
ID_KNIT2HTML_COMMAND = wx.NewIdRef()
ID_KNIT2PDF_COMMAND = wx.NewIdRef()
ID_NEWTEXT = wx.NewIdRef()


# get on with the program 
class MainWindow(wx.Frame):
    def __init__(self, parent=None, id=-1, title="", pos=wx.DefaultPosition,
                 size=(1200,700), style=wx.DEFAULT_FRAME_STYLE |
                                        wx.SUNKEN_BORDER |
                                        wx.CLIP_CHILDREN, filename="untitled."+FileExtension):
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
                         'newText': StartingText, # set in GlobalSettings modules
                         'RDirectory': self.GetRDirectory()}
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
        self.StatusBar()
        self.SetTitle()

    def CreateMenu(self):
        fileMenu = wx.Menu()
        for id, label, helpText, handler in \
                [(wx.ID_NEW, "New file\tCtrl+N", "Start a new file", self.OnNewFile),
                 (wx.ID_OPEN, "&Open\tCtrl+O", "Open an existing file", self.OnOpen),
                 (wx.ID_SAVE, "&Save\tCtrl+S", "Save the current file", self.OnSave),
                 (wx.ID_SAVEAS, "Save &As\tCtrl+Shift+S", "Save the file under a different name", self.OnSaveAs),
                 (None,) * 4,
                 (wx.ID_EXIT, "Quit && save\tCtrl+Q", "Saves the current file and closes the program", self.OnSafeExit)]:
            if label == None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar = wx.MenuBar()  # create the menu bar object
        menuBar.Append(fileMenu, "&File")  # Add the fileMenu to the MenuBar

        editMenu = wx.Menu()
        for id, label, helpText, handler in \
                [(wx.ID_CUT, "Cu&t\tCtrl+X", "Cut highlighted text to clipboard", self.OnCut),
                 (wx.ID_COPY, "&Copy\tCtrl+C", "Copy highlighted text to clipboard", self.OnCopy),
                 (wx.ID_PASTE, "&Paste\tCtrl+V", "Paste text from clipboard", self.OnPaste),
                 (wx.ID_SELECTALL, "Select all\tCtrl+A", "Highlight entire text", self.OnSelectAll),
                 (wx.ID_DELETE, "&Delete", "Delete highlighted text", self.OnDelete),
                 (ID_WORDCOUNT, "Word count\tCtrl+w", "get a word count of the entire text", self.OnWordCount),
                 (None,) * 4,
                 (ID_FINDONLY, "Find\tCtrl+F", "Open a standard find dialog box", self.OnShowFind),
                 (ID_FINDNEXT, "FindNext\tF3", "FindNext", self.F3Next),
                 (ID_FINDPREV, "FindPrevious\tShift+F3", "FindPrev", self.ShiftF3Previous),
                 (ID_GOTO, "Go to line\tCtrl+g", "Open a dialog box to choose a line number", self.OnGoToLine),
                 (ID_FINDREPLACE, "Find/replace\tCtrl+H", "Open a find/replace dialog box", self.OnShowFindReplace),
                 (ID_SETMARK, "Set Mark\tCtrl+SPACE", "Set Mark", self.OnSetMark),
                 (ID_SELECTTOMARK , "Select To Mark\tAlt+Ctrl+SPACE", "Select To Mark", self.OnSelectToMark),
                 (ID_ALTERNATE_FOCUS , "Alternate Focus\tF4", "Alternate Focus", self.AlternateFocus),
                 (None,) * 4,
                 (ID_SETTINGS, 'Settings', "Setup the editor to your liking", self.OnSettings)]:
            if label == None:
                editMenu.AppendSeparator()
            else:
                item = editMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(editMenu, "&Edit")  # Add the editMenu to the MenuBar

        viewMenu = wx.Menu()
        self.ShowStatusBar = viewMenu.Append(wx.ID_ANY, "Show status bar", 
            "Show Status bar", kind=wx.ITEM_CHECK)
        viewMenu.Check(self.ShowStatusBar.GetId(), True)
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.ShowStatusBar)
        self.IncreaseFont = viewMenu.Append(wx.ID_ANY, "Increase the font size\tCtrl+=", "Increase the font size")
        self.Bind(wx.EVT_MENU, self.OnIncreaseFontSize, self.IncreaseFont) 
        self.DecreaseFont = viewMenu.Append(wx.ID_ANY, "Decrease the font size\tCtrl+-", "Decrease the font size")
        self.Bind(wx.EVT_MENU, self.OnDecreaseFontSize, self.DecreaseFont) 
        self.ChooseFont = viewMenu.Append(wx.ID_ANY, "Choose font\tCtrl+D", "Choose the font size and other details")
        self.Bind(wx.EVT_MENU, self.OnSelectFont, self.ChooseFont )
        menuBar.Append(viewMenu, "View")  # Add the view Menu to the MenuBar

        buildMenu = wx.Menu()
        self.Render = buildMenu.Append(wx.ID_ANY, "Render the document\tF5", "Use the rmarkdown package to render the current file")
        self.Bind(wx.EVT_MENU, self.OnRenderNull, self.Render)  
      # Create render menu for WriteR
        if AppName == "WriteR":
            renderMenu = wx.Menu()
            self.ChooseRenderNull = renderMenu.Append(wx.ID_ANY, "Render using defaults", 
                "Use the rmarkdown package and render function to create HTML or only the first of multiple formats specified in YAML header", wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.OnSelectRenderNull, self.ChooseRenderNull)
            self.ChooseRenderHtml = renderMenu.Append(wx.ID_ANY, "Render into HTML only", 
                "Use the rmarkdown package and render function to create HTML", wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.OnSelectRenderHtml, self.ChooseRenderHtml) 
            self.ChooseRenderWord = renderMenu.Append(wx.ID_ANY, "Render into Microsoft Word only", 
                "Use the rmarkdown package and render function to create Microsoft Word", wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.OnSelectRenderWord, self.ChooseRenderWord) 
            self.ChooseRenderSlidy = renderMenu.Append(wx.ID_ANY, "Render into slidy only", 
                "Use the rmarkdown package and render function to create a slidy presentation", wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.OnSelectRenderSlidy, self.ChooseRenderSlidy) 
            self.ChooseRenderPdf = renderMenu.Append(wx.ID_ANY, "Render into pdf only", 
                "Use the rmarkdown package and render function to create pdf", wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.OnSelectRenderPdf, self.ChooseRenderPdf) 
            self.ChooseRenderAll = renderMenu.Append(wx.ID_ANY, "Render into all specified formats", 
                "Use the rmarkdown package and render function to create multiple output documents", wx.ITEM_RADIO)
            self.Bind(wx.EVT_MENU, self.OnSelectRenderAll, self.ChooseRenderAll) 
            buildMenu.AppendSubMenu(-1, "Set render process to...", renderMenu) # Add the render Menu as a submenu to the build menu
            for label, helpText, handler in \
                [
                 ("Knit to html\tF6", "Knit the script to HTML", self.OnKnit2html),
                 ("Knit to pdf\tShift+F6", "Knit the script to a pdf file using LaTeX", self.OnKnit2pdf)]:
                if label == None:
                    buildMenu.AppendSeparator()
                else:
                    item = buildMenu.Append(wx.ID_ANY, label, helpText)
                    self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(buildMenu, "Build")  # Add the Build Menu to the MenuBar

        formatMenu = wx.Menu()
        for label, helpText, handler, whichApp  in \
                [
                 ("Bold\tCtrl+B", "move to bold face font", self.OnBold, "md"),
                 ("Italic\tCtrl+I", "move to italic face font", self.OnItalic, "md"),
                 ("Code\tCtrl+`", "present using a typewriter font commonly seen when showing code", self.OnCode, "md"),
                 ("Maths mode\tCtrl+4", "move text to maths mode", self.OnMath, "md"),
                 ("Round brackets\tAlt+Shift+(", "Wrap text in round () brackets", self.OnRoundBrack, "all"),
                 ("Square brackets\tAlt+[", "Wrap text in square brackets", self.OnSquareBrack, "all"),
                 ("Curly brackets\tAlt+Shift+{", "Wrap text in curly brackets", self.OnCurlyBrack, "all"),
                 ("Round brackets (math)\tAlt+Shift+)", "Wrap math in round () brackets", self.OnMathRoundBrack, "md"),
                 ("Square brackets (math)\tAlt+]", "Wrap math in square brackets", self.OnMathSquareBrack, "md"),
                 ("Curly brackets (math)\tAlt+Shift+}", "Wrap math in curly brackets", self.OnMathCurlyBrack, "md")]:
            if label == None:
                formatMenu.AppendSeparator()
            elif AppName!="ScriptR" and whichApp=="md":
                item = formatMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
            elif whichApp=="all":
                item = formatMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(formatMenu, "format")  # Add the format Menu to the MenuBar


        insertMenu = wx.Menu()
        headingsMenu = wx.Menu()
        for label, helpText, handler in \
                [
                 ("level &1\tAlt+1", "insert heading level 1", self.OnHeading1), 
                 ("level &2\tAlt+2", "insert heading level 2", self.OnHeading2), 
                 ("level &3\tAlt+3", "insert heading level 3", self.OnHeading3), 
                 ("level &4\tAlt+4", "insert heading level 4", self.OnHeading4), 
                 ("level &5\tAlt+5", "insert heading level 5", self.OnHeading5), 
                 ("level &6\tAlt+6", "insert heading level 6", self.OnHeading6)]:
            item = headingsMenu.Append(wx.ID_ANY, label, helpText)
            self.Bind(wx.EVT_MENU, handler, item)
        insertMenu.Append(-1, "Heading", headingsMenu)
        for label, helpText, handler, whichApp  in \
                [
                 ("header/preamble\tCtrl+Shift+H", "", self.OnAddHeadBlock, "md"),
                 ("Separator\tCtrl+Shift+-", "", self.OnAddSeparator, "all"),
                 ("URL\tCtrl+Shift+U", "", self.OnAddURL, "md"),
                 ("e-mail\tCtrl+Shift+E", "", self.OnAddEMail, "md"),
                 ("Figure\tCtrl+Shift+F", "", self.OnAddFigure, "md"),
                 ("Reference\tCtrl+Shift+R", "", self.OnAddReference, "md")]:
            if label == None:
                insertMenu.AppendSeparator()
            elif AppName!="ScriptR" and whichApp=="md":
                item = insertMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
            elif whichApp=="all":
                item = insertMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(insertMenu, "insert")  # Add the insert Menu to the MenuBar

        CodeMenu = wx.Menu()
        for label, helpText, handler in \
                [
                 ("Insert a left assignment\tCtrl+<", "insert R code for the left assignment <-", self.OnRLAssign),
                 ("Insert a right assignment\tCtrl+>", "insert R code for the right assignment ->", self.OnRRAssign),
                 ("Insert a pipe operator\tCtrl+Shift+P", "insert R code for the pipe operator |>", self.OnRPipe)]:
            if label == None:
                CodeMenu.AppendSeparator()
            else:
                item = CodeMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(CodeMenu, "Code")  # Add the Code Menu to the MenuBar

        # Only use the Maths menu for WriteR and QuartoWriteR
        mathsMenu = wx.Menu()
        symbolsMenu = wx.Menu()
        for label, helpText, handler in \
                [
                ("infinity\tCtrl+Shift+I", "insert infinity", self.OnSymbol_infinity), 
                 ("times\tCtrl+Shift+*", "insert times", self.OnSymbol_times), 
                 ("partial derivative\tCtrl+Shift+D", "insert partial", self.OnSymbol_partial), 
                 ("plus or minus\tCtrl+Shift+=", "insert plus or minus sign", self.OnSymbol_plusminus), 
                 ("minus or plus\tCtrl+Shift+-", "insert minus or plus sign", self.OnSymbol_minusplus), 
                 ("less than or equal\tCtrl+Shift+<", "insert less than or equal sign", self.OnSymbol_leq), 
                 ("greater than or equal \tCtrl+Shift+>", "insert greater than or equal sign", self.OnSymbol_geq), 
                 ("not equal\tCtrl+Shift+!", "insert not equal sign", self.OnSymbol_neq), 
                 ("Left Parenthesis\tCtrl+9", "insert variable size left parenthesis", self.OnSymbol_LeftParen), 
                 ("Right Parenthesis\tCtrl+0", "insert variable size right parenthesis", self.OnSymbol_RightParen), 
                 ("Left Square bracket\tCtrl+[", "insert variable size left square bracket", self.OnSymbol_LeftSquare), 
                 ("Right Square bracket\tCtrl+]", "insert variable size right square bracket", self.OnSymbol_RightSquare), 
                 ("Left Curly bracket\tCtrl+Shift+{", "insert variable size left curly bracket", self.OnSymbol_LeftCurly), 
                 ("Right Curly bracket\tCtrl+Shift+}", "insert variable size right curly bracket", self.OnSymbol_RightCurly)]:
            if label == None:
                symbolsMenu.AppendSeparator()
            else:
                item = symbolsMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.Append(-1, "Symbols", symbolsMenu)
        structuresMenu = wx.Menu()
        for label, helpText, handler in \
                [
                 ("Square root\tAlt+Ctrl+Shift+R", "insert a square root", self.OnSquareRoot), 
                 ("bar \tCtrl+Shift+B", "insert a bar operator", self.OnMathBar), 
                 ("Absolute values\tCtrl+Shift+A", "insert left and right absolute value delimiters", self.OnAbsVal), 
                 ("Fraction\tCtrl+Shift+/", "insert a fraction", self.OnFraction), 
                 ("Summation\tAlt+Ctrl+Shift+S", "insert a summation", self.OnSummation), 
                 ("Integral\tAlt+Ctrl+Shift+I", "insert an integral", self.Onintegral), 
                 ("Product\tAlt+Ctrl+Shift+P", "insert a product", self.OnProduct), 
                 ("Limit\tAlt+Ctrl+Shift+L", "insert a limit", self.OnLimit), 
                 ("Double summation\tAlt+Ctrl+Shift+D", "insert a double summation", self.OnDoubleSummation), 
                 ("Double integral", "insert a double integral", self.OnDoubleIntegral)]:
            if label == None:
                structuresMenu.AppendSeparator()
            else:
                item = structuresMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.Append(-1, "Structures", structuresMenu)# Add the structures Menu as a submenu to the main menu
        GreekMenu = wx.Menu()
        for label, helpText, handler in \
                [
                 ("alpha\tAlt+Shift+A", "insert greek letter alpha", self.OnGreek_alpha), 
                 ("beta\tAlt+Shift+B", "insert greek letter beta", self.OnGreek_beta), 
                 ("gamma\tAlt+Shift+G", "insert greek letter gamma", self.OnGreek_gamma), 
                 ("delta\tAlt+Shift+D", "insert greek letter delta", self.OnGreek_delta), 
                 ("epsilon\tAlt+Shift+E", "insert greek letter epsilon", self.OnGreek_epsilon), 
                 ("epsilon (variant)\tAlt+Shift+V", "insert variant of greek letter epsilon", self.OnGreek_varepsilon), 
                 ("zeta\tAlt+Shift+Z", "insert greek letter zeta", self.OnGreek_zeta), 
                 ("eta\tAlt+Shift+W", "insert greek letter eta", self.OnGreek_eta), 
                 ("theta\tAlt+Shift+H", "insert greek letter theta", self.OnGreek_theta), 
                 ("theta (variant)\tAlt+Shift+/", "insert variant of greek letter theta", self.OnGreek_vartheta), 
                 ("iota\tAlt+Shift+I", "insert greek letter iota", self.OnGreek_iota), 
                 ("kappa\tAlt+Shift+K", "insert greek letter kappa", self.OnGreek_kappa), 
                 ("lambda\tAlt+Shift+L", "insert greek letter lambda", self.OnGreek_lambda), 
                 ("mu\tAlt+Shift+M", "insert greek letter mu", self.OnGreek_mu), 
                 ("nu\tAlt+Shift+N", "insert greek letter nu", self.OnGreek_nu), 
                 ("xi\tAlt+Shift+X", "insert greek letter xi", self.OnGreek_xi), 
                 ("omicron\tAlt+Shift+O", "insert greek letter omicron", self.OnGreek_omicron), 
                 ("pi\tAlt+Shift+P", "insert greek letter pi", self.OnGreek_pi), 
                 ("rho\tAlt+Shift+R", "insert greek letter rho", self.OnGreek_rho), 
                 ("sigma\tAlt+Shift+S", "insert greek letter sigma", self.OnGreek_sigma), 
                 ("tau\tAlt+Shift+T", "insert greek letter tau", self.OnGreek_tau), 
                 ("upsilon\tAlt+Shift+U", "insert greek letter upsilon", self.OnGreek_upsilon), 
                 ("phi\tAlt+Shift+F", "insert greek letter phi", self.OnGreek_phi), 
                 ("chi\tAlt+Shift+C", "insert greek letter chi", self.OnGreek_chi), 
                 ("psi\tAlt+Shift+Y", "insert greek letter psi", self.OnGreek_psi), 
                 ("omega\tAlt+Shift+.", "insert greek letter omega", self.OnGreek_omega)]:
            if label == None:
                GreekMenu.AppendSeparator()
            else:
                item = GreekMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.Append(-1, "Greek letters", GreekMenu)
        if(AppName != "ScriptR"):
            menuBar.Append(mathsMenu, "Maths")  # Add the maths Menu to the MenuBar

        helpMenu = wx.Menu()
        for id, label, helpText, handler in \
                [(wx.ID_ABOUT, "About", "Information about this program", self.OnAbout)]:
            if label == None:
                fileMenu.AppendSeparator()
            else:
                item = helpMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(helpMenu, "&Help")  # Add the helpMenu to the MenuBar
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
        super(MainWindow, self).SetTitle(AppName + " -  %s" % self.filename)

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

    # file menu events
    def OnOpen(self, event):
        if self.askUserForFilename(style=wx.FD_OPEN, **self.defaultFileDialogOptions()):
            self.fileOpen(self.dirname, self.filename)

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


    # Build Menu events # conditioning needed for apps is done in RMarkdownEvents.py or in menu construction
    OnRenderNull = RMarkdownEvents.OnRenderNull
    OnProcess = RMarkdownEvents.OnProcess
    OnRenderHtml = RMarkdownEvents.OnRenderHtml
    OnRenderAll = RMarkdownEvents.OnRenderAll 
    OnRenderWord = RMarkdownEvents.OnRenderWord 
    OnRenderPdf = RMarkdownEvents.OnRenderPdf 
    OnRenderSlidy = RMarkdownEvents.OnRenderSlidy 
    OnKnit2html = RMarkdownEvents.OnKnit2html 
    OnKnit2pdf = RMarkdownEvents.OnKnit2pdf 
    OnSelectRenderNull = RMarkdownEvents.OnSelectRenderNull 
    OnSelectRenderHtml = RMarkdownEvents.OnSelectRenderHtml 
    OnSelectRenderAll = RMarkdownEvents.OnSelectRenderAll 
    OnSelectRenderWord = RMarkdownEvents.OnSelectRenderWord 
    OnSelectRenderPdf = RMarkdownEvents.OnSelectRenderPdf 
    OnSelectRenderSlidy = RMarkdownEvents.OnSelectRenderSlidy 
    CurrentMarkdown= RMarkdownEvents.CurrentMarkdown

    # Code Menu events
    OnRPipe = RCodeEvents.OnRPipe
    OnRLAssign = RCodeEvents.OnRLAssign
    OnRRAssign = RCodeEvents.OnRRAssign

    # MathInserts are all LaTeX input for math mode; they are all included even though not used by ScriptR
    OnSymbol_infinity = MathInserts.OnSymbol_infinity
    OnSymbol_plusminus = MathInserts.OnSymbol_plusminus
    OnSymbol_minusplus = MathInserts.OnSymbol_minusplus
    OnSymbol_geq = MathInserts.OnSymbol_geq
    OnSymbol_leq = MathInserts.OnSymbol_leq
    OnSymbol_neq = MathInserts.OnSymbol_neq
    OnSymbol_times = MathInserts.OnSymbol_times
    OnSymbol_partial = MathInserts.OnSymbol_partial
    OnSymbol_LeftParen = MathInserts.OnSymbol_LeftParen
    OnSymbol_RightParen = MathInserts.OnSymbol_RightParen
    OnSymbol_LeftSquare = MathInserts.OnSymbol_LeftSquare
    OnSymbol_RightSquare = MathInserts.OnSymbol_RightSquare
    OnSymbol_LeftCurly = MathInserts.OnSymbol_LeftCurly
    OnSymbol_RightCurly = MathInserts.OnSymbol_RightCurly
    OnAbsVal = MathInserts.OnAbsVal
    OnMathBar = MathInserts.OnMathBar
    OnSquareRoot = MathInserts.OnSquareRoot
    OnFraction = MathInserts.OnFraction
    OnSummation = MathInserts.OnSummation
    Onintegral = MathInserts.Onintegral
    OnProduct = MathInserts.OnProduct
    OnLimit = MathInserts.OnLimit
    OnDoubleSummation = MathInserts.OnDoubleSummation
    OnDoubleIntegral = MathInserts.OnDoubleIntegral
    OnGreek_alpha = MathInserts.OnGreek_alpha
    OnGreek_beta = MathInserts.OnGreek_beta
    OnGreek_gamma = MathInserts.OnGreek_gamma
    OnGreek_delta = MathInserts.OnGreek_delta
    OnGreek_epsilon = MathInserts.OnGreek_epsilon
    OnGreek_varepsilon = MathInserts.OnGreek_varepsilon
    OnGreek_zeta = MathInserts.OnGreek_zeta
    OnGreek_eta = MathInserts.OnGreek_eta
    OnGreek_theta = MathInserts.OnGreek_theta
    OnGreek_vartheta = MathInserts.OnGreek_vartheta
    OnGreek_iota = MathInserts.OnGreek_iota
    OnGreek_kappa = MathInserts.OnGreek_kappa
    OnGreek_lambda = MathInserts.OnGreek_lambda
    OnGreek_mu = MathInserts.OnGreek_mu
    OnGreek_nu = MathInserts.OnGreek_nu
    OnGreek_xi = MathInserts.OnGreek_xi
    OnGreek_omicron = MathInserts.OnGreek_omicron
    OnGreek_pi = MathInserts.OnGreek_pi
    OnGreek_rho = MathInserts.OnGreek_rho
    OnGreek_sigma = MathInserts.OnGreek_sigma
    OnGreek_tau = MathInserts.OnGreek_tau
    OnGreek_upsilon = MathInserts.OnGreek_upsilon
    OnGreek_phi = MathInserts.OnGreek_phi
    OnGreek_chi = MathInserts.OnGreek_chi
    OnGreek_psi = MathInserts.OnGreek_psi
    OnGreek_omega = MathInserts.OnGreek_omega

    OnMathRoundBrack = MathInserts.OnMathRoundBrack
    OnMathCurlyBrack = MathInserts.OnMathCurlyBrack
    OnMathSquareBrack = MathInserts.OnMathSquareBrack


    # help menu events
    if(AppName == "ScriptR"):
        OnAbout = HelpMenuEventsS.OnAbout
    elif(AppName == "WriteR"):
        OnAbout = HelpMenuEventsR.OnAbout
    else:
        OnAbout = HelpMenuEventsQ.OnAbout




    # edit menu events ##checking some required
    OnSelectAll = EditMenuEvents.OnSelectAll
    OnDelete = EditMenuEvents.OnDelete
    OnPaste = EditMenuEvents.OnPaste
    OnCopy = EditMenuEvents.OnCopy
    OnCut = EditMenuEvents.OnCut
    OnGoToLine = EditMenuEvents.OnGoToLine
    OnSettings = EditMenuEvents.OnSettings

    # view menu events 
    ToggleStatusBar= ViewMenuEvents.ToggleStatusBar
    StatusBar = ViewMenuEvents.StatusBar
    OnIncreaseFontSize=  ViewMenuEvents.OnIncreaseFontSize
    OnDecreaseFontSize = ViewMenuEvents.OnDecreaseFontSize
    UpdateUI = ViewMenuEvents.UpdateUI
    OnSelectFont = ViewMenuEvents.OnSelectFont


    # format/Insert menu events 
    OnSquareBrack = MarkdownEvents.OnSquareBrack
    OnCurlyBrack = MarkdownEvents.OnCurlyBrack
    OnRoundBrack = MarkdownEvents.OnRoundBrack
    OnItalic = MarkdownEvents.OnItalic
    OnBold = MarkdownEvents.OnBold
    OnCode = MarkdownEvents.OnCode
    OnMath = MarkdownEvents.OnMath
    OnAddHeadBlock = MarkdownEvents.OnAddHeadBlock
    OnAddURL = MarkdownEvents.OnAddURL
    OnAddReference = MarkdownEvents.OnAddReference
    OnAddEMail = MarkdownEvents.OnAddEMail
    OnAddFigure = MarkdownEvents.OnAddFigure
    OnHeading1 = MarkdownEvents.OnHeading1
    OnHeading2 = MarkdownEvents.OnHeading2
    OnHeading3 = MarkdownEvents.OnHeading3
    OnHeading4 = MarkdownEvents.OnHeading4
    OnHeading5 = MarkdownEvents.OnHeading5
    OnHeading6 = MarkdownEvents.OnHeading6
    OnAddSeparator = MarkdownEvents.OnAddSeparator

    # processing events (all apps)
#move    GetRDirectory = GetRDirectory
    def GetRDirectory(self):
        def splitter(path, interest):
            look = split(path)
            if interest in look[1]:
                return look[1]
            if len(look[0]) == 0:
                return None
            return splitter(look[0], interest)
        rscript = 'Rscript.exe'
        warn = "Cannot find {} in default install location.".format(rscript)
        version = "R-0.0.0"
        choice = None
        if "No settings file reference to settings":
            if isdir("C:\\Program Files\\R"):
                hold = "C:\\Program Files\\R"
            elif isdir("C:\\Program Files (x86)\\R"):
                hold = "C:\\Program Files (x86)\\R"
            else:
                print (warn); return
            options = [join(r, rscript) for r, d, f in walk(hold) if rscript in f]
            printing('options', options)
            if len(options) > 0:
                choice = options[0]
                for op in options[1:]:
                    vv = splitter(op, 'R-')
                    if vv >= version:
                        if 'x64' in op:
                            choice = op
                            version = vv
                        elif 'i386' in op and 'x64' not in choice:
                            choice = op
                            version = vv
                        elif 'i386' not in choice and 'x64' not in choice:
                            choice = op
                            version = vv
            else:
                print (warn); return
        else:
            'something to get the information out of the settings file.'
        return choice

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

    def OnFindClose(self, event):
        event.GetDialog().Destroy()

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


# end of file
