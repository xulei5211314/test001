::�ű��Զ��滻 �����ļ�

@echo off
setlocal ENABLEDELAYEDEXPANSION
::platform-tools\adb kill-server

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
platform-tools\adb root

::��Ҫ�滻���ļ���
::SET SourceFile=dms-sysMng-workflow

::��Ҫ��Ŀ��·��+�ļ���
::SET J2Path=/app/output_linux_J2/bin/dms-sysMng-workflow

SET APData=/data

SET /p SourceFile=�滻�ļ���(Ĭ�ϴ��복��/dataĿ¼):
SET /p J2_PATH=���滻��J2·��(eg��/app/output_linux_J2/etc):
SET err=error
if exist %SourceFile% (
	echo %SourceFile%  �ļ�����!
) else (
    echo %SourceFile%  �ļ�������!
	pause
	exit
)

echo APȫ·����%APData%/%SourceFile%
echo J2ȫ·����%J2_PATH%/%SourceFile%

echo "copy��AP Data����"
platform-tools\adb push %SourceFile%  %APData%
platform-tools\adb shell sync
ping -n 1 127.0.0.1>nul
	
echo "J2��APP������Ϊ��д"
platform-tools\adb shell  hbipc-utils run \"mount -o rw,remount /app \" --bifsd
ping -n 2 127.0.0.1>nul

echo "�滻J2�ļ�"
for /f %%i in ('platform-tools\adb shell hbipc-utils put %APData%/%SourceFile%  %J2_PATH%/%SourceFile% --bifsd') do ( set result=%%i)
echo result1=%result%
echo %result1% | findstr %err% >nul && (
    echo "�滻ʧ��"
) || (
    echo "�滻�ɹ�"
	echo "�����ļ�MD5"
	certutil -hashfile %SourceFile% MD5
	echo "J2�ļ�MD5"
	platform-tools\adb shell  hbipc-utils run \"md5sum %J2_PATH%/%SourceFile% \" --bifsd 
)
ping -n 1 127.0.0.1>nul

echo "sync"
platform-tools\adb shell  hbipc-utils run \"sync \" --bifsd



ping -n 1 127.0.0.1>nul

echo "J2��APP������Ϊֻ��"
platform-tools\adb shell  hbipc-utils run \"mount -o ro,remount /app \" --bifsd

ping -n 2 127.0.0.1>nul

pause