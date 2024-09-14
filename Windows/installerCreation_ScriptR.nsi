name ScriptR
OutFile "ScriptRInstaller.exe"
InstallDir "C:\Program files\openAccessWare\ScriptR"
#LicenseText "Warnings:"
caption "Installer for ScriptR"
CompletedText "Installation of ScriptR is completed."
LicenseData ..\PackageFiles\install\warning.txt
UninstallCaption "Uninstall the ScriptR app."
UninstallText "Hopefully we will completely remove everything created when you installed ScriptR."

Page license
Page directory
Page instfiles
 UninstPage uninstConfirm
 UninstPage instfiles

Section

MessageBox MB_OK "You are about to install ScriptR. $\nBefore you use ScriptR though, you will need an installation of R. $\nScriptR will open without R but you won't get any benefit until you do install R. $\n$\nScriptR is not currently added to the system path."

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
file ScriptR.dist\*.*
file ..\PackageFiles\Python\*.wav
SetOutPath $INSTDIR\bin\wx
file ScriptR.dist\wx\*.*

SetOutPath $INSTDIR\doc
file ..\PackageFiles\documentation\*.*

WriteUninstaller $INSTDIR\uninstaller.exe

CreateDirectory $SMPROGRAMS\ScriptR
CreateShortCut "$SMPROGRAMS\ScriptR\Run ScriptR app.lnk" $INSTDIR\bin\ScriptR.exe "" $INSTDIR\ScriptR\bin\ScriptR.exe 0
CreateShortCut "$SMPROGRAMS\ScriptR\Uninstall ScriptR app.lnk" $INSTDIR\uninstaller.exe "" $INSTDIR\uninstaller.exe 0
SectionEnd

Section "Uninstall"
Delete "$SMPROGRAMS\ScriptR\Run ScriptR app.lnk"
Delete "$SMPROGRAMS\ScriptR\Uninstall ScriptR app.lnk"
rmDir "$SMPROGRAMS\ScriptR"

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
