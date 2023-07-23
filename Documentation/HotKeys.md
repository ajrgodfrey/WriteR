---
title: "Hot keys for use in ScriptR and WriteR"
author: "A. Jonathan R. Godfrey"
date: "Last updated: 23 July 2023"
output: html_document
---


## Introduction

WriteR has many hot keys; in fact, I've tried to ensure all menu items have a corresponding hot key. ScriptR does not have all the features of WriteR; QuartoWriteR is just WriteR for Quarto markdown documents so the hot keys are the same.

I've sorted the hot keys into sets that I think make sense. Some hot keys are very standard Windows hot keys because I use Windows and so do most of the people ScriptR/WriteR is meant to serve.



## Common Windows operations

| Hot Key | Function |
| --- | --- |
| Ctrl+a | Select all |
| Ctrl+b | Bold. Does not undo itself, nor does undo (Ctrl+z) work on it; not available in ScriptR |
| Ctrl+c | Copy to the clipboard |
| Ctrl+d | Select a font for the display (not the final document |
| Ctrl+f | Find. |
| Ctrl+g | go to line |
| Ctrl+h | Find/replace. |
| Ctrl+i | Italic. Does not undo itself, nor does undo (Ctrl+z) work on it; not available in ScriptR |
| Ctrl+n | Start a new file |
| Ctrl+o | Open a file |
| Ctrl+s | Save using the current filename |
| Ctrl+Shift+s | Save using a new filename |
| Ctrl+v | Paste from clipboard |
| Ctrl+w | Word count; not available in ScriptR |
| Ctrl+x | Cut to clipboard |
| Ctrl+z | Undo. Not so well-behaved as users might expect.  |
| Alt+f4 | Close the application|


## Not so common Windows hot keys


| Hot key | Functionality |
| --- | --- |
| Ctrl+q | Quit and save. Equivalent to Ctrl+s followed by Alt+f4 |
| Ctrl+- | Reduce font size for display font. |
| Ctrl+= | Increase font size for display font. |


## Markdown formatting

N.B. Most of these functions are not available in ScriptR.

Headings are of levels 1 to 6 and are all obtained using the Alt key in conjunction with the number for the desired level of heading.

To turn a text string into a math object, highlight the desired text and use Ctrl+4. This places a dollar sign before and after the text. Note that a double dollar can be inserted if no text is highlighted.

Similarly, use Ctrl+` to change a text string into a code font.

The markdown syntax for figures, URLs, email addresses, and a header (preamble)  is inserted using the hot keys Ctrl+Shift in conjunction with the initial letter.

To comment out a selection, or just insert the delimiters for a comment, use Alt+Shift+#



## R and R markdown 

R markdown is a specific flavour of markdown that is purpose-designed to add functionality for R statistical software. These hot keys and the associated functionality are not relevant for other markdown documents unless explicitly stated. Quarto markdown has similar functionality, albeit different syntax at times.

| Hot key | Functionality |
| --- | --- |
| Alt+c  | insert an inline R command  |
| Alt+r  | insert R code chunk |
| Alt+g  | insert R code chunk with additional content needed  for graphs |
| Alt+P | insert Python code chunk |
| Ctrl+< | left assignment operator <- |
| Ctrl+> | right assignment operator -> |
 | Ctrl+Shift+P | the pipe operator |


## Mathematical symbols, including Greek letters; not available in ScriptR 

These commands are all intended to produce LaTeX commands that are inserted in between single or double dollar signs for inline and newline based mathemathematical content respectively.



### Mathematical symbols

| Hot key | Functionality |
| --- | --- |
| Ctrl+Shift+* | common multiplication symbol |
| Ctrl+Shift+D | partial derivative, pronounced "del" |
| Ctrl+Shift+I | infinity |
| Ctrl+Shift+< | less than or equal sign |
| Ctrl+Shift+> | greater than or equal sign |
| Ctrl+Shift+! | not equal sign |
| Ctrl+Shift+- | "minus or plus" sign |
| Ctrl+Shift+= | "plus or minus" sign |

### Greek letters 

Lower case Greek letters use  Alt`+Shift` and the initial letter for alpha, beta, gamma, delta etc. Only exceptions to this rule are given in the table below. The hot key assignments  are based on how letters are written, not necessarily which letter of the English alphabet they most closely represent. Upper case Greek is not represented via hot keys, nor are the variants varrho, varsigma, and varphi.

| Hot key | Functionality |
| --- | --- |
| Alt+Shift+V | varepsilon |
| Alt+Shift+W | eta |
| Alt+Shift+H | theta |
| Alt+Shift+/ | vartheta |
| Alt+Shift+F | phi |
| Alt+Shift+C | chi |
| Alt+Shift+Y | psi |
| Alt+Shift+. | omega |


## Mathematical functions and structures; not available in ScriptR

These commands are all intended to produce LaTeX commands that are inserted in between single or double dollar signs for inline and newline based mathemathematical content respectively. They add placeholder text that needs to be replaced.

| Hot key | Functionality |
| --- | --- |
| Ctrl+Shift+B | bar, as for the mean of x |
| Alt+Ctrl+Shift+I | Integral |
| Alt+Ctrl+Shift+R | Square root |
| Alt+Ctrl+Shift+S | Summation |



## Bracketing functions

The first set of hot keys  is for inserting mathematical brackets one by one, and are used in math mode. Use of these hot keys ensure the resulting symbols are allowed to vary in size as required by the context; not available in ScriptR.

| Hot key | Functionality |
| --- | --- |
| Ctrl+9 | Left parenthesis (round bracket) for math |
| Ctrl+0 | Right parenthesis (round bracket) for math |
| Ctrl+[ | Left square bracket for math |
| Ctrl+] | Right square bracket for math |
| Ctrl+Shift+{ | Left curly bracket for math |
| Ctrl+Shift+} | Right curly bracket for math |

The second set of hot keys add bracketing before and after highlighted  text. They are generally expected to be used in math mode. The "left" key in a pair is for fixed size bracketing and can be used in regular text situations, while the "right" key of a pair creates variable sized bracketing and is only useful in math mode, so not available in ScriptR.

| Hot key | Functionality |
| --- | --- |
| Alt+Shift+( | parentheses a.k.a. round brackets for text |
| Alt+[ | square brackets for text |
| Alt+Shift+{ | curly brackets a.k.a. braces for text |
| Alt+Shift+) | parentheses a.k.a. round brackets for math |
| Alt+] | square brackets for math |
| Alt+Shift+} | curly brackets a.k.a. braces for math |



