# 2022.11.29 This file needs careful checking to ensure it remains totally independent of implementation
#    so that we can be sure it remains useful for WriteR and WriteQuarto

import wx
from MathInserts import *
import MathInserts 





def MakeMathsMenu(self, MainMenu):
        mathsMenu = wx.Menu()
        symbolsMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (wx.ID_ANY, "infinity\tCtrl+Shift+I", "insert infinity", OnSymbol_infinity), 
                 (wx.ID_ANY, "times\tCtrl+Shift+*", "insert times", OnSymbol_times), 
                 (wx.ID_ANY, "partial derivative\tCtrl+Shift+D", "insert partial", OnSymbol_partial), 
                 (wx.ID_ANY, "plus or minus\tCtrl+Shift+=", "insert plus or minus sign", OnSymbol_plusminus), 
                 (wx.ID_ANY, "minus or plus\tCtrl+Shift+-", "insert minus or plus sign", OnSymbol_minusplus), 
                 (wx.ID_ANY, "less than or equal\tCtrl+Shift+<", "insert less than or equal sign", OnSymbol_leq), 
                 (wx.ID_ANY, "greater than or equal \tCtrl+Shift+>", "insert greater than or equal sign", OnSymbol_geq), 
                 (wx.ID_ANY, "not equal\tCtrl+Shift+!", "insert not equal sign", OnSymbol_neq), 
                 (wx.ID_ANY, "Left Parenthesis\tCtrl+9", "insert variable size left parenthesis", OnSymbol_LeftParen), 
                 (wx.ID_ANY, "Right Parenthesis\tCtrl+0", "insert variable size right parenthesis", OnSymbol_RightParen), 
                 (wx.ID_ANY, "Left Square bracket\tCtrl+[", "insert variable size left square bracket", OnSymbol_LeftSquare), 
                 (wx.ID_ANY, "Right Square bracket\tCtrl+]", "insert variable size right square bracket", OnSymbol_RightSquare), 
                 (wx.ID_ANY, "Left Curly bracket\tCtrl+Shift+{", "insert variable size left curly bracket", OnSymbol_LeftCurly), 
                 (wx.ID_ANY, "Right Curly bracket\tCtrl+Shift+}", "insert variable size right curly bracket", OnSymbol_RightCurly)]:
            if id == None:
                symbolsMenu.AppendSeparator()
            else:
                item = symbolsMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.Append(-1, "Symbols", symbolsMenu)
        structuresMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (wx.ID_ANY, "Square root\tAlt+Ctrl+Shift+R", "insert a square root", OnSquareRoot), 
                 (wx.ID_ANY, "bar \tCtrl+Shift+B", "insert a bar operator", OnMathBar), 
                 (wx.ID_ANY, "Absolute values\tCtrl+Shift+A", "insert left and right absolute value delimiters", OnAbsVal), 
                 (wx.ID_ANY, "Fraction\tCtrl+Shift+/", "insert a fraction", OnFraction), 
                 (wx.ID_ANY, "Summation\tAlt+Ctrl+Shift+S", "insert a summation", OnSummation), 
                 (wx.ID_ANY, "Integral\tAlt+Ctrl+Shift+I", "insert an integral", Onintegral), 
                 (wx.ID_ANY, "Product\tAlt+Ctrl+Shift+P", "insert a product", OnProduct), 
                 (wx.ID_ANY, "limit\tAlt+Ctrl+Shift+L", "insert a limit", OnLimit), 
                 (wx.ID_ANY, "Double summation\tAlt+Ctrl+Shift+D", "insert a double summation", OnDoubleSummation), 
                 (wx.ID_ANY, "Double integral", "insert a double integral", OnDoubleIntegral)]:
            if id == None:
                structuresMenu.AppendSeparator()
            else:
                item = structuresMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.Append(-1, "Structures", structuresMenu)# Add the structures Menu as a submenu to the maths menu
        GreekMenu = wx.Menu()
        for id, label, helpText, handler in \
                [
                 (wx.ID_ANY, "alpha\tAlt+Shift+A", "insert greek letter alpha", OnGreek_alpha), 
                 (wx.ID_ANY, "beta\tAlt+Shift+B", "insert greek letter beta", OnGreek_beta), 
                 (wx.ID_ANY, "gamma\tAlt+Shift+G", "insert greek letter gamma", OnGreek_gamma), 
                 (wx.ID_ANY, "delta\tAlt+Shift+D", "insert greek letter delta", OnGreek_delta), 
                 (wx.ID_ANY, "epsilon\tAlt+Shift+E", "insert greek letter epsilon", OnGreek_epsilon), 
                 (wx.ID_ANY, "epsilon (variant)\tAlt+Shift+V", "insert variant of greek letter epsilon", OnGreek_varepsilon), 
                 (wx.ID_ANY, "zeta\tAlt+Shift+Z", "insert greek letter zeta", OnGreek_zeta), 
                 (wx.ID_ANY, "eta\tAlt+Shift+W", "insert greek letter eta", OnGreek_eta), 
                 (wx.ID_ANY, "theta\tAlt+Shift+H", "insert greek letter theta", OnGreek_theta), 
                 (wx.ID_ANY, "theta (variant)\tAlt+Shift+/", "insert variant of greek letter theta", OnGreek_vartheta), 
                 (wx.ID_ANY, "iota\tAlt+Shift+I", "insert greek letter iota", OnGreek_iota), 
                 (wx.ID_ANY, "kappa\tAlt+Shift+K", "insert greek letter kappa", OnGreek_kappa), 
                 (wx.ID_ANY, "lambda\tAlt+Shift+L", "insert greek letter lambda", OnGreek_lambda), 
                 (wx.ID_ANY, "mu\tAlt+Shift+M", "insert greek letter mu", OnGreek_mu), 
                 (wx.ID_ANY, "nu\tAlt+Shift+N", "insert greek letter nu", OnGreek_nu), 
                 (wx.ID_ANY, "xi\tAlt+Shift+X", "insert greek letter xi", OnGreek_xi), 
                 (wx.ID_ANY, "omicron\tAlt+Shift+O", "insert greek letter omicron", OnGreek_omicron), 
                 (wx.ID_ANY, "pi\tAlt+Shift+P", "insert greek letter pi", OnGreek_pi), 
                 (wx.ID_ANY, "rho\tAlt+Shift+R", "insert greek letter rho", OnGreek_rho), 
                 (wx.ID_ANY, "sigma\tAlt+Shift+S", "insert greek letter sigma", OnGreek_sigma), 
                 (wx.ID_ANY, "tau\tAlt+Shift+T", "insert greek letter tau", OnGreek_tau), 
                 (wx.ID_ANY, "upsilon\tAlt+Shift+U", "insert greek letter upsilon", OnGreek_upsilon), 
                 (wx.ID_ANY, "phi\tAlt+Shift+F", "insert greek letter phi", OnGreek_phi), 
                 (wx.ID_ANY, "chi\tAlt+Shift+C", "insert greek letter chi", OnGreek_chi), 
                 (wx.ID_ANY, "psi\tAlt+Shift+Y", "insert greek letter psi", OnGreek_psi), 
                 (wx.ID_ANY, "omega\tAlt+Shift+.", "insert greek letter omega", OnGreek_omega)]:
            if id == None:
                GreekMenu.AppendSeparator()
            else:
                item = GreekMenu.Append(wx.ID_ANY, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
        mathsMenu.Append(-1, "Greek letters", GreekMenu)
        MainMenu.Append(mathsMenu, "Maths")  # Add the maths Menu to the MenuBar

