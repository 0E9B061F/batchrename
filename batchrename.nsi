name "studio25 Batch Rename"

outFile "s25-batch_rename-setup.exe"

# Base directory to install to
installDir "$PROGRAMFILES\studio25\BatchRename"

# Registry key to check for directory (so if you install again, it will 
# overwrite the old one automatically)
InstallDirRegKey HKLM "Software\NSIS_BatchRename" "Install_Dir"

# Request application privileges for Windows Vista
RequestExecutionLevel admin

# Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles



# The stuff to install
Section "BatchRename (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  file dist\*
  file logo.png
  file xquit.png
  file icon16.png

  FileOpen  $0 $INSTDIR\br.py w
  FileWrite $0 "import os$\r$\n"
  FileWrite $0 "os.chdir('$INSTDIR')$\r$\n"
  FileWrite $0 "import batchrename$\r$\n"
  FileWrite $0 "batchrename.main()$\r$\n"
  FileClose $0
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\s25BatchRename "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\s25BatchRename" "DisplayName" "NSIS BatchRename"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\s25BatchRename" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\s25BatchRename" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\s25BatchRename" "NoRepair" 1
  WriteUninstaller "uninstall.exe"

  # Windows Explorer context menu integration
  WriteRegStr HKCR "Directory\shell\s25BatchRename" "" "Open Batch Renamer ..."
  WriteRegStr HKCR "Directory\shell\s25BatchRename\command" "" "$INSTDIR\br.exe %1"
  
SectionEnd



# Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\Studio25\Batch Rename"
  CreateShortCut "$SMPROGRAMS\Studio25\Batch Rename\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\Studio25\Batch Rename\Batch Rename.lnk" "$INSTDIR\br.exe" "" "$INSTDIR\br.exe" 0
  
SectionEnd



# Uninstaller
Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\s25BatchRename"
  DeleteRegKey HKLM SOFTWARE\s25BatchRename

  # Remove Windows Explorer context menu integration
  DeleteRegKey HKCR "Directory\shell\s25BatchRename"

  ; Remove files and uninstaller
  Delete $INSTDIR\*

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\Studio25\Batch Rename\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\Studio25\Batch Rename"
  RMDir "$INSTDIR"

SectionEnd

