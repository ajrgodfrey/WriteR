# WriteR application 


## System requirements
WriteR is intended for use with R markdown files. Users must have R installed and several R packages if they are to process markdown files into HTML or Microsoft Word's docx format; in addition, an installation of a LaTeX, probably miktex2.9 will be needed if the documents are to be processed into pdf files.

Perhaps the easiest way to ensure the necessary R add-on packages are installed is to install the BrailleR add-on package.
 

This repository was established 8 January 2016 after a meeting Jonathan had with James in Petone.


## 6 February 2016

Talk delivered on 4 February at DEIMS 2016 held at Shonan Village Center, Kanegawa, Japan.

## 6 March 2016

Time to get the main script out there for consumption and contributions.
- added Program folder. This can be used without Python installed. Copy the folder somewhere useful and look for WriteR.exe inside it.
- The wholly self contained executable called WriteR.exe can be used instead of the set of files in the Program folder. It is suggested that this may load more slowly but I couldn't see the difference. Take it alone and put in a folder that is on the path.



## 8 March 2016

Python development is now  just being handled by Jonathan Godfrey. Look for progress via C++ scripts instead.

## 15 April 2016

AJRG met with Timothy Bilton and we added some consideration for alternativ build methods

## 17-20 April 2016

- AJRG added Greek menu for insertion of Greek letters via LaTeX source and a few other menu items.
- AJRG altered some menu items to be submenus and continued to add more R markdown and LaTeX shortcuts.

## 28 May 2016

- AJRG added some more R shortcuts.
- AJRG fixed some redundant options in WriteROptions

## 30 May 2016
- AJRG ported this version into the BrailleR package.

## 2 June 2016

And so quickly, the world falls apart. The executable seems broken on my machine, as do versions going well back. The pyw script does work as expected though. NB this is only the single file WriteR.exe; the executable as a folder of files does perform properly. (Oct 2016)

## 22 September 2016

- AJRG fixed bug that had italics and bold face commands switched.
- AJRG added bracketing to the Format menu. Includes hot keys to wrap highlighted text string in round, square, or curly brackets.
- AJRG added varepsilon and vartheta to Greek letters menu


## October 2016

- AJRG found a way to put function definitions in a separate file. MathInserts.py was the first created.
- AJRG added more LaTeX symbols
- added documentation folder
-  aded file for hot key assignments
- AJRG ported version 161011.0 into the BrailleR package.


## May 2018

OK, it seems keeping the readme up to date was overlooked for a while! 

- The current version bundled with the BrailleR package is from March 2018.
- A new way of running Python scripts from within R is showing great promise. Initial testing of the reticulate package suggests that we ought to expect users to pull the latest version of WxPython down in a more automated fashion using `python pip install`; this creates a challenge in that the latest version is significantly different to the one used by AJRG until now. The question of backwards compatibility for some necessary code updates (made by Marshall Flax) remains unanswered. See the PR for MF's changes.
- It seems reasonable to expect users to have the latest formal release of WxPython from here onwards. Work is required to implement the smoother pathway inside R. This will be done in the development version of BrailleR.
- If we can expect users to have smoother access to WriteR.pyw as a BrailleR user, the need for the executable version may well be reduced.



## Work to do

- want to split the script into more easily managed parts. (Partially achieved with creation of MathInserts.py etc.)
- when we have saved, but done nothing else that alters the document, WriteR still asks us if we want to save our work. 
- A find/replace dialogue is desperately needed.
- Spell checking might then be possible.
-  direct use of pandoc instead of R for *.md files.
- various symbols need to be added to documentation for hot keys
- complete documentation for guidance to use
- more commands such as  div for divide, floor and ceiling, angle brackets, nth root (has square brackets), left and right without brackets, hat, and  widehat. 

