# 2022.11.29 This file is for the WriteR implementation; a separate one must be created for the quarto version

buildMenu = wx.Menu()
        self.Render = buildMenu.AppendSubMenu(wx.ID_ANY, "Render the document\tF5", "Use the rmarkdown package to render the document into the chosen format")
        self.Bind(wx.EVT_MENU, self.OnRenderNull, self.Render)
        # Create render menu
        renderMenu = wx.Menu()
        self.ChooseRenderNull = renderMenu.Append(wx.ID_ANY, "Render using defaults", "Use the rmarkdown package and render function to create HTML or only the first of multiple formats specified in YAML header", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderNull, self.ChooseRenderNull)
        self.ChooseRenderHtml = renderMenu.Append(wx.ID_ANY, "Render into HTML only", "Use the rmarkdown package and render function to create HTML", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderHtml, self.ChooseRenderHtml) 
        self.ChooseRenderWord = renderMenu.Append(wx.ID_ANY, "Render into Microsoft Word only", "Use the rmarkdown package and render function to create Microsoft Word", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderWord, self.ChooseRenderWord) 
        self.ChooseRenderSlidy = renderMenu.Append(wx.ID_ANY, "Render into slidy only", "Use the rmarkdown package and render function to create a slidy presentation", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderSlidy, self.ChooseRenderSlidy) 
        self.ChooseRenderPdf = renderMenu.Append(wx.ID_ANY, "Render into pdf only", "Use the rmarkdown package and render function to create pdf", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderPdf, self.ChooseRenderPdf) 
        self.ChooseRenderAll = renderMenu.Append(wx.ID_ANY, "Render into all specified formats", "Use the rmarkdown package and render function to create multiple output documents", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU, self.OnSelectRenderAll, self.ChooseRenderAll) 
        buildMenu.Append(-1, "Set render process to...", renderMenu) # Add the render Menu as a submenu to the build menu
        for id, label, helpText, handler in \
                [
                 (ID_KNIT2HTML, "Knit to html\tF6", "Knit the script to HTML", self.OnKnit2html),
                 (ID_KNIT2PDF, "Knit to pdf\tShift+F6", "Knit the script to a pdf file using LaTeX", self.OnKnit2pdf)]:
            if id == None:
                buildMenu.AppendSeparator()
            else:
'                item = buildMenu.Append(id, label, helpText)
                self.Bind(wx.EVT_MENU, handler, item)
menuBar.Append(buildMenu, "Build")  # Add the Build Menu to the MenuBar

