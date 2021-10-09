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

echo "进入拨号界面"
adb shell  "am start -n com.wt.emode/.MainActivity" 

