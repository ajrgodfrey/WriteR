# WriteR Version 0.161011.0
# development of this Python version left solely to Jonathan Godfrey from 8 March 2016 onwards
# a C++ version has been proposed for development in parallel, (led by James Curtis).
# cleaning taking place: any line starting with #- suggests a block of redundant code was removed.
# assistance from T.Bilton on 15 April 2016 to think about additions. More to come.


import wx 
import sys
from wx.py.shell import Shell
from wx.aui import AuiManager, AuiPaneInfo
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT
from os.path import join, split, isdir, expanduser, realpath
from os import walk
from time import asctime, sleep

print_option = False

# set up some ID tags
ID_BUILD = wx.NewId()
ID_KNIT2HTML = wx.NewId()
ID_KNIT2PDF = wx.NewId()
ID_SETTINGS = wx.NewId()

ID_FINDONLY = wx.NewId()
ID_FINDREPLACE = wx.NewId()


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
ID_SYMBOL_GRTREQL = wx.NewId() 
ID_SYMBOL_LESSEQL = wx.NewId() 
ID_SYMBOL_NOTEQL = wx.NewId() 

ID_RCOMMAND = wx.NewId()
ID_RCHUNK = wx.NewId()
ID_RGRAPH = wx.NewId()
ID_RPIPE = wx.NewId()
ID_RLASSIGN = wx.NewId()
ID_RRASSIGN = wx.NewId()

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
ID_GREEK_VAREPSILON = wx.NewId() 
ID_GREEK_ZETA = wx.NewId() 
ID_GREEK_ETA = wx.NewId() 
ID_GREEK_THETA = wx.NewId() 
ID_GREEK_VARTHETA = wx.NewId() 
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
ID_CODE = wx.NewId()
ID_RNDBRK = wx.NewId()
ID_SQBRK = wx.NewId()
ID_CRLBRK = wx.NewId()
ID_BRNDBRK = wx.NewId()
ID_BSQBRK = wx.NewId()
ID_BCRLBRK = wx.NewId()

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
ID_CRAN = wx.NewId()
ID_R_PATH = wx.NewId()
ID_BUILD_COMMAND = wx.NewId()
ID_KNIT2HTML_COMMAND = wx.NewId()
ID_KNIT2PDF_COMMAND = wx.NewId()
ID_NEWTEXT = wx.NewId()


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
        self.hardsettings = {'repo': "http://cran.stat.auckland.ac.nz/",
                             'rendercommand': '''rmarkdown::render("{}")''',
                             'renderallcommand': '''rmarkdown::render("{}", output_format="all")''',
                             'renderpdfcommand': '''rmarkdown::render("{}", output_format="pdf_document")''',
                             'renderwordcommand': '''rmarkdown::render("{}", output_format="word_document")''',
                             'renderhtmlcommand': '''rmarkdown::render("{}", output_format="html_document")''',
                             'knit2mdcommand': '''knitr::knit("{}")''',
                             'knit2htmlcommand': '''knitr::knit2html("{}")''',
                             'knit2pdfcommand': '''knitr::knit2pdf("{}")'''}
        self.settingsFile = "WriteROptions"
        self.settings = {#'dirname': 'none',
#                         'templates': 'none',
                         'lastdir': '.',
                         'filename': 'none',
                         'newText': "Use WriteR to edit your R markdown files, perhaps by starting from a template file",
                         'RDirectory': self.GetRDirectory()}
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
        # for find and find/replace dialogues we need...
        self.Bind(wx.EVT_FIND, self.OnFind)
        self.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        self.Bind(wx.EVT_FIND_REPLACE, self.OnFind)
        self.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnFind)
        self.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)

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
                 (wx.ID_EXIT, "Quit && save\tCtrl+Q", "Saves the current file and closes the program", self.OnSafeExit)]:
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
                 (ID_FINDONLY, "Find\tCtrl+F", "Open a standard find dialog box", self.OnShowFindToFix),
                 (ID_FINDREPLACE, "Find/replace\tCtrl+H", "Open a find /replace dialog box", self.OnShowFindReplaceToFix),
                 (None,) * 4,
                 (ID_SETTINGS, 'Settings', "Setup the editor to your liking", self.OnSettings)]:
            if id == None:
                editMenu.AppendSeparator()
            else:
                item = editMenu.Append(id, label, helpText)
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
        self.Render = buildMenu.Append(wx.ID_ANY, "Render the document\tF6", "Use the rmarkdown package to render the document into the chosen format")
        self.Bind(wx.EVT_MENU, self.OnRenderNull, self.Render)
        # Create render menu
        renderMenu = wx.Menu()
        self.ChooseRenderNull = renderMenu.Append(wx.ID_ANY, "Render using defaults", "Use the rmarkdown package and render function to create HTML or only the first of multiple formats specified in YAML header", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderNull, self.ChooseRenderNull)
        self.ChooseRenderHtml = renderMenu.Append(wx.ID_ANY, "Render into HTML only", "Use the rmarkdown package and render function to create HTML", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderHtml, self.ChooseRenderHtml) 
        self.ChooseRenderWord = renderMenu.Append(wx.ID_ANY, "Render into Microsoft Word only", "Use the rmarkdown package and render function to create Microsoft Word", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderWord, self.ChooseRenderWord) 
        self.ChooseRenderPdf = renderMenu.Append(wx.ID_ANY, "Render into pdf only", "Use the rmarkdown package and render function to create pdf", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderPdf, self.ChooseRenderPdf) 
        self.ChooseRenderAll = renderMenu.Append(wx.ID_ANY, "Render into all specified formats", "Use the rmarkdown package and render function to create multiple output documents", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderAll, self.ChooseRenderAll) 
        buildMenu.AppendMenu(-1, "Set render process to...", renderMenu) # Add the render Menu as a submenu to the build menu
        for id, label, helpText, handler in \
                [
                 (ID_BUILD, "Build\tF5", "Build the script", self.OnBuild),
                 (ID_KNIT2HTML, "Knit to html\tF7", "Knit the script to HTML", self.OnKnit2html),
                 (ID_KNIT2PDF, "Knit to pdf\tShift+F6", "Knit the script to a pdf file using LaTeX", self.OnKnit2pdf)]:
            if id == None:
                buildMenu.AppendSeparator()
            else:
                item = buildMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
 
        menuBar.Append(buildMenu, "Build")  # Add the Build Menu to the MenuBar

        insertMenu = wx.Menu()
        AddHeadBlock = insertMenu.Append(-1, "preamble")
        self.Bind(wx.EVT_MENU, self.OnAddHeadBlock, AddHeadBlock)
        AddURL = insertMenu.Append(-1, "URL")
        self.Bind(wx.EVT_MENU, self.OnAddURL, AddURL)
        AddEMail = insertMenu.Append(-1, "e-mail")
        self.Bind(wx.EVT_MENU, self.OnAddEMail, AddEMail)
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


        mathsMenu = wx.Menu()
        symbolsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_SYMBOL_INFINITY, "infinity\tCtrl+Shift+I", "insert infinity", self.OnSymbol_infinity), 
                 (ID_SYMBOL_TIMES, "times\tCtrl+Shift+*", "insert times", self.OnSymbol_times), 
                 (ID_SYMBOL_PARTIAL, "partial derivative\tCtrl+Shift+D", "insert partial", self.OnSymbol_partial), 
                 (ID_SYMBOL_LESSEQL, "less than or equal\tCtrl+Shift+<", "insert less than or equal sign", self.OnSymbol_leq), 
                 (ID_SYMBOL_GRTREQL, "greater than or equal \tCtrl+Shift+>", "insert greater than or equal sign", self.OnSymbol_geq), 
                 (ID_SYMBOL_NOTEQL, "not equal\tCtrl+Shift+!", "insert not equal sign", self.OnSymbol_neq), 
                 (ID_SYMBOL_LEFTPAREN, "Left Parenthesis\tCtrl+9", "insert variable size left parenthesis", self.OnSymbol_LeftParen), 
                 (ID_SYMBOL_RIGHTPAREN, "Right Parenthesis\tCtrl+0", "insert variable size right parenthesis", self.OnSymbol_RightParen), 
                 (ID_SYMBOL_LEFTSQUARE, "Left Square bracket\tCtrl+[", "insert variable size left square bracket", self.OnSymbol_LeftSquare), 
                 (ID_SYMBOL_RIGHTSQUARE, "Right Square bracket\tCtrl+]", "insert variable size right square bracket", self.OnSymbol_RightSquare), 
                 (ID_SYMBOL_LEFTCURLY, "Left Curly bracket\tCtrl+Shift+{", "insert variable size left curly bracket", self.OnSymbol_LeftCurly), 
                 (ID_SYMBOL_RIGHTCURLY, "Right Curly bracket\tCtrl+Shift+}", "insert variable size right curly bracket", self.OnSymbol_RightCurly)]:
            if id == None:
                symbolsMenu.AppendSeparator()
            else:
                item = symbolsMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.AppendMenu(-1, "Symbols", symbolsMenu)
        structuresMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_SQUAREROOT, "Square root\tAlt+Ctrl+Shift+R", "insert a square root", self.OnSquareRoot), 
                 (ID_FRACTION, "Fraction\tCtrl+Shift+/", "insert a fraction", self.OnFraction), 
                 (ID_SUMMATION, "Summation\tAlt+Ctrl+Shift+S", "insert a summation", self.OnSummation), 
                 (ID_INTEGRAL, "Integral\tAlt+Ctrl+Shift+I", "insert an integral", self.Onintegral), 
                 (ID_PRODUCT, "Product\tAlt+Ctrl+Shift+P", "insert a product", self.OnProduct), 
                 (ID_LIMIT, "Limit\tAlt+Ctrl+Shift+L", "insert a limit", self.OnLimit), 
                 (ID_DOUBLESUMMATION, "Double summation\tAlt+Ctrl+Shift+D", "insert a double summation", self.OnDoubleSummation), 
                 (ID_DOUBLEINTEGRAL, "Double integral", "insert a double integral", self.OnDoubleIntegral)]:
            if id == None:
                structuresMenu.AppendSeparator()
            else:
                item = structuresMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.AppendMenu(-1, "Structures", structuresMenu)# Add the structures Menu as a submenu to the main menu
        GreekMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_GREEK_ALPHA, "alpha\tAlt+Shift+A", "insert greek letter alpha", self.OnGreek_alpha), 
                 (ID_GREEK_BETA, "beta\tAlt+Shift+B", "insert greek letter beta", self.OnGreek_beta), 
                 (ID_GREEK_GAMMA, "gamma\tAlt+Shift+G", "insert greek letter gamma", self.OnGreek_gamma), 
                 (ID_GREEK_DELTA, "delta\tAlt+Shift+D", "insert greek letter delta", self.OnGreek_delta), 
                 (ID_GREEK_EPSILON, "epsilon\tAlt+Shift+E", "insert greek letter epsilon", self.OnGreek_epsilon), 
                 (ID_GREEK_VAREPSILON, "epsilon (variant)\tAlt+Shift+V", "insert variant of greek letter epsilon", self.OnGreek_varepsilon), 
                 (ID_GREEK_ZETA, "zeta\tAlt+Shift+Z", "insert greek letter zeta", self.OnGreek_zeta), 
                 (ID_GREEK_ETA, "eta\tAlt+Shift+W", "insert greek letter eta", self.OnGreek_eta), 
                 (ID_GREEK_THETA, "theta\tAlt+Shift+H", "insert greek letter theta", self.OnGreek_theta), 
                 (ID_GREEK_VARTHETA, "theta (variant)\tAlt+Shift+/", "insert variant of greek letter theta", self.OnGreek_vartheta), 
                 (ID_GREEK_IOTA, "iota\tAlt+Shift+I", "insert greek letter iota", self.OnGreek_iota), 
                 (ID_GREEK_KAPPA, "kappa\tAlt+Shift+K", "insert greek letter kappa", self.OnGreek_kappa), 
                 (ID_GREEK_LAMBDA, "lambda\tAlt+Shift+L", "insert greek letter lambda", self.OnGreek_lambda), 
                 (ID_GREEK_MU, "mu\tAlt+Shift+M", "insert greek letter mu", self.OnGreek_mu), 
                 (ID_GREEK_NU, "nu\tAlt+Shift+N", "insert greek letter nu", self.OnGreek_nu), 
                 (ID_GREEK_XI, "xi\tAlt+Shift+X", "insert greek letter xi", self.OnGreek_xi), 
                 (ID_GREEK_OMICRON, "omicron\tAlt+Shift+O", "insert greek letter omicron", self.OnGreek_omicron), 
                 (ID_GREEK_PI, "pi\tAlt+Shift+P", "insert greek letter pi", self.OnGreek_pi), 
                 (ID_GREEK_RHO, "rho\tAlt+Shift+R", "insert greek letter rho", self.OnGreek_rho), 
                 (ID_GREEK_SIGMA, "sigma\tAlt+Shift+S", "insert greek letter sigma", self.OnGreek_sigma), 
                 (ID_GREEK_TAU, "tau\tAlt+Shift+T", "insert greek letter tau", self.OnGreek_tau), 
                 (ID_GREEK_UPSILON, "upsilon\tAlt+Shift+U", "insert greek letter upsilon", self.OnGreek_upsilon), 
                 (ID_GREEK_PHI, "phi\tAlt+Shift+F", "insert greek letter phi", self.OnGreek_phi), 
                 (ID_GREEK_CHI, "chi\tAlt+Shift+C", "insert greek letter chi", self.OnGreek_chi), 
                 (ID_GREEK_PSI, "psi\tAlt+Shift+Y", "insert greek letter psi", self.OnGreek_psi), 
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
                 (ID_RGRAPH, "Insert R code chunk for a graph\tAlt+G", "insert R code chunk for a graph", self.OnRGraph),
                 (ID_RLASSIGN, "Insert a left assignment\tCtrl+<", "insert R code for the left assignment <-", self.OnRLAssign),
                 (ID_RRASSIGN, "Insert a right assignment\tCtrl+>", "insert R code for the right assignment ->", self.OnRRAssign),
                 (ID_RPIPE, "Insert a pipe operator\tCtrl+Shift+P", "insert R code for the pipe operator %>%", self.OnRPipe)]:
            if id == None:
                statsMenu.AppendSeparator()
            else:
                item = statsMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(statsMenu, "Stats")  # Add the stats Menu to the MenuBar

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
# help menu events
    def OnAbout(self, event):
        dialog = wx.MessageDialog(self, "WriteR is a  first attempt  at developing an R Markdown editor\n"
                                        "using wxPython. Development started by Jonathan Godfrey\n"
                                        "and James Curtis in 2015.\nContinued development assisted by Timothy Bilton in 2016.\nSend all feedback to Jonathan Godfrey at a.j.godfrey@massey.ac.nz\nVersion: 0.160530.0 (or later)",
                                  "About this R Markdown Editor", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

# file menu events
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


# view menu events
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




# general events
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

    def OnRenderNull(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['rendercommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])

    # set default build 
    OnBuild = OnRenderNull

    def OnRenderHtml(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['renderhtmlcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])
    def OnRenderAll(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['renderallcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])
    def OnRenderWord(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['renderwordcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])
    def OnRenderPdf(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('rmarkdown', installed.packages()[,1])){{'''.format() +
                          '''install.packages('rmarkdown', repos="{0}")}};require(rmarkdown);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['renderpdfcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])


    def OnSelectRenderNull(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderNull, self.Render)
    def OnSelectRenderHtml(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderHtml, self.Render)
    def OnSelectRenderAll(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderAll, self.Render)
    def OnSelectRenderWord(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderWord, self.Render)
    def OnSelectRenderPdf(self, event):
        self.Bind(wx.EVT_MENU, self.OnRenderPdf, self.Render)


    def OnKnit2html(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('knitr', installed.packages()[,1])){{'''.format() +
                          '''install.packages('knitr', repos="{0}")}};require(knitr);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['knit2htmlcommand'].format(
                              join(self.dirname, self.filename).replace('\\', '\\\\'))])

    def OnKnit2pdf(self, event):
        self._mgr.GetPane("console").Show().Bottom().Layer(0).Row(0).Position(0)
        self._mgr.Update()
        # This allows the file to be up to date for the build
        self.OnSave(event)
        self.StartThread([self.settings['RDirectory'], "-e",
                          '''if (!is.element('knitr', installed.packages()[,1])){{'''.format() +
                          '''install.packages('knitr', repos="{0}")}};require(knitr);'''.format(
                              self.hardsettings['repo']) +
                          self.hardsettings['knit2pdfcommand'].format(
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

    def OnRPipe(self, event):
        self.editor.WriteText(" %>% ") 
    def OnRLAssign(self, event):
        self.editor.WriteText(" <- ") 
    def OnRRAssign(self, event):
        self.editor.WriteText(" -> ") 

    def OnSymbol_infinity(self, event):
        self.editor.WriteText("\\infty{}") 
    def OnSymbol_geq(self, event):
        self.editor.WriteText(" \\geq ") 
    def OnSymbol_leq(self, event):
        self.editor.WriteText(" \\leq ") 
    def OnSymbol_neq(self, event):
        self.editor.WriteText(" \\ne ") 

    def OnSymbol_times(self, event):
        self.editor.WriteText("\\times{}") 
    def OnSymbol_partial(self, event):
        self.editor.WriteText("\\partial{}") 
    def OnSymbol_LeftParen(self, event):
        self.editor.WriteText("\\left(") 
    def OnSymbol_RightParen(self, event):
        self.editor.WriteText("\\right) ") 
    def OnSymbol_LeftSquare(self, event):
        self.editor.WriteText("\\left[") 
    def OnSymbol_RightSquare(self, event):
        self.editor.WriteText("\\right] ") 
    def OnSymbol_LeftCurly(self, event):
        self.editor.WriteText("\\left\\{") 
    def OnSymbol_RightCurly(self, event):
        self.editor.WriteText("\\right\\} ")



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
    def OnGreek_varepsilon(self, event):
        self.editor.WriteText("\\varepsilon{}") 
    def OnGreek_zeta(self, event):
        self.editor.WriteText("\\zeta{}") 
    def OnGreek_eta(self, event):
        self.editor.WriteText("\\eta{}") 
    def OnGreek_theta(self, event):
        self.editor.WriteText("\\theta{}") 
    def OnGreek_vartheta(self, event):
        self.editor.WriteText("\\vartheta{}") 
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
    def OnSquareBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("]")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("[")
        self.editor.SetInsertionPoint(to + 2)

    def OnCurlyBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("}")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("{")
        self.editor.SetInsertionPoint(to + 2)


    def OnRoundBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText(")")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("(")
        self.editor.SetInsertionPoint(to + 2)

    def OnMathSquareBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("\\right] ")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText(" \\left[")
        self.editor.SetInsertionPoint(to + 15)

    def OnMathCurlyBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("\\right} ")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText(" \\left{")
        self.editor.SetInsertionPoint(to + 15)

    def OnMathRoundBrack(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("\\right) ")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText(" \\left(")
        self.editor.SetInsertionPoint(to + 15)

    def OnMath(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("$")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("$")
        self.editor.SetInsertionPoint(to + 2)

    def OnItalic(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("*")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("*")
        self.editor.SetInsertionPoint(to + 2)


    def OnBold(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("**")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("**")
        self.editor.SetInsertionPoint(to + 4)

    def OnCode(self, event):
        frm, to = self.editor.GetSelection()
        self.editor.SetInsertionPoint(to)
        self.editor.WriteText("`")
        self.editor.SetInsertionPoint(frm)
        self.editor.WriteText("`")
        self.editor.SetInsertionPoint(to + 2)


    def OnAddHeadBlock(self, event):
        self.editor.SetInsertionPoint(0)
        self.editor.WriteText('---\ntitle: ""\nauthor: ""\ndate: ""\noutput: html_document\n---\n') 
        self.editor.SetInsertionPoint(13)

    def OnAddURL(self, event):
        self.editor.WriteText(" [alt text](http://) ") 
    def OnAddEMail(self, event):
        self.editor.WriteText(" [name](Mailto:) ") 
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

    # view menu events
    def ToggleStatusBar(self, event):
        if self.statusbar.IsShown():
            self.statusbar.Hide()
        else:
            self.statusbar.Show()
            self.SetStatusText(SBText)




    def OnClose(self, event):
        self.settings['filename'] = self.filename
        self.settings['lastdir'] = self.dirname
        self.setSettings(self.settingsFile, self.settings)
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
        wx.MessageBox("You wanted to see the settings")

    def OnShowFindToFix(self, event):
        wx.MessageBox("This feature is not fully implemented as yet.")
    def OnShowFindReplaceToFix(self, event):
        wx.MessageBox("This feature is not fully implemented as yet.")

    def OnShowFind(self, event):
        data = wx.FindReplaceData()
        dlg = wx.FindReplaceDialog(self, data, "Find")
        dlg.data = data  # save a reference to it...
        dlg.Show(True)

    def OnShowFindReplace(self, event):
        data = wx.FindReplaceData()
        dlg = wx.FindReplaceDialog(self, data, "Find & Replace", wx.FR_REPLACEDIALOG)
        dlg.data = data  # save a reference to it...
        dlg.Show(True)

    def OnFind(self, event):
        map = {
            wx.wxEVT_COMMAND_FIND : "FIND",
            wx.wxEVT_COMMAND_FIND_NEXT : "FIND_NEXT",
            wx.wxEVT_COMMAND_FIND_REPLACE : "REPLACE",
            wx.wxEVT_COMMAND_FIND_REPLACE_ALL : "REPLACE_ALL",
            }
        et = event.GetEventType()
        if et in map:
            evtType = map[et]
        else:
            evtType = "**Unknown Event Type**"
        if et in [wx.wxEVT_COMMAND_FIND_REPLACE, wx.wxEVT_COMMAND_FIND_REPLACE_ALL]:
            replaceTxt = "Replace text: %s" % event.GetReplaceString()
        else:
            replaceTxt = ""

    def OnFindClose(self, event):
        event.GetDialog().Destroy()
 # mandatory lines to get program running.
if __name__ == "__main__":
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    app.MainLoop()
