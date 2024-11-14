# import external modules
import sys
from threading import Event
from os.path import split, realpath
import winsound

import wx
import wx.adv
from wx.aui import AuiManager, AuiPaneInfo

# import our modules
from Settings import (
    AppName,
    AppSettings,
)  # for making sure the correct app is being opened.
import FileMenuEvents  # for opening and closing files
import EditMenuEvents  # for editing content
import ViewMenuEvents  # for managing the main window
import MyConsole  # for displaying outcome of processing
import RMarkdownEvents  # for processing files
import RCodeEvents  # for code inserts
import MarkdownEvents  # for formatting and inserts in text
import MathInserts  # for equations
import HelpMenuEvents  # for help with the specific apps


beep = "winsound" in sys.modules


# get on with the program
class MainWindow(wx.Frame):
    """This is the front facing document editor space and all its menus and events"""

    def __init__(
        self,
        parent=None,
        id=-1,
        title="",
        pos=wx.DefaultPosition,
        size=(1200, 700),
        style=wx.DEFAULT_FRAME_STYLE | wx.SUNKEN_BORDER | wx.CLIP_CHILDREN,
        filename="untitled." + AppSettings["extension"][AppName],
    ):
        super(MainWindow, self).__init__(parent, id, title, pos, size, style)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self._mgr = AuiManager()
        self._mgr.SetManagedWindow(self)
        self.focusConsole = False
        self.ChosenFontSize = 14
        self.font = wx.Font(
            self.ChosenFontSize, wx.MODERN, wx.NORMAL, wx.NORMAL, False, "Consolas"
        )
        self.settings = {
            "lastdir": ".",
            "filename": "none",
            "newText": AppSettings["startingText"][AppName],
            "RDirectory": self.GetRDirectory(),
        }
        if len(sys.argv) > 1:
            self.settings["lastdir"], self.settings["filename"] = split(
                realpath(sys.argv[-1])
            )
            self.filename = self.settings["filename"]
            self.dirname = self.settings["lastdir"]
            self.CreateExteriorWindowComponents()
            self.CreateInteriorWindowComponents()
            self.fileOpen(self.dirname, self.filename)
        elif self.settings["filename"] == "none":
            self.filename = filename
            self.dirname = self.settings["lastdir"]
            self.CreateExteriorWindowComponents()
            self.CreateInteriorWindowComponents()
            self.OnOpen(self)
            #  set the save flag to true if OnOpen is cancelled
        else:
            self.filename = self.settings["filename"]
            self.dirname = self.settings["lastdir"]
            self.CreateExteriorWindowComponents()
            self.CreateInteriorWindowComponents()
            self.fileOpen(self.dirname, self.filename)
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
        self.editor = self.CreateTextCtrl(self.settings["newText"])
        self.console = MyConsole.MyConsole(self)
        self._mgr.AddPane(self.editor, AuiPaneInfo().Name("editor").CenterPane().Hide())
        self._mgr.GetPane("editor").Show()
        self.editor.SetFocus()
        self.editor.SelectAll()
        self.priorMatchCol = 0
        self.priorMatchRow = 0
        self._mgr.Update()

    def CreateExteriorWindowComponents(self):
        self.CreateMenu()
        self.StatusBar()
        self.SetTitle()

    def CreateMenu(self):
        menuBar = wx.MenuBar()  # create the menu bar object and add menus to it
        fileMenu = wx.Menu()
        for id, label, helpText, handler in [
            (wx.ID_NEW, "New file\tCtrl+N", "Start a new file", self.OnNewFile),
            (wx.ID_OPEN, "&Open\tCtrl+O", "Open an existing file", self.OnOpen),
            (wx.ID_SAVE, "&Save\tCtrl+S", "Save the current file", self.OnSave),
            (
                wx.ID_SAVEAS,
                "Save &As\tCtrl+Shift+S",
                "Save the file under a different name",
                self.OnSaveAs,
            ),
            (None,) * 4,
            (
                wx.ID_EXIT,
                "Quit && save\tCtrl+Q",
                "Saves the current file and closes the program",
                self.OnSafeExit,
            ),
        ]:
            if label is None:
                fileMenu.AppendSeparator()
            else:
                item = fileMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(fileMenu, "&File")  # Add the fileMenu to the MenuBar

        editMenu = wx.Menu()
        for id, label, helpText, handler in [
            (
                wx.ID_CUT,
                "Cu&t\tCtrl+X",
                "Cut highlighted text to clipboard",
                self.OnCut,
            ),
            (
                wx.ID_COPY,
                "&Copy\tCtrl+C",
                "Copy highlighted text to clipboard",
                self.OnCopy,
            ),
            (wx.ID_PASTE, "&Paste\tCtrl+V", "Paste text from clipboard", self.OnPaste),
            (
                wx.ID_SELECTALL,
                "Select all\tCtrl+A",
                "Highlight entire text",
                self.OnSelectAll,
            ),
            (wx.ID_DELETE, "&Delete", "Delete highlighted text", self.OnDelete),
            (
                wx.ID_ANY,
                "Word count\tCtrl+w",
                "get a word count of the entire text",
                self.OnWordCount,
            ),
            (None,) * 4,
            (
                wx.ID_FIND,
                "Find\tCtrl+F",
                "Open a standard find dialog box",
                self.OnShowFind,
            ),
            (wx.ID_ANY, "FindNext\tF3", "FindNext", self.F3Next),
            (wx.ID_ANY, "FindPrevious\tShift+F3", "FindPrev", self.ShiftF3Previous),
            (
                wx.ID_ANY,
                "Go to line\tCtrl+g",
                "Open a dialog box to choose a line number",
                self.OnGoToLine,
            ),
            (
                wx.ID_REPLACE,
                "Find/replace\tCtrl+H",
                "Open a find/replace dialog box",
                self.OnShowFindReplace,
            ),
            (wx.ID_ANY, "Set Mark\tCtrl+SPACE", "Set Mark", self.OnSetMark),
            (
                wx.ID_ANY,
                "Select To Mark\tAlt+Ctrl+SPACE",
                "Select To Mark",
                self.OnSelectToMark,
            ),
            (
                wx.ID_ANY,
                "Alternate Focus\tF4",
                "Alternate Focus",
                self.AlternateFocus,
            ),
            (None,) * 4,
            (
                wx.ID_PREFERENCES,
                "Settings",
                "Setup the editor to your liking",
                self.OnSettings,
            ),
        ]:
            if label is None:
                editMenu.AppendSeparator()
            else:
                item = editMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(editMenu, "&Edit")  # Add the editMenu to the MenuBar

        viewMenu = wx.Menu()
        ShowStatusBarMenu = viewMenu.Append(
            wx.ID_ANY, "Show status bar", "Show Status bar", kind=wx.ITEM_CHECK
        )
        viewMenu.Check(ShowStatusBarMenu.GetId(), True)
        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, ShowStatusBarMenu)
        IncreaseFontMenu = viewMenu.Append(
            wx.ID_ANY, "Increase the font size\tCtrl+=", "Increase the font size"
        )
        self.Bind(wx.EVT_MENU, self.OnIncreaseFontSize, IncreaseFontMenu)
        DecreaseFontMenu = viewMenu.Append(
            wx.ID_ANY, "Decrease the font size\tCtrl+-", "Decrease the font size"
        )
        self.Bind(wx.EVT_MENU, self.OnDecreaseFontSize, DecreaseFontMenu)
        ChooseFontMenu = viewMenu.Append(
            wx.ID_ANY, "Choose font\tCtrl+D", "Choose the font size and other details"
        )
        self.Bind(wx.EVT_MENU, self.OnSelectFont, ChooseFontMenu)
        menuBar.Append(viewMenu, "View")  # Add the view Menu to the MenuBar

        buildMenu = wx.Menu()
        RenderFastMenu = buildMenu.Append(
            wx.ID_ANY,
            "Render the document\tF5",
            "Use the rmarkdown package to render the current file",
        )
        self.Bind(wx.EVT_MENU, self.OnRenderNull, RenderFastMenu)
        # Create menu item to re-install rmarkdown package
        if AppName != "mdWriter":
            FixRMenu = buildMenu.Append(
                wx.ID_ANY, "Fix R packages", "reinstall the rmarkdown package "
            )
            self.Bind(wx.EVT_MENU, self.OnFixR, FixRMenu)
            CheckRMenu = buildMenu.Append(
                wx.ID_ANY, "Check R version", "get the version information from R "
            )
            self.Bind(wx.EVT_MENU, self.CheckRVersion, CheckRMenu)
        if AppName == "QuartoWriter":
            CheckQuartoMenu = buildMenu.Append(
                wx.ID_ANY,
                "Check Quarto version",
                "get the version information for Quarto ",
            )
            self.Bind(wx.EVT_MENU, self.CheckQuartoVersion, CheckQuartoMenu)
            CheckPythonMenu = buildMenu.Append(
                wx.ID_ANY,
                "Check Python version",
                "get version information for  Python ",
            )
            self.Bind(wx.EVT_MENU, self.CheckPythonVersion, CheckPythonMenu)
        else:
            CheckPandocMenu = buildMenu.Append(
                wx.ID_ANY,
                "Check Pandoc version",
                "get version information from Pandoc ",
            )
            self.Bind(wx.EVT_MENU, self.CheckPandocVersion, CheckPandocMenu)
        if AppName != "ScriptR":
            # Create render menu for WriteR etc.
            renderMenu = wx.Menu()
            renderMenu = wx.Menu()
            for label, helpText, handler in [
                (
                    "defaults",
                    "Use the render function to create HTML or only the first of multiple formats specified in YAML header",
                    self.OnSelectRenderNull,
                ),
                (
                    "HTML only",
                    "Use the render function to create HTML",
                    self.OnSelectRenderHtml,
                ),
                (
                    "Microsoft &Word only",
                    "Use the render function to create Microsoft Word",
                    self.OnSelectRenderWord,
                ),
                (
                    "slidy only",
                    "Use the render function to create a slidy presentation",
                    self.OnSelectRenderSlidy,
                ),
                (
                    "pdf only",
                    "Use the render function to create pdf",
                    self.OnSelectRenderPdf,
                ),
                (
                    "all specified formats",
                    "Use the render function to create multiple output documents",
                    self.OnSelectRenderAll,
                ),
            ]:
                item = renderMenu.Append(wx.ID_ANY, label, helpText, wx.ITEM_RADIO)
                self.Bind(wx.EVT_MENU, handler, item)

            buildMenu.Append(
                -1, "Set render process to...", renderMenu
            )  # Add the render Menu as a submenu to the build menu
            for label, helpText, handler, whichApp in [
                ("Knit to html\tF6", "Knit the script to HTML", self.OnKnit2html, "R"),
                (
                    "Knit to pdf\tShift+F6",
                    "Knit the script to a pdf file using LaTeX",
                    self.OnKnit2pdf,
                    "R",
                ),
                (
                    "Render into &HTML\tShift+f5",
                    "Use the render function to create HTML",
                    self.OnRenderHtml,
                    "md",
                ),
                (
                    "Render into Microsoft &Word",
                    "Use the render function to create Microsoft Word",
                    self.OnRenderWord,
                    "md",
                ),
                (
                    "Render into &slidy",
                    "Use the render function to create a slidy presentation",
                    self.OnRenderSlidy,
                    "md",
                ),
                (
                    "Render into &pdf",
                    "Use the render function to create pdf",
                    self.OnRenderPdf,
                    "md",
                ),
                (
                    "Render into &all specified formats",
                    "Use the render function to create multiple output documents",
                    self.OnRenderAll,
                    "md",
                ),
            ]:
                if label is None:
                    buildMenu.AppendSeparator()
                elif (
                    (whichApp == "R" and AppName == "WriteR")
                    or (whichApp == "Q" and AppName == "QuartoWriteR")
                    or whichApp == "md"
                ):
                    item = buildMenu.Append(wx.ID_ANY, label, helpText)
                    self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(buildMenu, "Build")  # Add the Build Menu to the MenuBar

        formatMenu = wx.Menu()
        for label, helpText, handler, whichApp in [
            ("indent", "", self.OnIndent, "md"),
            ("Bold\tCtrl+B", "move to bold face font", self.OnBold, "md"),
            ("Italic\tCtrl+I", "move to italic face font", self.OnItalic, "md"),
            (
                "Code\tCtrl+`",
                "present using a typewriter font commonly seen when showing code",
                self.OnCode,
                "md",
            ),
            ("Maths mode\tCtrl+4", "move text to maths mode", self.OnMath, "md"),
            (
                "Comment out a selection\tAlt+q",
                "Comment out some selected text or insert the delimiters for a comment",
                self.OnHTMLComment,
                "md",
            ),
            (
                "Round brackets\tAlt+Shift+(",
                "Wrap text in round () brackets",
                self.OnRoundBrack,
                "all",
            ),
            (
                "Square brackets\tAlt+[",
                "Wrap text in square brackets",
                self.OnSquareBrack,
                "all",
            ),
            (
                "Curly brackets\tAlt+Shift+{",
                "Wrap text in curly brackets",
                self.OnCurlyBrack,
                "all",
            ),
        ]:
            if label is None:
                formatMenu.AppendSeparator()
            elif AppName != "ScriptR" and whichApp == "md":
                item = formatMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
            elif whichApp == "all":
                item = formatMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        caseMenu = wx.Menu()
        for label, helpText, handler in [
            ("all &lower", "convert all letters to lower case", self.MakeLowerCase),
            ("all &upper", "convert all letters to upper case", self.MakeUpperCase),
            ("snake case", "convert all words to snake case", self.MakeSnakeCase),
            (
                "camel case",
                "convert all words to a camel case string",
                self.MakeCamelCase,
            ),
            (
                "snake to camel case",
                "convert a snake case string to a camel case string",
                self.SnakeToCamelCase,
            ),
            (
                "camel to snake case",
                "convert a camel case string to a snake case string",
                self.CamelToSnakeCase,
            ),
            (
                "capi&talise all words",
                "convert initials of all words to capitals",
                self.MakeTitleCase,
            ),
            (
                "capitalise &first letter",
                "convert initial letters of lines to upper case",
                self.MakeCapsCase,
            ),
        ]:
            item = caseMenu.Append(wx.ID_ANY, label, helpText)
            self.Bind(wx.EVT_MENU, handler, item)
        formatMenu.Append(-1, "Convert case", caseMenu)
        menuBar.Append(formatMenu, "f&ormat")  # Add the format Menu to the MenuBar

        insertMenu = wx.Menu()
        headingsMenu = wx.Menu()
        for label, helpText, handler in [
            ("level &1\tAlt+1", "insert heading level 1", self.OnHeading1),
            ("level &2\tAlt+2", "insert heading level 2", self.OnHeading2),
            ("level &3\tAlt+3", "insert heading level 3", self.OnHeading3),
            ("level &4\tAlt+4", "insert heading level 4", self.OnHeading4),
            ("level &5\tAlt+5", "insert heading level 5", self.OnHeading5),
            ("level &6\tAlt+6", "insert heading level 6", self.OnHeading6),
        ]:
            item = headingsMenu.Append(wx.ID_ANY, label, helpText)
            self.Bind(wx.EVT_MENU, handler, item)
        insertMenu.Append(-1, "Heading", headingsMenu)
        for label, helpText, handler, whichApp in [
            ("header/preamble\tCtrl+Shift+H", "", self.OnAddHeadBlock, "md"),
            (
                "Separator\tCtrl+Shift+Space",
                "insert a code separation line",
                self.OnAddSeparator,
                "all",
            ),
            (
                "URL\tCtrl+Shift+U",
                "insert a link to a website or file",
                self.OnAddURL,
                "md",
            ),
            (
                "e-mail\tCtrl+Shift+E",
                "insert a link to send an email",
                self.OnAddEMail,
                "md",
            ),
            (
                "Figure\tCtrl+Shift+F",
                "insert the markdown needed to insert a graphic file",
                self.OnAddFigure,
                "md",
            ),
            (
                "Reference\tCtrl+Shift+R",
                "insert the markdown for a citation",
                self.OnAddReference,
                "md",
            ),
        ]:
            if label is None:
                insertMenu.AppendSeparator()
            elif AppName != "ScriptR" and whichApp == "md":
                item = insertMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
            elif whichApp == "all":
                item = insertMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(insertMenu, "insert")  # Add the insert Menu to the MenuBar

        codeMenu = wx.Menu()
        for label, helpText, handler, whichApp in [
            (
                "Insert inline R command\tCtrl+Shift+C",
                "insert an in-line R command",
                self.OnRCommand,
                "md",
            ),
            (
                "Insert R code chunk\tAlt+R",
                "insert standard R code chunk",
                self.OnRChunk,
                "md",
            ),
            (
                "Insert R code chunk for a graph\tAlt+G",
                "insert R code chunk for a graph",
                self.OnRGraph,
                "md",
            ),
            (
                "Insert Python code chunk\tAlt+P",
                "insert standard Python code chunk",
                self.OnPythonChunk,
                "md",
            ),
            (
                "Insert a left assignment\tCtrl+<",
                "insert R code for the left assignment <-",
                self.OnRLAssign,
                "all",
            ),
            (
                "Insert a right assignment\tCtrl+>",
                "insert R code for the right assignment ->",
                self.OnRRAssign,
                "all",
            ),
            (
                "Insert a pipe operator\tCtrl+Shift+P",
                "insert R code for the pipe operator |>",
                self.OnRPipe,
                "all",
            ),
        ]:
            if label is None:
                codeMenu.AppendSeparator()
            elif (AppName != "ScriptR" and whichApp == "md") or whichApp == "all":
                item = codeMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(codeMenu, "Code")  # Add the Code Menu to the MenuBar

        # We only use the Maths menu for WriteR and QuartoWriteR, but it gets built anyway
        mathsMenu = wx.Menu()
        symbolsMenu = wx.Menu()
        for label, helpText, handler in [
            ("infinity\tCtrl+Shift+I", "insert infinity", self.OnSymbol_infinity),
            ("times\tCtrl+Shift+*", "insert times", self.OnSymbol_times),
            (
                "partial derivative\tCtrl+Shift+D",
                "insert partial",
                self.OnSymbol_partial,
            ),
            (
                "plus or minus\tCtrl+Shift+=",
                "insert plus or minus sign",
                self.OnSymbol_plusminus,
            ),
            (
                "minus or plus\tCtrl+Shift+-",
                "insert minus or plus sign",
                self.OnSymbol_minusplus,
            ),
            (
                "less than or equal\tCtrl+Shift+<",
                "insert less than or equal sign",
                self.OnSymbol_leq,
            ),
            (
                "greater than or equal \tCtrl+Shift+>",
                "insert greater than or equal sign",
                self.OnSymbol_geq,
            ),
            ("not equal\tCtrl+Shift+!", "insert not equal sign", self.OnSymbol_neq),
            (
                "Left Parenthesis\tCtrl+9",
                "insert variable size left parenthesis",
                self.OnSymbol_LeftParen,
            ),
            (
                "Right Parenthesis\tCtrl+0",
                "insert variable size right parenthesis",
                self.OnSymbol_RightParen,
            ),
            (
                "Left Square bracket\tCtrl+[",
                "insert variable size left square bracket",
                self.OnSymbol_LeftSquare,
            ),
            (
                "Right Square bracket\tCtrl+]",
                "insert variable size right square bracket",
                self.OnSymbol_RightSquare,
            ),
            (
                "Left Curly bracket\tCtrl+Shift+{",
                "insert variable size left curly bracket",
                self.OnSymbol_LeftCurly,
            ),
            (
                "Right Curly bracket\tCtrl+Shift+}",
                "insert variable size right curly bracket",
                self.OnSymbol_RightCurly,
            ),
        ]:
            if label is None:
                symbolsMenu.AppendSeparator()
            else:
                item = symbolsMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.Append(-1, "Symbols", symbolsMenu)
        structuresMenu = wx.Menu()
        for label, helpText, handler in [
            (
                "Round brackets (math)\tAlt+Shift+)",
                "Wrap math in round () brackets",
                self.OnMathRoundBrack,
            ),
            (
                "Square brackets (math)\tAlt+]",
                "Wrap math in square brackets",
                self.OnMathSquareBrack,
            ),
            (
                "Curly brackets (math)\tAlt+Shift+}",
                "Wrap math in curly brackets",
                self.OnMathCurlyBrack,
            ),
            (
                "Square root\tAlt+Ctrl+Shift+R",
                "insert a square root",
                self.OnSquareRoot,
            ),
            ("bar \tCtrl+Shift+B", "insert a bar operator", self.OnMathBar),
            (
                "Absolute values\tCtrl+Shift+A",
                "insert left and right absolute value delimiters",
                self.OnAbsVal,
            ),
            ("Fraction\tCtrl+Shift+/", "insert a fraction", self.OnFraction),
            ("Summation\tAlt+Ctrl+Shift+S", "insert a summation", self.OnSummation),
            ("Integral\tAlt+Ctrl+Shift+I", "insert an integral", self.Onintegral),
            ("Product\tAlt+Ctrl+Shift+P", "insert a product", self.OnProduct),
            ("Limit\tAlt+Ctrl+Shift+L", "insert a limit", self.OnLimit),
            (
                "Double summation\tAlt+Ctrl+Shift+D",
                "insert a double summation",
                self.OnDoubleSummation,
            ),
            ("Double integral", "insert a double integral", self.OnDoubleIntegral),
        ]:
            if label is None:
                structuresMenu.AppendSeparator()
            else:
                item = structuresMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.Append(
            -1, "Structures", structuresMenu
        )  # Add the structures Menu as a submenu to the main menu
        GreekMenu = wx.Menu()
        for label, helpText, handler in [
            ("alpha\tAlt+Shift+A", "insert greek letter alpha", self.OnGreek_alpha),
            ("beta\tAlt+Shift+B", "insert greek letter beta", self.OnGreek_beta),
            ("gamma\tAlt+Shift+G", "insert greek letter gamma", self.OnGreek_gamma),
            ("delta\tAlt+Shift+D", "insert greek letter delta", self.OnGreek_delta),
            (
                "epsilon\tAlt+Shift+E",
                "insert greek letter epsilon",
                self.OnGreek_epsilon,
            ),
            (
                "epsilon (variant)\tAlt+Shift+V",
                "insert variant of greek letter epsilon",
                self.OnGreek_varepsilon,
            ),
            ("zeta\tAlt+Shift+Z", "insert greek letter zeta", self.OnGreek_zeta),
            ("eta\tAlt+Shift+W", "insert greek letter eta", self.OnGreek_eta),
            ("theta\tAlt+Shift+H", "insert greek letter theta", self.OnGreek_theta),
            (
                "theta (variant)\tAlt+Shift+/",
                "insert variant of greek letter theta",
                self.OnGreek_vartheta,
            ),
            ("iota\tAlt+Shift+I", "insert greek letter iota", self.OnGreek_iota),
            ("kappa\tAlt+Shift+K", "insert greek letter kappa", self.OnGreek_kappa),
            ("lambda\tAlt+Shift+L", "insert greek letter lambda", self.OnGreek_lambda),
            ("mu\tAlt+Shift+M", "insert greek letter mu", self.OnGreek_mu),
            ("nu\tAlt+Shift+N", "insert greek letter nu", self.OnGreek_nu),
            ("xi\tAlt+Shift+X", "insert greek letter xi", self.OnGreek_xi),
            (
                "omicron\tAlt+Shift+O",
                "insert greek letter omicron",
                self.OnGreek_omicron,
            ),
            ("pi\tAlt+Shift+P", "insert greek letter pi", self.OnGreek_pi),
            ("rho\tAlt+Shift+R", "insert greek letter rho", self.OnGreek_rho),
            ("sigma\tAlt+Shift+S", "insert greek letter sigma", self.OnGreek_sigma),
            ("tau\tAlt+Shift+T", "insert greek letter tau", self.OnGreek_tau),
            (
                "upsilon\tAlt+Shift+U",
                "insert greek letter upsilon",
                self.OnGreek_upsilon,
            ),
            ("phi\tAlt+Shift+F", "insert greek letter phi", self.OnGreek_phi),
            ("chi\tAlt+Shift+C", "insert greek letter chi", self.OnGreek_chi),
            ("psi\tAlt+Shift+Y", "insert greek letter psi", self.OnGreek_psi),
            ("omega\tAlt+Shift+.", "insert greek letter omega", self.OnGreek_omega),
        ]:
            if label is None:
                GreekMenu.AppendSeparator()
            else:
                item = GreekMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.Append(-1, "Greek letters", GreekMenu)
        if AppName != "ScriptR":
            menuBar.Append(mathsMenu, "Maths")  # Add the maths Menu to the MenuBar

        helpMenu = wx.Menu()
        for id, label, helpText, handler, whichApp in [
            (
                wx.ID_ANY,
                "Basic help",
                "just a bit about using this program",
                self.OnBasicHelp,
                "all",
            ),
            (
                wx.ID_ABOUT,
                "About",
                "Information about this program",
                self.OnAbout,
                "all",
            ),
        ]:
            if label is None:
                helpMenu.AppendSeparator()
            else:
                item = helpMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        menuBar.Append(helpMenu, "&Help")  # Add the helpMenu to the MenuBar
        self.SetMenuBar(menuBar)  # Add the menuBar to the Frame

    def CreateTextCtrl(self, text):
        text = wx.TextCtrl(
            self,
            -1,
            text,
            wx.Point(0, 0),
            wx.Size(150, 90),
            # wx.NO_BORDER | wx.TE_MULTILINE)
            wx.TE_MULTILINE,
        )
        text.SetFont(self.font)
        return text

    def SetTitle(self, *args, **kwargs):
        # MainWindow.SetTitle overrides wx.Frame.SetTitle, so we have to
        # call it using super:
        super(MainWindow, self).SetTitle(AppName + f" -  {self.filename}")

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

    # file menu events
    OnOpen = FileMenuEvents.OnOpen
    OnClose = FileMenuEvents.OnClose
    fatalError = FileMenuEvents.fatalError
    fileOpen = FileMenuEvents.fileOpen
    OnNewFile = FileMenuEvents.OnNewFile
    OnSaveAs = FileMenuEvents.OnSaveAs
    OnSave = FileMenuEvents.OnSave
    OnExit = FileMenuEvents.OnExit
    OnSafeExit = FileMenuEvents.OnSafeExit

    # Build Menu events # conditioning needed for apps is done in RMarkdownEvents.py or in menu construction
    CheckRVersion = RMarkdownEvents.CheckRVersion
    OnFixR = RMarkdownEvents.OnFixR
    CheckQuartoVersion = RMarkdownEvents.CheckQuartoVersion
    CheckPythonVersion = RMarkdownEvents.CheckPythonVersion
    CheckPandocVersion = RMarkdownEvents.CheckPandocVersion
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
    CurrentMarkdown = RMarkdownEvents.CurrentMarkdown

    # Code Menu events
    OnRPipe = RCodeEvents.OnRPipe
    OnRLAssign = RCodeEvents.OnRLAssign
    OnRRAssign = RCodeEvents.OnRRAssign
    OnRChunk = RCodeEvents.OnRChunk
    OnRGraph = RCodeEvents.OnRGraph
    OnPythonChunk = RCodeEvents.OnPythonChunk
    OnRCommand = RCodeEvents.OnRCommand

    # MathInserts are all LaTeX input for math mode; they are all included even though not used by ScriptR; menu is blanked out for ScriptR
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
    OnAbout = HelpMenuEvents.OnAbout
    OnBasicHelp = HelpMenuEvents.OnBasicHelp

    # edit menu events ##checking some required
    OnSelectAll = EditMenuEvents.OnSelectAll
    OnDelete = EditMenuEvents.OnDelete
    OnPaste = EditMenuEvents.OnPaste
    OnCopy = EditMenuEvents.OnCopy
    OnCut = EditMenuEvents.OnCut
    OnGoToLine = EditMenuEvents.OnGoToLine
    OnSettings = EditMenuEvents.OnSettings
    OnWordCount = EditMenuEvents.OnWordCount
    OnShowFind = EditMenuEvents.OnShowFind
    OnSetMark = EditMenuEvents.OnSetMark
    F3Next = EditMenuEvents.F3Next
    ShiftF3Previous = EditMenuEvents.ShiftF3Previous
    OnFind = EditMenuEvents.OnFind
    OnFindClose = EditMenuEvents.OnFindClose
    OnShowFindReplace = EditMenuEvents.OnShowFindReplace
    OnSelectToMark = EditMenuEvents.OnSelectToMark
    #    AlternateFocus = EditMenuEvents.AlternateFocus
    #    ActuallyAlternateFocus = EditMenuEvents.ActuallyAlternateFocus
    duplicateline = EditMenuEvents.duplicateline
    lineup = EditMenuEvents.lineup
    linedown = EditMenuEvents.linedown

    # view menu events
    ToggleStatusBar = ViewMenuEvents.ToggleStatusBar
    StatusBar = ViewMenuEvents.StatusBar
    OnIncreaseFontSize = ViewMenuEvents.OnIncreaseFontSize
    OnDecreaseFontSize = ViewMenuEvents.OnDecreaseFontSize
    UpdateUI = ViewMenuEvents.UpdateUI
    OnSelectFont = ViewMenuEvents.OnSelectFont

    # format/Insert menu events
    MakeLowerCase = MarkdownEvents.MakeLowerCase
    MakeUpperCase = MarkdownEvents.MakeUpperCase
    MakeSnakeCase = MarkdownEvents.MakeSnakeCase
    CamelToSnakeCase = MarkdownEvents.CamelToSnakeCase
    MakeCamelCase = MarkdownEvents.MakeCamelCase
    MakeTitleCase = MarkdownEvents.MakeTitleCase
    SnakeToCamelCase = MarkdownEvents.SnakeToCamelCase
    MakeCapsCase = MarkdownEvents.MakeCapsCase
    OnSquareBrack = MarkdownEvents.OnSquareBrack
    OnCurlyBrack = MarkdownEvents.OnCurlyBrack
    OnRoundBrack = MarkdownEvents.OnRoundBrack
    OnItalic = MarkdownEvents.OnItalic
    OnBold = MarkdownEvents.OnBold
    OnCode = MarkdownEvents.OnCode
    OnMath = MarkdownEvents.OnMath
    OnHTMLComment = MarkdownEvents.OnHTMLComment
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
    OnIndent = MarkdownEvents.OnIndent

    # processing events (all apps)
    GetRDirectory = RMarkdownEvents.GetRDirectory

    def SetFocusConsole(self, toConsole):
        if toConsole != self.focusConsole:
            self.ActuallyAlternateFocus()

    def AlternateFocus(self, event):
        self.ActuallyAlternateFocus()

    def ActuallyAlternateFocus(self):
        if self.focusConsole:
            self.editor.SetFocus()
            if beep:
                winsound.PlaySound("e10.wav", winsound.SND_FILENAME)
        else:
            self.console.SetFocus()
            if beep:
                winsound.PlaySound("s8.wav", winsound.SND_FILENAME)
        self.focusConsole = not self.focusConsole
