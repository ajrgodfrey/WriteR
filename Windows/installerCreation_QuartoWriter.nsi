name QuartoWriter
OutFile "QuartoWriterInstaller.exe"
InstallDir "C:\Program files\openAccessWare\QuartoWriter"
#LicenseText "Warnings:"
caption "Installer for QuartoWriter"
CompletedText "Installation of QuartoWriter is completed."
LicenseData warning.txt
UninstallCaption "Uninstall the QuartoWriter app."
UninstallText "Hopefully we will completely remove everything created when you installed QuartoWriter."
SetOverwrite try

Page license
Page directory
Page instfiles
 UninstPage uninstConfirm
 UninstPage instfiles

Section

MessageBox MB_OK "You are about to install QuartoWriter. $\n $\n$\nQuartoWriter is not currently added to the system path."

#ReadEnvStr $R0 "PATH"
#messagebox mb_ok '$R0'
# StrCpy $R0 "$R0;$INSTDIR\bin\"
# System::Call 'KERNEL32::SetEnvironmentVariable(t "PATH", t R0)i.r2'
# ReadEnvStr $R0 "PATH"
# messagebox mb_ok '$R0'

SetOutPath $INSTDIR
File version.txt
File warning.txt
SetOutPath $INSTDIR\Source
file ..\PackageFiles\Python\*.py
file ..\PackageFiles\Python\*.pyw
SetOutPath $INSTDIR\bin
file QuartoWriter.dist\*.*
file ..\PackageFiles\Python\*.wav
SetOutPath $INSTDIR\bin\wx
file QuartoWriter.dist\wx\*.*
SetOutPath $INSTDIR\doc
file ..\PackageFiles\documentation\*.*

WriteUninstaller $INSTDIR\uninstaller.exe

CreateDirectory $SMPROGRAMS\QuartoWriter
CreateShortCut "$SMPROGRAMS\QuartoWriter\Run QuartoWriter app.lnk" $INSTDIR\bin\QuartoWriter.exe "" $INSTDIR\QuartoWriter\bin\QuartoWriter.exe 0
CreateShortCut "$SMPROGRAMS\QuartoWriter\Uninstall QuartoWriter app.lnk" $INSTDIR\uninstaller.exe "" $INSTDIR\uninstaller.exe 0
SectionEnd

Section "Uninstall"
Delete "$SMPROGRAMS\QuartoWriter\Run QuartoWriter app.lnk"
Delete "$SMPROGRAMS\QuartoWriter\Uninstall QuartoWriter app.lnk"
rmDir "$SMPROGRAMS\QuartoWriter"

Delete $INSTDIR\version.txt
Delete $INSTDIR\warning.txt
Delete $INSTDIR\Source\*.*
RMDir $INSTDIR\Source
Delete $INSTDIR\bin\wx\*.*
RMDir $INSTDIR\bin\wx
Delete $INSTDIR\bin\*.*
RMDir $INSTDIR\bin
Delete $INSTDIR\doc\*.*
RMDir $INSTDIR\doc
Delete $INSTDIR\uninstaller.exe
RMDir $INSTDIR
SectionEnd
