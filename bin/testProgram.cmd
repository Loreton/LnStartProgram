@echo off
    set "workDir=%CD%"
    SET "PROGRAM_TO_START=Unknown"
    :: call "%~dp0\LnStartProgram.cmd" --debug %*
    echo  "calling... %~dp0\LnStartProgram.cmd" %*
    call "%~dp0\LnStartProgram.cmd" %*
    echo "%ERRORLEVEL: %ERRORLEVEL%"
:EOF
    CD /D "%workDir%"
    if not "%ERRORLEVEL%" == "0" pause