@echo off
echo Automatic run as admin...
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit

rem Set environment variable
set CURRENT_PATH=%~dp0
setx CURRENT_PATH "%CURRENT_PATH%" /M
