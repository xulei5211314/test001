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

echo "���벦�Ž���"
adb shell  "am start -n com.wt.emode/.MainActivity" 

