rd /s /q build
rd /s /q dist
C:\Python27\python.exe setup.py py2exe --includes sip
"C:\Program Files (x86)\NSIS\Bin\makensis.exe" /V4 batchrename.nsi
dist\batchrename.exe
