@echo off
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"

regsvr32 /s "UnityCaptureFilter32bit.dll" "/i:UnityCaptureName=VirtualCamera"
regsvr32 /s "UnityCaptureFilter64bit.dll" "/i:UnityCaptureName=VirtualCamera"
