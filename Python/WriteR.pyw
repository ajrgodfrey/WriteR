# WriteR Version 0.160420.4
# development of this Python version left solely to Jonathan Godfrey from 8 March 2016 onwards
# a C++ version will commence development in parallel, led by James Curtis.
# cleaning taking place: any line starting with #- suggests a block of redundant code was removed.
# assistance from T.Bilton on 15 April 2016 to add knit command. More to come.


import wx 
import sys
from wx.py.shell import Shell
from wx.aui import AuiManager, AuiPaneInfo
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT
from os.path import join, split, isdir, expanduser, realpath
from os import walk
from time import asctime, sleep
#from FormatMenuEvents import *

print_option = False

# set up some ID tags
ID_STATUSBAR = wx.NewId()
ID_BUILD = wx.NewId()
ID_KNIT2HTML = wx.NewId()
ID_SETTINGS = wx.NewId()

# symbols menu for mathematical symbols
ID_SYMBOL_INFINITY = wx.NewId() 
ID_SYMBOL_TIMES = wx.NewId() 
ID_SYMBOL_PARTIAL = wx.NewId() 
ID_SYMBOL_LEFTPAREN = wx.NewId() 
ID_SYMBOL_RIGHTPAREN = wx.NewId() 
ID_SYMBOL_LEFTSQUARE = wx.NewId() 
ID_SYMBOL_RIGHTSQUARE = wx.NewId() 
ID_SYMBOL_LEFTCURLY = wx.NewId() 
ID_SYMBOL_RIGHTCURLY = wx.NewId()

ID_RCOMMAND = wx.NewId()
ID_RCHUNK = wx.NewId()
ID_RGRAPH = wx.NewId()

ID_SQUAREROOT = wx.NewId() 
ID_FRACTION = wx.NewId() 
ID_SUMMATION = wx.NewId() 
ID_INTEGRAL = wx.NewId() 
ID_PRODUCT = wx.NewId() 
ID_LIMIT = wx.NewId() 
ID_DOUBLESUMMATION = wx.NewId() 
ID_DOUBLEINTEGRAL = wx.NewId()

# Greek menu for Greek letters
ID_GREEK_ALPHA = wx.NewId() 
ID_GREEK_BETA = wx.NewId() 
ID_GREEK_GAMMA = wx.NewId() 
ID_GREEK_DELTA = wx.NewId() 
ID_GREEK_EPSILON = wx.NewId() 
ID_GREEK_ZETA = wx.NewId() 
ID_GREEK_ETA = wx.NewId() 
ID_GREEK_THETA = wx.NewId() 
ID_GREEK_IOTA = wx.NewId() 
ID_GREEK_KAPPA = wx.NewId() 
ID_GREEK_LAMBDA = wx.NewId() 
ID_GREEK_MU = wx.NewId() 
ID_GREEK_NU = wx.NewId() 
ID_GREEK_XI = wx.NewId() 
ID_GREEK_OMICRON = wx.NewId() 
ID_GREEK_PI = wx.NewId() 
ID_GREEK_RHO = wx.NewId() 
ID_GREEK_SIGMA = wx.NewId() 
ID_GREEK_TAU = wx.NewId() 
ID_GREEK_UPSILON = wx.NewId() 
ID_GREEK_PHI = wx.NewId() 
ID_GREEK_CHI = wx.NewId() 
ID_GREEK_PSI = wx.NewId() 
ID_GREEK_OMEGA = wx.NewId()

# format menu items
ID_BOLD = wx.NewId()
ID_ITALIC = wx.NewId()
ID_MATH = wx.NewId()

# IDs for headings
ID_H1 = wx.NewId() 
ID_H2 = wx.NewId() 
ID_H3 = wx.NewId() 
ID_H4 = wx.NewId() 
ID_H5 = wx.NewId() 
ID_H6 = wx.NewId()

# set up global text strings
SBText = "This program is for editing R Markdown files"


def dcf_dumps(data, sort_keys=True):
    string = ""
    for k, v in sorted(data.iteritems()):
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
    if print_option: print args


