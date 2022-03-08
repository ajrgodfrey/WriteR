# WriteR for Windows

A decent attempt has been made to make an executable and and installation executable version of WriteR for Windows users.

This folder contains the instructions (below) and tools used to make the  compiled executable and the installer file.

It is intended for developers, not users.

If you do not know how to use these files, please steer away from them.



## Using the files

The files in this folder of the repo need to be moved to the folder above the repo when it is pulled down to a developer's machine, so that the commands in them do not affect the repo itself. You will see reference to a a folder called "PackageFiles" which is the top of the repo as it was originally set up, way, way back when it all began. If you call the repo something else, then you will need to edit the files accordingly.



## Creating the executable

The current tool used to create a folder and a single file version of WriteR is done using the Python module pyinstaller. The folder is what gets used by the installer, while the single file can be shared as a separate download if needed.


The Nullsoft installer creator is being used to build the installation file. This uses the settings/script file `installerCreation.nsi` in this folder. A version of NSIS will be needed to make use of this script.




## Work to do

Aside from the comments about desirable features for the app, the remaining desirable features for he installer are:

1. to add the app's folder  to the system path so that it can be called from anywhere.
2. To ensure that Rmd files are associated with the app so that clicking on files automatically opens WriteR. This can be achieved manually but it would be nice to automate this outcome.



