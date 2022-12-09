# 2022.11.29 This file contains all ID tags so that we can be completely sure there are no clashes between WriteR and WriteQuarto
# it shoudl become redundant as wx.ID_ANY gets rolled out

import wx


# wx.Window.NewControlId()

# set up some ID tags
ID_BUILD = wx.Window.NewControlId()
ID_KNIT2HTML = wx.Window.NewControlId()
ID_KNIT2PDF = wx.Window.NewControlId()
ID_SETTINGS = wx.Window.NewControlId()

ID_FINDONLY = wx.Window.NewControlId()
ID_FINDNEXT = wx.Window.NewControlId()
ID_FINDPREV = wx.Window.NewControlId()
ID_FINDREPLACE = wx.Window.NewControlId()
ID_GOTO  = wx.Window.NewControlId()
ID_WORDCOUNT = wx.Window.NewControlId()

ID_SETMARK = wx.Window.NewControlId()
ID_SELECTTOMARK = wx.Window.NewControlId()

ID_ALTERNATE_FOCUS = wx.Window.NewControlId()


ID_RCOMMAND = wx.Window.NewControlId()
ID_COMMENTOUT = wx.Window.NewControlId()
ID_RCHUNK = wx.Window.NewControlId()
ID_RGRAPH = wx.Window.NewControlId()
ID_RPIPE = wx.Window.NewControlId()
ID_RLASSIGN = wx.Window.NewControlId()
ID_RRASSIGN = wx.Window.NewControlId()

# IDs for headings
ID_H1 = wx.Window.NewControlId() 
ID_H2 = wx.Window.NewControlId() 
ID_H3 = wx.Window.NewControlId() 
ID_H4 = wx.Window.NewControlId() 
ID_H5 = wx.Window.NewControlId() 
ID_H6 = wx.Window.NewControlId()

ID_DIRECTORY_CHANGE = wx.Window.NewControlId()
ID_CRAN = wx.Window.NewControlId()
ID_R_PATH = wx.Window.NewControlId()
ID_BUILD_COMMAND = wx.Window.NewControlId()
ID_KNIT2HTML_COMMAND = wx.Window.NewControlId()
ID_KNIT2PDF_COMMAND = wx.Window.NewControlId()
ID_NEWTEXT = wx.Window.NewControlId()



### N.B. we should be able to eliminate the creation of these ID tags with wx.ID_ANY

# symbols menu for mathematical symbols
ID_SYMBOL_INFINITY = wx.Window.NewControlId() 
ID_SYMBOL_MINUSPLUS = wx.Window.NewControlId() 
ID_SYMBOL_PLUSMINUS = wx.Window.NewControlId() 
ID_SYMBOL_TIMES = wx.Window.NewControlId() 
ID_SYMBOL_PARTIAL = wx.Window.NewControlId() 
ID_SYMBOL_LEFTPAREN = wx.Window.NewControlId() 
ID_SYMBOL_RIGHTPAREN = wx.Window.NewControlId() 
ID_SYMBOL_LEFTSQUARE = wx.Window.NewControlId() 
ID_SYMBOL_RIGHTSQUARE = wx.Window.NewControlId() 
ID_SYMBOL_LEFTCURLY = wx.Window.NewControlId() 
ID_SYMBOL_RIGHTCURLY = wx.Window.NewControlId()
ID_SYMBOL_GRTREQL = wx.Window.NewControlId() 
ID_SYMBOL_LESSEQL = wx.Window.NewControlId() 
ID_SYMBOL_NOTEQL = wx.Window.NewControlId() 


ID_SQUAREROOT = wx.Window.NewControlId() 
ID_MATHBAR = wx.Window.NewControlId() 
ID_ABSVAL = wx.Window.NewControlId() 
ID_FRACTION = wx.Window.NewControlId() 
ID_SUMMATION = wx.Window.NewControlId() 
ID_INTEGRAL = wx.Window.NewControlId() 
ID_PRODUCT = wx.Window.NewControlId() 
ID_LIMIT = wx.Window.NewControlId() 
ID_DOUBLESUMMATION = wx.Window.NewControlId() 
ID_DOUBLEINTEGRAL = wx.Window.NewControlId()


# Greek menu for Greek letters
ID_GREEK_ALPHA = wx.Window.NewControlId() 
ID_GREEK_BETA = wx.Window.NewControlId() 
ID_GREEK_GAMMA = wx.Window.NewControlId() 
ID_GREEK_DELTA = wx.Window.NewControlId() 
ID_GREEK_EPSILON = wx.Window.NewControlId() 
ID_GREEK_VAREPSILON = wx.Window.NewControlId() 
ID_GREEK_ZETA = wx.Window.NewControlId() 
ID_GREEK_ETA = wx.Window.NewControlId() 
ID_GREEK_THETA = wx.Window.NewControlId() 
ID_GREEK_VARTHETA = wx.Window.NewControlId() 
ID_GREEK_IOTA = wx.Window.NewControlId() 
ID_GREEK_KAPPA = wx.Window.NewControlId() 
ID_GREEK_LAMBDA = wx.Window.NewControlId() 
ID_GREEK_MU = wx.Window.NewControlId() 
ID_GREEK_NU = wx.Window.NewControlId() 
ID_GREEK_XI = wx.Window.NewControlId() 
ID_GREEK_OMICRON = wx.Window.NewControlId() 
ID_GREEK_PI = wx.Window.NewControlId() 
ID_GREEK_RHO = wx.Window.NewControlId() 
ID_GREEK_SIGMA = wx.Window.NewControlId() 
ID_GREEK_TAU = wx.Window.NewControlId() 
ID_GREEK_UPSILON = wx.Window.NewControlId() 
ID_GREEK_PHI = wx.Window.NewControlId() 
ID_GREEK_CHI = wx.Window.NewControlId() 
ID_GREEK_PSI = wx.Window.NewControlId() 
ID_GREEK_OMEGA = wx.Window.NewControlId()
