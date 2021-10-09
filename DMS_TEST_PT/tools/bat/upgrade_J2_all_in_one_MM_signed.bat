@echo off
@adb devices | findstr "\<device\>"

IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb disable"
pause
exit
:FINISH
echo "adb connect ok"
echo adb root
adb root
ping -n 2 127.0.0.1>nul
adb shell mkdir -p /sdcard/hobot/upgrade
cd tools\upgrade_package
SET SourceFile=all_in_one_MM_signed.zip

if exist %SourceFile% (
	echo %SourceFile%  file exist!
	adb push all_in_one_MM_signed.zip /sdcard/hobot/upgrade
	adb shell sync
) else (
    echo %SourceFile%  file not find
	pause
)

adb shell am start -n com.incall.apps.aiservice/.ui.activity.FactoryTestActivity
cd ..\..
