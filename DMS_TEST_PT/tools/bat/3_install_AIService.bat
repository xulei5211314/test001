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

echo "��װAIService��ʼ+++++++"
adb install -r AIService.apk
echo "����AIService��װ+++++++"
ping -n 5 127.0.0.1>nul

echo "����AIService-APK+++++++"
adb shell am start -n com.incall.apps.aiservice/.ui.activity.LauncherActivity


pause