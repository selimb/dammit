@echo off
set py26="C:\Python26\python.exe"
echo Getting version...
py26 -c "from dammit.__main__ import __version__; print __version__" > tmp_file
set /p version= < tmp_file
del tmp_file
echo Version = %version%
echo Did you update the version in setup.py and dammit.py?
echo Did you update CHANGES.md?
echo Did you commit your changes?
PAUSE
echo Removing current AHK executable...
REM del bin\activatePID.exe
echo Building AHK...
REM "C:\Program Files (x86)\AutoHotkey\Compiler\Ahk2Exe.exe" /in bin\activatePID.ahk /out bin\activatePID.exe
echo Building egg...
REM py26 setup.py bdist_egg
echo Cleaning...
py26 setup.py clean --all
del dammit.egg-info
rmdir dammit.egg-info

echo.
echo Rolling out
set dest="T:\selimb\dammit"
echo Cleaning eggs in %dest%
del /Q %dest%\*.egg
echo Copying egg to %dest%
copy dist\*.egg %dest%\

echo Release complete...