# 2022.12.03 this file is for the processing of files using quarto
#      It is therefore intended solely for QuartoWriter, not WriteR

import wx
import sys
from wx.py.shell import Shell
from wx.aui import AuiManager, AuiPaneInfo
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT
from os.path import join, split, isdir, expanduser, realpath
from os import walk
from time import asctime, sleep


def QuartoRenderCmd(file):
    "quarto render " + file

def QuartoPreviewCmd(file):
    "quarto preview " + file



def QuartoVersionCmd():
    "quarto --version"

