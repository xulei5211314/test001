::脚本自动执行变砖升级J2
@echo off
::adb kill-server
@adb devices | findstr "\<device\>"
IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb 未连接请检查线束"
pause
exit
:FINISH
echo "adb 连接正常"
echo "进入车机"
SET /p SourceFile=输入过滤关键字(logcat -v time):
adb root
adb remount
adb shell logcat -v time |findstr %SourceFile%

pause


