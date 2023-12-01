@echo off
SETLOCAL

REM Try using Python Launcher first
py update.py 2>nul
IF %ERRORLEVEL% EQU 0 GOTO End

REM If Python Launcher is not available, fall back to 'python'
python update.py 2>nul
IF %ERRORLEVEL% EQU 0 GOTO End

REM If both attempts fail, display an error message
echo Unable to find Python. Please ensure Python is installed and in your PATH.
GOTO End

:End
pause
ENDLOCAL