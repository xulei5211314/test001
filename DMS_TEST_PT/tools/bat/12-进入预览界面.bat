@echo off
platform-tools\adb kill-server
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
platform-tools\adb root

echo "����Ԥ������"
platform-tools\adb shell  "am start -n  com.incall.apps.aiservice/.ui.activity.LauncherActivity" 

