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

echo "���빤�̽���"
adb shell  "am start -n  com.incall.apps.aiservice/.ui.activity.FactoryTestActivity" 

