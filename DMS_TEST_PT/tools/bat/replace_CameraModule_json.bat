@echo off
setlocal ENABLEDELAYEDEXPANSION

@adb devices | findstr "\<device\>"
IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb not connect"
pause
exit
:FINISH
echo "adb exist"

echo adb root
adb root
@echo on
dir
@echo off
cd tools\resource\json
@echo on
dir
@echo off
SET SourceFile=CameraModule.json
SET J2Path= /app/output_linux_J2/etc/CameraModule.json
SET APData=/data
SET err=error

if exist %SourceFile% (
	echo %SourceFile% exist
) else (
    echo %SourceFile% not exist
	pause
	exit
)

echo "push %SourceFile%  %APData%"
adb push %SourceFile%  %APData%
adb shell sync
ping -n 1 127.0.0.1>nul
	
echo " run \"mount -o rw,remount /app \"
adb shell  hbipc-utils run \"mount -o rw,remount /app \" --bifsd
ping -n 2 127.0.0.1>nul

echo "put %APData%/%SourceFile%  %J2Path%"
adb shell hbipc-utils put %APData%/%SourceFile%  %J2Path% --bifsd

for /F %%i in ('adb shell hbipc-utils put %APData%/%SourceFile%  %J2Path% --bifsd') do ( set result=%%i)
echo result=%result%
echo %result%| findstr %err% >nul && (
    echo "�滻ʧ��"
) || (
    echo "�滻�ɹ�"
	adb shell  hbipc-utils run \"chmod a+x %J2Path% \" --bifsd
	certutil -hashfile %SourceFile% MD5
	echo "J2��CameraModule.json�ļ�MD5"
	adb shell  hbipc-utils run \"md5sum %J2Path% \" --bifsd 
)

ping -n 1 127.0.0.1>nul

echo "sync"
adb shell  hbipc-utils run \"sync \" --bifsd

ping -n 1 127.0.0.1>nul

adb shell  hbipc-utils run \"mount -o ro,remount /app \" --bifsd
cd ..\..\..