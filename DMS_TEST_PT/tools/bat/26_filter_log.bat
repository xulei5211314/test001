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
SET /p SourceFile=������˹ؼ���(logcat -v time):
adb root
adb remount
adb shell logcat -v time |findstr %SourceFile%

pause


