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
adb shell  hbipc-utils run \"mount -o rw,remount /\" --bifsd
ping -n 2 127.0.0.1>nul
echo "��ʼ��spi_dev.json�����ļ���"
adb shell  hbipc-utils run \"mv /etc/spi_dev.json /etc/spi_dev.jsonb\" --bifsd
echo "spi_dev.json����Ϊspi_dev.jsonb"
ping -n 2 127.0.0.1>nul
#adb shell  hbipc-utils run \"/app/output_linux_J2/bin/power_off.sh\" --bifsd
pause


