# The WriteR family of applications 


WriteR  was created so that blind users could draft and compile R markdown documents. It is needed because while sighted users do this in RStudio, this software does not work well enough with the screen reading software blind people use.

WriteR also works well enough with regular markdown documents.


The advent of Quarto as the next generation of R markdown in 2022 inspired more work on WriteR. First, the syntax of Quarto is different, and second, Quarto documents can be processed outside of R. The third app in the family is a cut-back version for editing R scripts as a substitute for the novice user who does not want to dive into R markdown or Quarto at the outset.

![OpenSource](https://img.shields.io/badge/OpenSource-Yes-green)
![OSc](https://img.shields.io/badge/OS-Multi-blue)
![License](https://img.shields.io/badge/License-GPL2-yellow)


## Latest news

### ScriptR 2023.0

The first version of the app allows editing of an R script. Processing into HTML is done using the `rmarkdown` package in R. The result is an HTML page that the user must refresh.


### WriteR 2022.2

The primary reason for this new version is to create  a second application for writing quarto documents. Work is needed to pull all common content out of the primary app file into child files (modules)

Work on this version also had to deal with wxPython developments, including deprocated functionality.



### WriteR 2022.1

In March 2022, AJRG worked on making an executable and corresponding installer for Windows users.

- the executable is built using pyinstaller, with both a folder and a single file version.
- Nullsoft is the tool being used to create the Windows installer.
- a version number was added to the distribution. This duplicates information held in the Help menu.


## System requirements for WriteR


### R and R markdown processing

WriteR is intended for use with R markdown files. Users must have R and Pandoc installed and several R packages if they are to process markdown files into HTML or Microsoft Word's docx format; in addition, an installation of a LaTeX, probably miktex2.9 will be needed if the documents are to be processed into pdf files.


Perhaps the easiest way to ensure the necessary R add-on packages are installed is to install the BrailleR add-on package.

An installation of Quarto includes pandoc, but not R. 

### Python requirements

If you do not use the dedicated Windows installer for WriteR, you will need to use the original source Python scripts.  
To get WriteR to run using the Python script files, users must have Python 3.8 installed and the corresponding version of wxPython. Once Python 3.8 is installed, the command line "`pip install wxPython`" can be issued to install the wx module, or if it is already there, "`pip install -U wxPython`" will update it. N.B. The capitalisation  of U and P was intentional (and is required).


## Work to do

- want to split the script into more easily managed parts. (Partially achieved with creation of MathInserts.py etc.)
- when we have saved, but done nothing else that alters the document, WriteR still asks us if we want to save our work. 
- Spell checking might now be possible.
-  direct use of pandoc instead of R for *.md files.
- various symbols need to be added to documentation for hot keys. This is work in progress but seems fairly complete.
- complete documentation for guidance to use
- more commands such as  div for divide, floor and ceiling, angle brackets, nth root (has square brackets), left and right without brackets, hat, and  widehat. 

