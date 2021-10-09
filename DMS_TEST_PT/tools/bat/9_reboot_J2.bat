::重启J2
@echo off
adb kill-server
@adb devices | findstr "\<device\>"
IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb 未连接请检查线束"
pause
exit
:FINISH
echo "adb 连接正常"
echo adb root
adb root

echo "重启J2"
adb shell  hbipc-utils run \"i2cset -y -f 2 0x3a 0x08 0x0\" --bifsd

