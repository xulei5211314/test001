::�ű��Զ�ִ�б�ש����J2
@echo off
::adb kill-server
@adb devices | findstr "\<device\>"
IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb δ������������"
pause
exit
:FINISH
echo "adb ��������"
echo "���복��"
adb root
adb remount
adb shell tail -f /sdcard/hobot/diag/auto_diag.log

pause


