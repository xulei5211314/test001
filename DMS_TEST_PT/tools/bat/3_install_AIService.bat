::脚本自动执行变砖升级J2
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

echo adb remount
adb remount

echo "安装AIService开始+++++++"
adb install -r AIService.apk
echo "结束AIService安装+++++++"
ping -n 5 127.0.0.1>nul

echo "启动AIService-APK+++++++"
adb shell am start -n com.incall.apps.aiservice/.ui.activity.LauncherActivity


pause