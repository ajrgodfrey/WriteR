# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx
        mathsMenu = wx.Menu()
        symbolsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_SYMBOL_INFINITY, "infinity\tCtrl+Shift+I", "insert infinity", self.OnSymbol_infinity), 
                 (ID_SYMBOL_TIMES, "times\tCtrl+Shift+*", "insert times", self.OnSymbol_times), 
                 (ID_SYMBOL_PARTIAL, "partial derivative\tCtrl+Shift+D", "insert partial", self.OnSymbol_partial), 
                 (ID_SYMBOL_PLUSMINUS, "plus or minus\tCtrl+Shift+=", "insert plus or minus sign", self.OnSymbol_plusminus), 
                 (ID_SYMBOL_MINUSPLUS, "minus or plus\tCtrl+Shift+-", "insert minus or plus sign", self.OnSymbol_minusplus), 
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
        mathsMenu.Append(-1, "Symbols", symbolsMenu)
        structuresMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (ID_SQUAREROOT, "Square root\tAlt+Ctrl+Shift+R", "insert a square root", self.OnSquareRoot), 
                 (ID_MATHBAR, "bar \tCtrl+Shift+B", "insert a bar operator", self.OnMathBar), 
                 (ID_ABSVAL, "Absolute values\tCtrl+Shift+A", "insert left and right absolute value delimiters", self.OnAbsVal), 
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
        mathsMenu.Append(-1, "Structures", structuresMenu)# Add the structures Menu as a submenu to the main menu
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
        mathsMenu.Append(-1, "Greek letters", GreekMenu)
        menuBar.Append(mathsMenu, "Maths")  # Add the maths Menu to the MenuBar

