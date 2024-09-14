name mdWriter
OutFile "mdWriterInstaller.exe"
InstallDir "C:\Program files\openAccessWare\mdWriter"
#LicenseText "Warnings:"
caption "Installer for mdWriter"
CompletedText "Installation of mdWriter is completed."
LicenseData ..\PackageFiles\install\warning.txt
UninstallCaption "Uninstall the mdWriter app."
UninstallText "Hopefully we will completely remove everythiung created when you installed mdWriter."

Page license
Page directory
Page instfiles
 UninstPage uninstConfirm
 UninstPage instfiles

Section

MessageBox MB_OK "You are about to install mdWriter. $\nBefore you use mdWriter though, you will need an installation of Pandoc. $\nWriteR will open without this tool, but you get minimal benefit from its use until you do install Pandoc. $\n$\nWriteR is not currently added to the system path."

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
file mdWriter.dist\*.*
file ..\PackageFiles\Python\*.wav
SetOutPath $INSTDIR\bin\wx
file mdWriter.dist\wx\*.*
SetOutPath $INSTDIR\doc
file ..\PackageFiles\documentation\*.*

WriteUninstaller $INSTDIR\uninstaller.exe

CreateDirectory $SMPROGRAMS\mdWriter
CreateShortCut "$SMPROGRAMS\mdWriter\Run mdWriter app.lnk" $INSTDIR\bin\mdWriter.exe "" $INSTDIR\mdWriter\bin\mdWriter.exe 0
CreateShortCut "$SMPROGRAMS\mdWriter\Uninstall mdWriter app.lnk" $INSTDIR\uninstaller.exe "" $INSTDIR\uninstaller.exe 0
SectionEnd

Section "Uninstall"
Delete "$SMPROGRAMS\mdWriter\Run mdWriter app.lnk"
Delete "$SMPROGRAMS\mdWriter\Uninstall mdWriter app.lnk"
rmDir "$SMPROGRAMS\mdWriter"

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
