@echo off
setlocal ENABLEDELAYEDEXPANSION

::adb kill-server

@adb devices | findstr "\<device\>"
IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb not connect!"
pause
exit
:FINISH
echo "adb ok"

echo adb root
adb root

cd tool\resource\json
SET SourceFile=global.json
SET J2Path= /app/output_linux_J2/etc/global.json
SET APData=/data
SET err=error
if exist %SourceFile% (
	echo %SourceFile%  exist
) else (
    echo %SourceFile% not exist!
	pause
	exit
)

echo "copy to AP Data"
adb push %SourceFile%  %APData%
adb shell sync
ping -n 1 127.0.0.1>nul
adb shell  hbipc-utils run \"mount -o rw,remount /app \" --bifsd
ping -n 2 127.0.0.1>nul

echo "replace global.json"
adb shell hbipc-utils put %APData%/%SourceFile%  %J2Path% --bifsd

for /F %%i in ('adb shell hbipc-utils put %APData%/%SourceFile%  %J2Path% --bifsd') do ( set result=%%i)
echo result=%result%
echo %result%| findstr %err% >nul && (
    echo "replace fail"
) || (
    echo "replace success"
	adb shell  hbipc-utils run \"chmod a+x %J2Path% \" --bifsd
	certutil -hashfile %SourceFile% MD5
	echo "MD5 J2 global.json"
	adb shell  hbipc-utils run \"md5sum %J2Path% \" --bifsd 
)

ping -n 1 127.0.0.1>nul

echo "sync"
adb shell  hbipc-utils run \"sync \" --bifsd

ping -n 1 127.0.0.1>nul

echo "config to read only"
adb shell  hbipc-utils run \"mount -o ro,remount /app \" --bifsd
cd ..\..\..
