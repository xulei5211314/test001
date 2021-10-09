::脚本自动替换 其它文件

@echo off
setlocal ENABLEDELAYEDEXPANSION
::platform-tools\adb kill-server

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
platform-tools\adb root

::需要替换的文件名
::SET SourceFile=dms-sysMng-workflow

::需要的目标路径+文件名
::SET J2Path=/app/output_linux_J2/bin/dms-sysMng-workflow

SET APData=/data

SET /p SourceFile=替换文件名(默认存入车机/data目录):
SET J2_PATH=/mnt/
SET err=error
if exist %SourceFile% (
	echo %SourceFile%  文件存在!
) else (
    echo %SourceFile%  文件不存在!
	pause
	exit
)

echo AP全路径：%APData%/%SourceFile%
echo J2全路径：%J2_PATH%/%SourceFile%

echo "copy到AP Data分区"
platform-tools\adb push %SourceFile%  %APData%
platform-tools\adb shell sync
ping -n 1 127.0.0.1>nul
	
echo "挂载分区"
platform-tools\adb shell  hbipc-utils run \"mount LABEL="kernelbak" /mnt\" --bifsd
echo "J2的APP分区设为读写"
platform-tools\adb shell  hbipc-utils run \"mount -o rw,remount /\" --bifsd
ping -n 2 127.0.0.1>nul

echo "替换J2文件"
for /f %%i in ('platform-tools\adb shell hbipc-utils put %APData%/%SourceFile%  %J2_PATH%/%SourceFile% --bifsd') do ( set result=%%i)
echo result1=%result%
echo %result1% | findstr %err% >nul && (
    echo "替换失败"
) || (
    echo "替换成功"
	echo "本地文件MD5"
	certutil -hashfile %SourceFile% MD5
	echo "J2文件MD5"
	platform-tools\adb shell  hbipc-utils run \"md5sum %J2_PATH%/%SourceFile% \" --bifsd 
)
ping -n 1 127.0.0.1>nul

echo "sync"
platform-tools\adb shell  hbipc-utils run \"sync \" --bifsd



ping -n 1 127.0.0.1>nul

echo "J2的APP分区设为只读"
platform-tools\adb shell  hbipc-utils run \"mount -o ro,remount /\" --bifsd

ping -n 2 127.0.0.1>nul

pause