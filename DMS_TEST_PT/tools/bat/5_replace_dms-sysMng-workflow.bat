::脚本自动替换 dms-sysMng-workflow

@echo off
setlocal ENABLEDELAYEDEXPANSION
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

::需要替换的文件名
SET SourceFile=dms-sysMng-workflow

::需要的目标路径+文件名
SET J2Path=/app/output_linux_J2/bin/dms-sysMng-workflow

SET APData=/data
SET err=error
if exist %SourceFile% (
	echo %SourceFile%  文件存在!
) else (
    echo %SourceFile%  文件不存在!
	pause
	exit
)

echo "copy到AP Data分区"
adb push %SourceFile%  %APData%
adb shell sync
ping -n 1 127.0.0.1>nul
	
echo "J2的APP分区设为读写"
adb shell  hbipc-utils run \"mount -o rw,remount /app \" --bifsd
ping -n 2 127.0.0.1>nul

echo "替换dms-sysMng-workflow"
for /F %%j in ('adb shell hbipc-utils put %APData%/%SourceFile%  %J2Path% --bifsd') do ( set ret=%%j)
echo ret=%ret%

echo %ret%| findstr %err% >nul && (
    echo "替换失败"
) || (
    echo "替换成功"
	adb shell  hbipc-utils run \"chmod a+x %J2Path% \" --bifsd
	certutil -hashfile %SourceFile% MD5
	echo "J2侧hobotdms_app文件MD5"
	adb shell  hbipc-utils run \"md5sum %J2_PATH%/%SourceFile% \" --bifsd 
)
ping -n 1 127.0.0.1>nul

echo "sync"
adb shell  hbipc-utils run \"sync \" --bifsd

ping -n 1 127.0.0.1>nul

echo "J2的APP分区设为只读"
adb shell  hbipc-utils run \"mount -o ro,remount /app \" --bifsd

ping -n 2 127.0.0.1>nul

pause