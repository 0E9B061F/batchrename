outFile "s25-batch_rename-setup.exe"

# this will set the default installation dir to the desktop
# $DESKTOP points to the desktop of the current user, regardless of user
installDir "$PROGRAMFILES\studio25\Batch Rename"

section
  # sets the installation path
  # $INSTDIR is defined by the installdir command, so you only should use $INSTDIR
  setOutPath $INSTDIR

  # This will be the file that will be included in the installer, this file has to exist :)
  file dist\*
  file logo.png
  file xquit.png
  file icon16.png

sectionEnd
