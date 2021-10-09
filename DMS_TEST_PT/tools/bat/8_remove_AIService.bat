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

echo "移除系统AIService"
adb shell mv /system/app/AIService/AIService.apk /system/app/AIService/AIService.apk.b
adb shell rm -r /data/app/com.incall.apps.aiservice*



pause