::�ű��Զ�ִ�б�ש����J2
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

echo adb remount
adb remount

echo "�Ƴ�ϵͳAIService"
adb shell mv /system/app/AIService/AIService.apk /system/app/AIService/AIService.apk.b
adb shell rm -r /data/app/com.incall.apps.aiservice*



pause