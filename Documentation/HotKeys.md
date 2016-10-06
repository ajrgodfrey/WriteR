---
title: "Hot keys for use in WriteR"
author: "A. Jonathan R. Godfrey"
date: "Last updated: 6 October 2016"
output: html_document
---


## Introduction

WriteR has many hot keys; in fact, I've tried to ensure all menu items have a corresponding hot key.

I've sorted the hot keys into sets that I think make sense. Some hot keys are very standard Windows hot keys because I use Windows and so do most of the people WriteR is meant to serve.



## Common Windows operations

| Hot Key | Function |
| --- | --- |
| Ctrl+a | Select all |
| Ctrl+b | Bold. Does not undo itself, nor does undo (Ctrl+z work on it) |
| Ctrl+c | Copy to the clipboard |
| Ctrl+d | Select a font for the display (not the final document |
| Ctrl+f | Find. Not implemented properly yet. |
| Ctrl+h | Find/replace. Not implemented yet. |
| Ctrl+i | Italic. Does not undo itself, nor does undo (Ctrl+z work on it) |
| Ctrl+n | Start a new file |
| Ctrl+o | Open a file |
| Ctrl+s | Save using the current filename |
| Ctrl+Shift+s | Save using a new filename |
| Ctrl+v | Paste from clipboard |
| Ctrl+x | Cut to clipboard |
| Ctrl+z | Undo. Not so well-behaved as users might expect.  |
| Alt+f4 | Close WriteR |


## Not so common Windows hot keys


| Hot key | Functionality |
| --- | --- |
| Ctrl+q | Quit and save. Equivalent to Ctrl+s followed by Alt+f4 |
| Ctrl+- | Reduce font size for display font. |
| Ctrl+= | Increase font size for display font. |

## Mathematical symbols, including Greek letters 

These commands are all intended to produce LaTeX commands that are inserted in between single or double dollar signs for inline and newline based mathemathematical content respectively.


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


## Mathematical functions and structures

These commands are all intended to produce LaTeX commands that are inserted in between single or double dollar signs for inline and newline based mathemathematical content respectively. They add placeholder text that needs to be replaced.

| Hot key | Functionality |
| --- | --- |
| Alt+Ctrl+Shift+I | Integral |
| Alt+Ctrl+Shift+R | Square root |
| Alt+Ctrl+Shift+S | Summation |



## Bracketing functions

The first set of hot keys  is for inserting mathematical brackets one by one, and are used in math mode.

| Hot key | Functionality |
| --- | --- |
| Ctrl+9 | Left parenthesis (round bracket) for math |
| Ctrl+0 | Right parenthesis (round bracket) for math |
| Ctrl+[ | Left square bracket for math |
| Ctrl+] | Right square bracket for math |
| Ctrl+Shift+{ | Left curly bracket for math |
| Ctrl+Shift+} | Right curly bracket for math |

The second set of hot keys add bracketing before and after highlighted  text. They are generally expected to be used in math mode.

| Hot key | Functionality |
| --- | --- |
| Alt+Shift+( | parentheses a.k.a. round brackets for text |
| Alt+[ | square brackets for text |
| Alt+Shift+{ | curly brackets a.k.a. braces for text |
| Alt+Shift+) | parentheses a.k.a. round brackets for math |
| Alt+] | square brackets for math |
| Alt+Shift+} | curly brackets a.k.a. braces for math |


