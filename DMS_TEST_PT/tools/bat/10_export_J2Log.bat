::脚本自动替换hobotdmsapp

@echo off & color 0e & setlocal enabledelayedexpansion 

@adb devices | findstr "\<device\>"
IF ERRORLEVEL 1 goto NOCONNECTED
goto FINISH

:NOCONNECTED
echo "adb 未连接请检查线束"
pause
exit
:FINISH
echo "adb 连接正常"

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
    echo "HBIPC通信正常"

) || (
    echo "HBIPC通信异常！！！！！"
	pause
	exit
)

echo "J2 LOG日志打包"
adb shell hbipc-utils run \"cd /userdata && mkdir -p AI_log && rm -rf /userdata/AI_log/* && cd /userdata/log && cp -r * ../AI_log && cd /userdata && tar czvf /userdata/log.tar.gz AI_log/ \"  --bifsd

echo "J2日志Copy到本地"
adb shell hbipc-utils get /sdcard/log.tar.gz /userdata/log.tar.gz --bifsd


echo "删除J2侧临时目录"
adb shell hbipc-utils run \"cd /userdata && rm -rf log.tar.gz && rm -rf AI_log/* \" --bifsd"


echo "J2 日志导出到PC"
adb pull /sdcard/log.tar.gz .

ping -n 1 127.0.0.1>nul