class BashProcessThread(Thread):
    def __init__(self, flag, input_list, writelineFunc):
        Thread.__init__(self)
        self.flag = flag
        self.writelineFunc = writelineFunc
        self.setDaemon(True)
        self.input_list = input_list
        printing(input_list)
        self.comp_thread = Popen(input_list, stdout=PIPE, stderr=STDOUT)

    #- def run(self):

class MyInterpretor(object):
    def __init__(self, locals, rawin, stdin, stdout, stderr):
        self.introText = "Welcome to stackoverflow bash shell"
        self.locals = locals
        self.revision = 1.0
        self.rawin = rawin
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.more = False
        # bash process
        self.bp = Popen(['python', '-u', 'test_out.py'], shell=False, stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        # start output grab thread
        self.outputThread = BashProcessThread(self.bp.stdout.readline)
        self.outputThread.start()
        # start err grab thread
        # self.errorThread = BashProcessThread(self.bp.stderr.readline)
        # self.errorThread.start()

    #- def getAutoCompleteKeys(self):
    #- def getAutoCompleteList(self, *args, **kwargs):
    #- def getCallTip(self, command):
    #- def push(self, command):

ID_DIRECTORY_CHANGE = wx.NewId()
ID_R_PATH = wx.NewId()
ID_BUILD_COMMAND = wx.NewId()
ID_KNIT2HTML_COMMAND = wx.NewId()


class SettingsDialog(wx.Dialog):
    def __init__(self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, "Settings", pos, size, style)
        self._frame = parent
        s1 = wx.BoxSizer(wx.HORIZONTAL)
        self._default_directory = wx.TextCtrl(self, ID_DIRECTORY_CHANGE, parent.settings['dirname'],
                                              wx.Point(0, 0), wx.Size(350, 20))
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.Add(wx.StaticText(self, -1, "Default directory"))
        s1.Add(self._default_directory)
        s1.Add((1, 1), 1, wx.EXPAND)
        s1.SetItemMinSize(1, (180, 20))
        s2 = wx.BoxSizer(wx.HORIZONTAL)
        self._default_CRAN = wx.TextCtrl(self, ID_DIRECTORY_CHANGE, parent.settings['repo'],
                                         wx.Point(0, 0), wx.Size(350, 20))
        s2.Add((1, 1), 1, wx.EXPAND)
        s2.Add(wx.StaticText(self, -1, "Default CRAN server"))
        s2.Add(self._default_CRAN)
        s2.Add((1, 1), 1, wx.EXPAND)
        s2.SetItemMinSize(1, (180, 20))
        s3 = wx.BoxSizer(wx.HORIZONTAL)
        self._r_path = wx.TextCtrl(self, ID_R_PATH, parent.settings['RDirectory'],
                                   wx.Point(0, 0), wx.Size(350, 20))
        s3.Add((1, 1), 1, wx.EXPAND)
        s3.Add(wx.StaticText(self, -1, "Rscript executable"))
        s3.Add(self._r_path)
        s3.Add((1, 1), 1, wx.EXPAND)
        s3.SetItemMinSize(1, (180, 20))
        s4 = wx.BoxSizer(wx.HORIZONTAL)
        self._build_command = wx.TextCtrl(self, ID_BUILD_COMMAND, parent.settings['buildcommand'],
                                          wx.Point(0, 0), wx.Size(350, 60), wx.TE_MULTILINE)
        s4.Add((1, 1), 1, wx.EXPAND)
        s4.Add(wx.StaticText(self, -1, "Built command\n(The braces {} denote\nthe file path placeholder.)"))
        s4.Add(self._build_command)
        s4.Add((1, 1), 1, wx.EXPAND)
        s4.SetItemMinSize(1, (180, 60))
        s5 = wx.BoxSizer(wx.HORIZONTAL)
        self._knit2html_command = wx.TextCtrl(self, ID_KNIT2HTML_COMMAND, parent.settings['knit2htmlcommand'],
                                          wx.Point(0, 0), wx.Size(350, 60), wx.TE_MULTILINE)
        s5.Add((1, 1), 1, wx.EXPAND)
        s5.Add(wx.StaticText(self, -1, "Knit2html command\n(The braces {} denote\nthe file path placeholder.)"))
        s5.Add(self._knit2html_command)
        s5.Add((1, 1), 1, wx.EXPAND)
        s5.SetItemMinSize(1, (180, 60))
        s6 = wx.BoxSizer(wx.HORIZONTAL)
        self._window_text = wx.TextCtrl(self, ID_BUILD_COMMAND, parent.settings['newText'],
                                        wx.Point(0, 0), wx.Size(350, 60), wx.TE_MULTILINE)
        s6.Add((1, 1), 1, wx.EXPAND)
        s6.Add(wx.StaticText(self, -1, "The default text included in all new files."))
        s6.Add(self._window_text)
        s6.Add((1, 1), 1, wx.EXPAND)
        s6.SetItemMinSize(1, (180, 60))
        grid_sizer = wx.GridSizer(cols=1)
        grid_sizer.SetHGap(5)
        grid_sizer.Add(s1)
        grid_sizer.Add(s2)
        grid_sizer.Add(s3)
        grid_sizer.Add(s4)
        grid_sizer.Add(s5)
        grid_sizer.Add(s6)
        cont_sizer = wx.BoxSizer(wx.VERTICAL)
        cont_sizer.Add(grid_sizer, 1, wx.EXPAND | wx.ALL, 6)
        btn_sizer = wx.StdDialogButtonSizer()
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btn_sizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btn_sizer.AddButton(btn)
        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog. (Cool, huh?)")
        btn_sizer.AddButton(btn)
        btn_sizer.Realize()
        cont_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 6)
        self.SetSizer(cont_sizer)
        cont_sizer.Fit(self)


