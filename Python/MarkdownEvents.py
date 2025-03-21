# basic markdown and formatting

import re

from Settings import AppName


def Add2bits(self, event, fromText="", toText="", newPos=0):
    frm, to = self.editor.GetSelection()
    self.editor.SetInsertionPoint(to)
    self.editor.WriteText(toText)
    self.editor.SetInsertionPoint(frm)
    self.editor.WriteText(fromText)
    self.editor.SetInsertionPoint(frm + newPos)


def OnSquareBrack(self, event):
    Add2bits(self, event, fromText="[", toText="]", newPos=2)


def OnCurlyBrack(self, event):
    Add2bits(self, event, fromText="{", toText="}", newPos=2)


def OnRoundBrack(self, event):
    Add2bits(self, event, fromText="(", toText=")", newPos=2)


def OnAddHeadBlock(self, event):
    self.editor.SetInsertionPoint(0)
    self.editor.WriteText('---\ntitle: ""\nauthor: ""\ndate: ""\n')
    if AppName == "WriteR":
        self.editor.WriteText("output: html_document\n")
    elif AppName == "QuartoWriter":
        self.editor.WriteText(
            'bibliography: foo.bib\ntoc: true\nnumber-sections: true\nreference-location: document\nhighlight-style: pygments\nmermaid-format: png\ncode-line-numbers: true\ntidy: true\nfig-align: center\nexecute:\n  echo: true\nformat:\n  html:\n    anchor-sections: false\n    code-tools: true\n    code-fold: show\n    code-summary: "Show the code"\n    code-overflow: wrap\n    code-block-border-left: true\n    code-copy: true\n    mainfont: Source Sans Pro\n    theme: journal\n    toc-depth: 3\n    toc-location: left\n    captions: true\n    cap-location: margin\n    table-captions: true\n    tbl-cap-location: margin\n'
        )
    self.editor.WriteText("---\n\n")
    self.editor.SetInsertionPoint(13)


def OnAddReference(self, event):
    self.editor.WriteText(" [@ref] ")


def OnAddURL(self, event):
    self.editor.WriteText(" [alt text](http://) ")


def OnAddEMail(self, event):
    self.editor.WriteText(" [name](Mailto:) ")


def OnAddFigure(self, event):
    self.editor.WriteText(" ![alt tag](filename) ")


def OnHeading1(self, event):
    self.editor.WriteText("\n")
    if AppName == "ScriptR":
        self.editor.WriteText("#' ")
    self.editor.WriteText("# ")


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


def OnMath(self, event):
    Add2bits(self, event, fromText="$", toText="$", newPos=2)


def OnItalic(self, event):
    Add2bits(self, event, fromText="*", toText="*", newPos=2)


def OnBold(self, event):
    Add2bits(self, event, fromText="**", toText="**", newPos=4)


def OnCode(self, event):
    Add2bits(self, event, fromText="`", toText="`", newPos=2)


def OnHTMLComment(self, event):
    Add2bits(self, event, fromText="<!--\n", toText="\n-->", newPos=15)


def OnAddSeparator(self, event):
    self.editor.WriteText("\n")
    if AppName == "ScriptR":
        self.editor.WriteText("#' ")
    self.editor.WriteText("--- \n")


def MakeLowerCase(self, event):
    frm, to = self.editor.GetSelection()
    selected_text = self.editor.GetValue()[frm:to]
    new_text = selected_text.lower()
    self.editor.Replace(frm, to, new_text)


def MakeUpperCase(self, event):
    frm, to = self.editor.GetSelection()
    selected_text = self.editor.GetValue()[frm:to]
    new_text = selected_text.upper()
    self.editor.Replace(frm, to, new_text)


def MakeTitleCase(self, event):
    frm, to = self.editor.GetSelection()
    selected_text = self.editor.GetValue()[frm:to]
    new_text = selected_text.title()
    self.editor.Replace(frm, to, new_text)


def MakeCapsCase(self, event):
    frm, to = self.editor.GetSelection()
    selected_text = self.editor.GetValue()[frm:to]
    new_text = selected_text.capitalize()
    self.editor.Replace(frm, to, new_text)


def MakeSnakeCase(self, event):
    frm, to = self.editor.GetSelection()
    selected_text = self.editor.GetValue()[frm:to]
    # Replace spaces and special characters with underscores
    snake_case_text = re.sub(r"[\W_]+", "_", selected_text)
    # Convert to lowercase
    snake_case_text = snake_case_text.lower()
    # Remove leading and trailing underscores
    snake_case_text = snake_case_text.strip("_")
    self.editor.Replace(frm, to, snake_case_text)


def MakeCamelCase(self, event):
    frm, to = self.editor.GetSelection()
    text = self.editor.GetValue()[frm:to]
    # Split the text by spaces
    words = text.split()
    # Capitalize the first letter of each word (except the first word)
    camel_case_words = [words[0].lower()] + [word.capitalize() for word in words[1:]]
    # Join the words to form the camel case string
    camel_case_string = "".join(camel_case_words)
    self.editor.Replace(frm, to, camel_case_string)


def SnakeToCamelCase(self, event):
    frm, to = self.editor.GetSelection()
    snake_case_string = self.editor.GetValue()[frm:to]
    # Split the snake case string by underscores
    words = snake_case_string.split("_")
    # Capitalize the first letter of each word (except the first word)
    camel_case_words = [words[0]] + [word.capitalize() for word in words[1:]]
    # Join the words to form the camel case string
    camel_case_string = "".join(camel_case_words)
    self.editor.Replace(frm, to, camel_case_string)


def CamelToSnakeCase(self, event):
    frm, to = self.editor.GetSelection()
    camel_case_string = self.editor.GetValue()[frm:to]
    snake_case_string = re.sub(r"(?<!^)(?=[A-Z])", "_", camel_case_string)
    # Convert to lowercase
    snake_case_string = snake_case_string.lower()
    self.editor.Replace(frm, to, snake_case_string)


# NOT WORKING
def OnIndent(self, event):
    frm, to = self.editor.GetSelection()
    selected_text = self.editor.GetValue()[(frm - 2) : (to - 5)]
    lines = selected_text.split("\n")
    new_text = "\n    ".join(lines)
    self.editor.Replace(frm, to, new_text)


# end of file
