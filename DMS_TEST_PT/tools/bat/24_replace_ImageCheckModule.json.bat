::�ű��Զ��滻hobotdmsapp

@echo off
setlocal ENABLEDELAYEDEXPANSION

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

echo adb root
adb root

cd tool\resource\json
::��Ҫ�滻���ļ���
SET SourceFile=ImageCheckModule.json

::��Ҫ��Ŀ��·��+�ļ���
SET J2Path= /app/output_linux_J2/etc/ImageCheckModule.json
SET APData=/data

SET err=error

if exist %SourceFile% (
	echo %SourceFile%  �ļ�����!
) else (
    echo %SourceFile%  �ļ�������!
	pause
	exit
)

echo "copy��AP Data����"
adb push %SourceFile%  %APData%
adb shell sync
ping -n 1 127.0.0.1>nul
	
echo "J2��APP������Ϊ��д"
adb shell  hbipc-utils run \"mount -o rw,remount /app \" --bifsd
ping -n 2 127.0.0.1>nul

echo "�滻ImageCheckModule.json"
adb shell hbipc-utils put %APData%/%SourceFile%  %J2Path% --bifsd

for /F %%i in ('adb shell hbipc-utils put %APData%/%SourceFile%  %J2Path% --bifsd') do ( set result=%%i)
echo result=%result%
echo %result%| findstr %err% >nul && (
    echo "�滻ʧ��"
) || (
    echo "�滻�ɹ�"
	adb shell  hbipc-utils run \"chmod a+x %J2Path% \" --bifsd
	certutil -hashfile %SourceFile% MD5
	echo "J2��ImageCheckModule.json�ļ�MD5"
	adb shell  hbipc-utils run \"md5sum %J2Path% \" --bifsd 
)

ping -n 1 127.0.0.1>nul

echo "sync"
adb shell  hbipc-utils run \"sync \" --bifsd

ping -n 1 127.0.0.1>nul

echo "J2��APP������Ϊֻ��"
adb shell  hbipc-utils run \"mount -o ro,remount /app \" --bifsd
cd ..\..\..
