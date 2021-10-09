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
adb root
adb remount
adb shell  hbipc-utils run \"mount -o rw,remount /\" --bifsd
ping -n 2 127.0.0.1>nul
echo "开始对spi_dev.json更改文件名"
adb shell  hbipc-utils run \"mv /etc/spi_dev.json /etc/spi_dev.jsonb\" --bifsd
echo "spi_dev.json更改为spi_dev.jsonb"
ping -n 2 127.0.0.1>nul
#adb shell  hbipc-utils run \"/app/output_linux_J2/bin/power_off.sh\" --bifsd
pause


