@echo off
    set "workDir=%CD%"
    SET "PROGRAM_TO_START=TotalCommander"
    :: call "%~dp0\LnStartProgram.cmd" --debug %*
    call "%~dp0\LnStartProgram.cmd" %*
    echo "%ERRORLEVEL: %ERRORLEVEL%"
:EOF
    CD /D "%workDir%"
    if not "%ERRORLEVEL%" == "0" pause