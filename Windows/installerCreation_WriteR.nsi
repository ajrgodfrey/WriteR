name WriteR
OutFile "WriteRInstaller.exe"
InstallDir "C:\Program files\openAccessWare\WriteR"
#LicenseText "Warnings:"
caption "Installer for WriteR"
CompletedText "Installation of WriteR is completed."
LicenseData ..\PackageFiles\install\warning.txt
UninstallCaption "Uninstall the WriteR app."
UninstallText "Hopefully we will completely remove everythiung created when you installed WriteR."

Page license
Page directory
Page instfiles
 UninstPage uninstConfirm
 UninstPage instfiles

Section

MessageBox MB_OK "You are about to install WriteR. $\nBefore you use WriteR though, you will need an installation of both R and pandoc. $\nWriteR will open without either tool, but you won't get any benefit from its use until you do install these tools. $\n$\nWriteR is not currently added to the system path."

#ReadEnvStr $R0 "PATH"
#messagebox mb_ok '$R0'
# StrCpy $R0 "$R0;$INSTDIR\bin\"
# System::Call 'KERNEL32::SetEnvironmentVariable(t "PATH", t R0)i.r2'
# ReadEnvStr $R0 "PATH"
# messagebox mb_ok '$R0'

SetOutPath $INSTDIR
File ..\PackageFiles\Install\version.txt
File ..\PackageFiles\Install\warning.txt
SetOutPath $INSTDIR\Source
file ..\PackageFiles\Python\*.py
file ..\PackageFiles\Python\*.pyw
SetOutPath $INSTDIR\bin
file WriteR.exe 
SetOutPath $INSTDIR\doc
file ..\PackageFiles\documentation\*.*

WriteUninstaller $INSTDIR\uninstaller.exe

CreateDirectory $SMPROGRAMS\WriteR
CreateShortCut "$SMPROGRAMS\WriteR\Run WriteR app.lnk" $INSTDIR\bin\WriteR.exe "" $INSTDIR\WriteR\bin\WriteR.exe 0
CreateShortCut "$SMPROGRAMS\WriteR\Uninstall WriteR app.lnk" $INSTDIR\uninstaller.exe "" $INSTDIR\uninstaller.exe 0
SectionEnd

Section "Uninstall"
Delete "$SMPROGRAMS\WriteR\Run WriteR app.lnk"
Delete "$SMPROGRAMS\WriteR\Uninstall WriteR app.lnk"
rmDir "$SMPROGRAMS\WriteR"

Delete $INSTDIR\version.txt
Delete $INSTDIR\warning.txt
Delete $INSTDIR\Source\*.*
RMDir $INSTDIR\Source
Delete $INSTDIR\bin\*.*
RMDir $INSTDIR\bin
Delete $INSTDIR\doc\*.*
RMDir $INSTDIR\doc
Delete $INSTDIR\uninstaller.exe
RMDir $INSTDIR
SectionEnd
