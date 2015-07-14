@echo off
set py26="C:\Python26\python.exe"
echo Getting version...
%py26% -c "from dammit import __version__; print __version__" > tmp_file
set /p package_version= < tmp_file
del tmp_file
%py26% setup.py --version > tmp_file
set /p setup_version= < tmp_file
del tmp_file
if not %setup_version% == %package_version% (
    echo FATAL
    echo Setup.py version %setup_version% != Package version %package_version%
    exit /b 1
)
set version=%setup_version%
echo Version = %version%
echo Did you update CHANGES.md?
echo Did you commit your changes?
PAUSE

echo.
echo Building
echo ========
echo Removing current AHK executable...
del /Q bin\activatePID.exe >NUL
echo Building AHK...
"C:\Program Files (x86)\AutoHotkey\Compiler\Ahk2Exe.exe" /in bin\activatePID.ahk /out bin\activatePID.exe >NUL
echo Building egg...
%py26% setup.py bdist_egg >NUL

echo.
echo Rolling out
echo ===========
set dest=T:\selimb\dammit
echo Cleaning eggs in %dest%
del %dest%\*.egg
echo Copying egg to %dest%
copy dist\*.egg %dest%\ >NUL
echo Echoing version number
echo %version% > %dest%\version.txt
attrib +h +s %dest%\version.txt

echo.
echo Cleaning...
%py26% setup.py clean --all >NUL
del /Q dammit.egg-info >NUL
rmdir /Q dammit.egg-info >NUL
del /Q dist>NUL
rmdir /Q dist>NUL

echo.
echo Release complete.
