::����J2
@echo off
adb kill-server
@adb devices | findstr "\<device\>"
IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb δ������������"
pause
exit
:FINISH
echo "adb ��������"
echo adb root
adb root

echo "����J2"
adb shell  hbipc-utils run \"i2cset -y -f 2 0x3a 0x08 0x0\" --bifsd

