@echo off
platform-tools\adb kill-server
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
platform-tools\adb root

echo "进入预览界面"
platform-tools\adb shell  "am start -n  com.incall.apps.aiservice/.ui.activity.LauncherActivity" 

