echo "in bat"
@echo off
::adb kill-server
@adb devices | findstr "\<device\>"
IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb not connect"
pause
exit
:FINISH
echo "adb exist"
::echo adb root
::adb reboot

echo "start get"
adb shell  hbipc-utils run \"cat /app/output_linux_J2/version\" --bifsd