# get on with the program
class MainWindow(wx.Frame):
    def __init__(self, parent=None, id=-1, title="", pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE |
                                        wx.SUNKEN_BORDER |
                                        wx.CLIP_CHILDREN, filename="untitled.Rmd"):
        super(MainWindow, self).__init__(parent, id, title, pos, size, style)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self._mgr = AuiManager()
        self._mgr.SetManagedWindow(self)
        self.font = wx.Font(14, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas')
        # self.font.SetPointSize(int) # to change the font size
        self.settingsFile = "WriteROptions"
        self.settings = {'repo': "http://cran.stat.auckland.ac.nz/",
                         'dirname': 'none',
                         'templates': 'none',
                         'lastdir': expanduser('~'),
                         'filename': 'none',
                         'newText': "Use WriteR to edit your R markdown files",
                         'RDirectory': self.GetRDirectory(),
                         'buildcommand': '''rmarkdown::render("{}")''',
                         'knit2htmlcommand': '''knitr::knit2html("{}")'''}
        self.settings = self.getSettings(self.settingsFile, self.settings)
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

    def CreateInteriorWindowComponents(self):
        self.editor = self.CreateTextCtrl(self.settings['newText'])
        self.console = self.CreateTextCtrl("")
        self.console.SetEditable(False)
        self._mgr.AddPane(self.console, AuiPaneInfo().Name("console")
                          .Caption("Console").Bottom().Layer(1).Position(1).CloseButton(True)
                          .MinimizeButton(True).Hide())
        self._mgr.AddPane(self.editor, AuiPaneInfo().Name('editor').
                          CenterPane().Hide())
        self._mgr.GetPane("console").Hide().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.GetPane("editor").Show()
        self.editor.SetFocus()
        self.editor.SelectAll()
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
                 (
                 wx.ID_EXIT, "Quit && save\tCtrl+Q", "Saves the current file and closes the program", self.OnSafeExit)]:
            if id == None:
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
                 (None,) * 4,
                 (ID_SETTINGS, 'Settings', "Setup the editor to your liking", self.OnSettings)]:
            if id == None:
                editMenu.AppendSeparator()
            else:
                item = editMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(editMenu, "&Edit")  # Add the editMenu to the MenuBar


        buildMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_BUILD, "Build\tF5", "Build the script", self.OnBuild),
                 (ID_KNIT2HTML, "Knit to html\tF6", "Knit the script to HTML", self.OnKnit2html)]:
            if id == None:
                buildMenu.AppendSeparator()
            else:
                item = buildMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(buildMenu, "Build")  # Add the Build Menu to the MenuBar

        insertMenu = wx.Menu()
        AddURL = insertMenu.Append(-1, "URL")
        self.Bind(wx.EVT_MENU, self.OnAddURL, AddURL)
        AddFigure = insertMenu.Append(-1, "Figure")
        self.Bind(wx.EVT_MENU, self.OnAddFigure, AddFigure)
        headingsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_H1, "level &1\tAlt+1", "insert heading level 1", self.OnHeading1), 
                 (ID_H2, "level &2\tAlt+2", "insert heading level 2", self.OnHeading2), 
                 (ID_H3, "level &3\tAlt+3", "insert heading level 3", self.OnHeading3), 
                 (ID_H4, "level &4\tAlt+4", "insert heading level 4", self.OnHeading4), 
                 (ID_H5, "level &5\tAlt+5", "insert heading level 5", self.OnHeading5), 
                 (ID_H6, "level &6\tAlt+6", "insert heading level 6", self.OnHeading6)]:
            if id == None:
                headingsMenu.AppendSeparator()
            else:
                item = headingsMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        insertMenu.AppendMenu(-1, "Heading", headingsMenu)
        menuBar.Append(insertMenu, "Insert")  # Add the Insert Menu to the MenuBar

        formatMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_BOLD, "Bold\tCtrl+b", "move to bold face font", self.OnBold),
                 (ID_ITALIC, "Italic\tCtrl+i", "move to italic face font", self.OnItalic),
                 (ID_MATH, "Maths mode\tCtrl+Shift+$", "move text to maths mode", self.OnMath)]:
            if id == None:
                formatMenu.AppendSeparator()
            else:
                item = formatMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(formatMenu, "F&ormat")  # Add the format Menu to the MenuBar


        mathsMenu = wx.Menu()
        symbolsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_SYMBOL_INFINITY, "infinity\tCtrl+Shift+i", "insert infinity", self.OnSymbol_infinity), 
                 (ID_SYMBOL_TIMES, "times\tCtrl+8", "insert times", self.OnSymbol_times), 
                 (ID_SYMBOL_PARTIAL, "partial\tCtrl+Shift+d", "insert partial", self.OnSymbol_partial), 
                 (ID_SYMBOL_LEFTPAREN, "LeftParen\tCtrl+9", "insert left parenthesis", self.OnSymbol_LeftParen), 
                 (ID_SYMBOL_RIGHTPAREN, "RightParen\tCtrl+0", "insert right parenthesis", self.OnSymbol_RightParen), 
                 (ID_SYMBOL_LEFTSQUARE, "LeftSquare\tCtrl+[", "insert left square bracket", self.OnSymbol_LeftSquare), 
                 (ID_SYMBOL_RIGHTSQUARE, "RightSquare\tCtrl+]", "insert right square bracket", self.OnSymbol_RightSquare), 
                 (ID_SYMBOL_LEFTCURLY, "LeftCurly\tCtrl+Shift+{", "insert left curly bracket", self.OnSymbol_LeftCurly), 
                 (ID_SYMBOL_RIGHTCURLY, "RightCurly\tCtrl+Shift+}", "insert right curly bracket", self.OnSymbol_RightCurly)]:
            if id == None:
                symbolsMenu.AppendSeparator()
            else:
                item = symbolsMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.AppendMenu(-1, "Symbols", symbolsMenu)
        structuresMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_SQUAREROOT, "Square root\tAlt+Ctrl+Shift+r", "insert a square root", self.OnSquareRoot), 
                 (ID_FRACTION, "Fraction\tCtrl+Shift+/", "insert a fraction", self.OnFraction), 
                 (ID_SUMMATION, "Summation\tAlt+Ctrl+Shift+s", "insert a summation", self.OnSummation), 
                 (ID_INTEGRAL, "Integral\tAlt+Ctrl+Shift+i", "insert an integral", self.Onintegral), 
                 (ID_PRODUCT, "Product\tAlt+Ctrl+Shift+p", "insert a product", self.OnProduct), 
                 (ID_LIMIT, "Limit\tAlt+Ctrl+Shift+l", "insert a limit", self.OnLimit), 
                 (ID_DOUBLESUMMATION, "Double summation\tAlt+Ctrl+Shift+d", "insert a double summation", self.OnDoubleSummation), 
                 (ID_DOUBLEINTEGRAL, "Double integral", "insert a double integral", self.OnDoubleIntegral)]:
            if id == None:
                structuresMenu.AppendSeparator()
            else:
                item = structuresMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.AppendMenu(-1, "structures", structuresMenu)# Add the structures Menu as a submenu to the main menu
        GreekMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_GREEK_ALPHA, "alpha\tAlt+Shift+a", "insert greek letter alpha", self.OnGreek_alpha), 
                 (ID_GREEK_BETA, "beta\tAlt+Shift+b", "insert greek letter beta", self.OnGreek_beta), 
                 (ID_GREEK_GAMMA, "gamma\tAlt+Shift+g", "insert greek letter gamma", self.OnGreek_gamma), 
                 (ID_GREEK_DELTA, "delta\tAlt+Shift+d", "insert greek letter delta", self.OnGreek_delta), 
                 (ID_GREEK_EPSILON, "epsilon\tAlt+Shift+e", "insert greek letter epsilon", self.OnGreek_epsilon), 
                 (ID_GREEK_ZETA, "zeta\tAlt+Shift+z", "insert greek letter zeta", self.OnGreek_zeta), 
                 (ID_GREEK_ETA, "eta\tAlt+Shift+w", "insert greek letter eta", self.OnGreek_eta), 
                 (ID_GREEK_THETA, "theta\tAlt+Shift+/", "insert greek letter theta", self.OnGreek_theta), 
                 (ID_GREEK_IOTA, "iota\tAlt+Shift+i", "insert greek letter iota", self.OnGreek_iota), 
                 (ID_GREEK_KAPPA, "kappa\tAlt+Shift+k", "insert greek letter kappa", self.OnGreek_kappa), 
                 (ID_GREEK_LAMBDA, "lambda\tAlt+Shift+l", "insert greek letter lambda", self.OnGreek_lambda), 
                 (ID_GREEK_MU, "mu\tAlt+Shift+m", "insert greek letter mu", self.OnGreek_mu), 
                 (ID_GREEK_NU, "nu\tAlt+Shift+n", "insert greek letter nu", self.OnGreek_nu), 
                 (ID_GREEK_XI, "xi\tAlt+Shift+x", "insert greek letter xi", self.OnGreek_xi), 
                 (ID_GREEK_OMICRON, "omicron\tAlt+Shift+o", "insert greek letter omicron", self.OnGreek_omicron), 
                 (ID_GREEK_PI, "pi\tAlt+Shift+p", "insert greek letter pi", self.OnGreek_pi), 
                 (ID_GREEK_RHO, "rho\tAlt+Shift+r", "insert greek letter rho", self.OnGreek_rho), 
                 (ID_GREEK_SIGMA, "sigma\tAlt+Shift+s", "insert greek letter sigma", self.OnGreek_sigma), 
                 (ID_GREEK_TAU, "tau\tAlt+Shift+t", "insert greek letter tau", self.OnGreek_tau), 
                 (ID_GREEK_UPSILON, "upsilon\tAlt+Shift+u", "insert greek letter upsilon", self.OnGreek_upsilon), 
                 (ID_GREEK_PHI, "phi\tAlt+Shift+f", "insert greek letter phi", self.OnGreek_phi), 
                 (ID_GREEK_CHI, "chi\tAlt+Shift+c", "insert greek letter chi", self.OnGreek_chi), 
                 (ID_GREEK_PSI, "psi\tAlt+Shift+y", "insert greek letter psi", self.OnGreek_psi), 
                 (ID_GREEK_OMEGA, "omega\tAlt+Shift+.", "insert greek letter omega", self.OnGreek_omega)]:
            if id == None:
                GreekMenu.AppendSeparator()
            else:
                item = GreekMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.AppendMenu(-1, "Greek letters", GreekMenu)
        menuBar.Append(mathsMenu, "Maths")  # Add the maths Menu to the MenuBar

        statsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_RCOMMAND, "Insert inline R command", "insert an in-line R command", self.OnRCommand),
                 (ID_RCHUNK, "Insert R code chunk\tAlt+R", "insert standard R code chunk", self.OnRChunk),
                 (ID_RGRAPH, "Insert R code chunk for a graph\tAlt+g", "insert R code chunk for a graph", self.OnRGraph)
]:
            if id == None:
                statsMenu.AppendSeparator()
            else:
                item = statsMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(statsMenu, "stats")  # Add the stats Menu to the MenuBar


        helpMenu = wx.Menu()
        for id, label, helpText, handler in \
                [(wx.ID_ABOUT, "About", "Information about this program", self.OnAbout)]:
            if id == None:
                fileMenu.AppendSeparator()
            else:
                item = helpMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(helpMenu, "&Help")  # Add the helpMenu to the MenuBar
        self.SetMenuBar(menuBar)  # Add the menuBar to the Frame

    def CreateShellCtrl(self):
        shell = Shell(self, -1, wx.Point(0, 0), wx.Size(150, 90),
                      wx.NO_BORDER | wx.TE_MULTILINE, InterpClass=MyInterpretor)
        shell.SetFont(self.font)
        return shell

    def CreateTextCtrl(self, text):
        text = wx.TextCtrl(self, -1, text, wx.Point(0, 0), wx.Size(150, 90),
                           wx.NO_BORDER | wx.TE_MULTILINE)
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
    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, "WriteR is a  first attempt  at developing an R Markdown editor\n"
                                        "using wxPython, developed by Jonathan Godfrey\n"
                                        "and James Curtis in 2015.\nVersion: 0.150302",
                                  "About this R Markdown Editor", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnSafeExit(self, event):
        self.OnSave(event)
        self.OnExit(event)

    def OnExit(self, event):
        self.Close()  # Close the main window.

    def OnSave(self, event):
        textfile = open(join(self.dirname, self.filename), "w")
        textfile.write(self.editor.GetValue())
        textfile.close()

    def OnOpen(self, event):
        if self.askUserForFilename(style=wx.OPEN, **self.defaultFileDialogOptions()):
            self.fileOpen(self.dirname, self.filename)

    def fileOpen(self, dirname, filename):
        textfile = open(join(dirname, filename), "r")
        self.editor.SetValue(textfile.read())
        textfile.close()

    def OnNewFile(self, event):
        self.olddirname = self.dirname
        self.dirname = ".\\templates"
        self.OnOpen(event)
        self.dirname = self.olddirname
        if self.filename == "Blank.Rmd":
            self.editor.WriteText("% file created on " + asctime() + "\n\n")
        self.OnSaveAs(event)

    def OnSaveAs(self, event):
        if self.askUserForFilename(defaultFile=self.filename, style=wx.SAVE, **self.defaultFileDialogOptions()):
            self.OnSave(event)

            # edit menu events
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


    # view menu events (removed)
    def StatusBar(self):
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetFieldsCount(3)
        self.statusbar.SetStatusWidths([-5, -2, -1])
        self.SetStatusText(SBText)

    def StartThread(self, input_object):
        if self.sub_flag.isSet(): return
        if self.comp_thread is not None:
            self.sub_flag.set()
            while self.comp_thread.isAlive():
                sleep(1)
            self.sub_flag.clear()
            self.console.SetValue('')
        self.comp_thread = BashProcessThread(self.sub_flag, input_object, self.console.WriteText)
        self.comp_thread.start()

    def OnBuild(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.settings['repo']) +
                          self.settings['buildcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])

    def OnKnit2html(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('knitr', installed.packages()[,1])){{'''.format() +
                          '''install.packages('knitr', repos="{0}")}};require(knitr);'''.format(
                              self.settings['repo']) +
                          self.settings['knit2htmlcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])


    def OnRCommand(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("`")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("`r ")
        self.editor.SetInsertionPoint(frm + 3)


    def OnRChunk(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("\n```\n\n")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("\n```{r }\n")
        self.editor.SetInsertionPoint(frm + 8)

    def OnRGraph(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("\n```\n\n")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("\n```{r , fig.height=5, fig.width=5, fig.cap=\"\"}\n")
        self.editor.SetInsertionPoint(frm + 8)


    def OnSymbol_infinity(self, event):
        self.editor.WriteText("\\infty{}") 
    def OnSymbol_times(self, event):
        self.editor.WriteText("\\times{}") 
    def OnSymbol_partial(self, event):
        self.editor.WriteText("\\partial{}") 
    def OnSymbol_LeftParen(self, event):
        self.editor.WriteText("\\left(") 
    def OnSymbol_RightParen(self, event):
        self.editor.WriteText("\\right)") 
    def OnSymbol_LeftSquare(self, event):
        self.editor.WriteText("\\left[") 
    def OnSymbol_RightSquare(self, event):
        self.editor.WriteText("\\right]") 
    def OnSymbol_LeftCurly(self, event):
        self.editor.WriteText("\\left Curly{}") 
    def OnSymbol_RightCurly(self, event):
        self.editor.WriteText("\\right Curly{}")



    def OnSquareRoot(self, event):
        self.editor.WriteText("\\sqrt{}") 
    def OnFraction(self, event):
        self.editor.WriteText("\\frac{ num }{ den }") 
    def OnSummation(self, event):
        self.editor.WriteText("\\sum_{ lower }^{ upper }{ what }") 
    def Onintegral(self, event):
        self.editor.WriteText("\\int_{ lower }^{ upper }{ what }") 
    def OnProduct(self, event):
        self.editor.WriteText("\\prod_{ lower }^{ upper }{ what }") 
    def OnLimit(self, event):
        self.editor.WriteText("\\lim_{ what \\to where }{is}") 
    def OnDoubleSummation(self, event):
        self.editor.WriteText("\\sum_{ lower }^{ upper }{\\sum_{ lower }^{ upper }{ what }}") 
    def OnDoubleIntegral(self, event):
        self.editor.WriteText("\\int_{ lower }^{ upper }{\\int_{ lower }^{ upper }{ what }}") 

    def OnGreek_alpha(self, event):
        self.editor.WriteText("\\alpha{}") 
    def OnGreek_beta(self, event):
        self.editor.WriteText("\\beta{}") 
    def OnGreek_gamma(self, event):
        self.editor.WriteText("\\gamma{}") 
    def OnGreek_delta(self, event):
        self.editor.WriteText("\\delta{}") 
    def OnGreek_epsilon(self, event):
        self.editor.WriteText("\\epsilon{}") 
    def OnGreek_zeta(self, event):
        self.editor.WriteText("\\zeta{}") 
    def OnGreek_eta(self, event):
        self.editor.WriteText("\\eta{}") 
    def OnGreek_theta(self, event):
        self.editor.WriteText("\\theta{}") 
    def OnGreek_iota(self, event):
        self.editor.WriteText("\\iota{}") 
    def OnGreek_kappa(self, event):
        self.editor.WriteText("\\kappa{}") 
    def OnGreek_lambda(self, event):
        self.editor.WriteText("\\lambda{}") 
    def OnGreek_mu(self, event):
        self.editor.WriteText("\\mu{}") 
    def OnGreek_nu(self, event):
        self.editor.WriteText("\\nu{}") 
    def OnGreek_xi(self, event):
        self.editor.WriteText("\\xi{}") 
    def OnGreek_omicron(self, event):
        self.editor.WriteText("\\omicron{}") 
    def OnGreek_pi(self, event):
        self.editor.WriteText("\\pi{}") 
    def OnGreek_rho(self, event):
        self.editor.WriteText("\\rho{}") 
    def OnGreek_sigma(self, event):
        self.editor.WriteText("\\sigma{}") 
    def OnGreek_tau(self, event):
        self.editor.WriteText("\\tau{}") 
    def OnGreek_upsilon(self, event):
        self.editor.WriteText("\\upsilon{}") 
    def OnGreek_phi(self, event):
        self.editor.WriteText("\\phi{}") 
    def OnGreek_chi(self, event):
        self.editor.WriteText("\\chi{}") 
    def OnGreek_psi(self, event):
        self.editor.WriteText("\\psi{}") 
    def OnGreek_omega(self, event):
        self.editor.WriteText("\\omega{}")

    # format menu events
    def OnMath(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("$")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("$")
        self.editor.SetInsertionPoint(to + 2)

    def OnBold(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("*")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("*")
        self.editor.SetInsertionPoint(to + 2)


    def OnItalic(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("**")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("**")
        self.editor.SetInsertionPoint(to + 4)

    def OnAddURL(self, event):
        self.editor.WriteText(" [alt text](http://) ") 
    def OnAddFigure(self, event):
        self.editor.WriteText(" ![alt tag](filename) ") 

    def OnHeading1(self, event):
        self.editor.WriteText("\n# ") 
    def OnHeading2(self, event):
        self.editor.WriteText("\n## ") 
    def OnHeading3(self, event):
        self.editor.WriteText("\n### ") 
    def OnHeading4(self, event):
        self.editor.WriteText("\n#### ") 
    def OnHeading5(self, event):
        self.editor.WriteText("\n##### ") 
    def OnHeading6(self, event):
        self.editor.WriteText("\n###### ")



    def OnClose(self, event):
        self.settings['filename'] = self.filename
        self.settings['lastdir'] = self.dirname
        self.setSettings(self.settingsFile, self.settings)
        if event.CanVeto() and self.editor.IsModified():
            hold = wx.MessageBox("Your file has not been saved. Would you like to save your work?",
                                 "Save before exit?",
                                 wx.ICON_QUESTION | wx.YES_NO | wx.CANCEL | wx.YES_DEFAULT)
            if hold == wx.YES:
                self.OnSaveAs(event)
                self.Destroy()
            elif hold == wx.NO:
                self.Destroy()
            else:
                event.Veto()
        else:
            self.Destroy()

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
                print warn; return
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
                print warn; return
        else:
            'something to get the information out of the settings file.'
        return choice

    def GetStartPosition(self):
        self.x = self.x + 20
        x = self.x
        pt = self.ClientToScreen(wx.Point(0, 0))
        return wx.Point(pt.x + x, pt.y + x)

    def getSettings(self, filepath, settings):
        try:
            file = open(filepath, 'r')
            sets = file.read()
            file.close()
            if len(sets) > 0:
                sets = dcf_loads(sets)
                assert (set(settings.keys()) == set(sets.keys()))
                return sets
        except:
            pass
        return self.setSettings(filepath, settings)

    def setSettings(self, filepath, settings):
        file = open(filepath, 'w')
        file.write(dcf_dumps(settings))
        file.close()
        return settings

    def OnSettings(self, event):
        dlg = SettingsDialog(self, -1, "Sample Dialog", size=(350, 200),
                             style=wx.DEFAULT_DIALOG_STYLE)
        dlg.CenterOnScreen()
        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            self.settings = self.setSettings(self.settingsFile,
                                             {'repo': dlg._default_CRAN.GetValue(),
                                              'dirname': dlg._default_directory.GetValue(),
                                              'lastdir': dlg._default_directory.GetValue(),
                                              'template': dlg._default_directory.GetValue(),
                                              'filename': self.settings['filename'],
                                              'newText': dlg._window_text.GetValue(),
                                              'RDirectory': dlg._r_path.GetValue(),
                                              'buildcommand': dlg._build_command.GetValue(),
                                              'knit2htmlcommand': dlg._knit2html_command.GetValue()})
        dlg.Destroy()

# manditory lines to get program running.
if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    app.MainLoop()
