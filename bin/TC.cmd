@echo off

    SET "PROGRAM_TO_START=TotalCommander"
    :: call "%~dp0\LnStartProgram.cmd" --debug %*
    call "%~dp0\LnStartProgram.cmd" %*
    echo %ERRORLEVEL%
:EOF
if not "%ERRORLEVEL%" == "0" pause