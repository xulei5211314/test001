::�ű��Զ��滻hobotdmsapp

@echo off & color 0e & setlocal enabledelayedexpansion 

@adb devices | findstr "\<device\>"
IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb δ������������"
pause
exit
:FINISH
echo "adb ��������"

set sysMng=dms-sysMng-workflow
adb shell  hbipc-utils run \"ps\" --bifsd>ps.txt 
    for /f "delims=" %%a in (ps.txt) do ( 
      for /f "delims=:" %%i in ('call echo %%a^|find /i "dms-sysMng-workflow"') do (
		set result=%%a
		echo %%a
        )
    ) 
	del /s /q ps.txt
echo %result%| findstr %sysMng% >nul && (
    echo "HBIPCͨ������"

) || (
    echo "HBIPCͨ���쳣����������"
	pause
	exit
)

echo "J2 LOG��־���"
adb shell hbipc-utils run \"cd /userdata && mkdir -p AI_log && rm -rf /userdata/AI_log/* && cd /userdata/log && cp -r * ../AI_log && cd /userdata && tar czvf /userdata/log.tar.gz AI_log/ \"  --bifsd

echo "J2��־Copy������"
adb shell hbipc-utils get /sdcard/log.tar.gz /userdata/log.tar.gz --bifsd


echo "ɾ��J2����ʱĿ¼"
adb shell hbipc-utils run \"cd /userdata && rm -rf log.tar.gz && rm -rf AI_log/* \" --bifsd"


echo "J2 ��־������PC"
adb pull /sdcard/log.tar.gz .

ping -n 1 127.0.0.1>nul

