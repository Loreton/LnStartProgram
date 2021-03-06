@echo off
    @setlocal

    echo "%CD%"
    CD /D "%~dp0"
    set "myDIR=%CD%"
    :: echo "%CD%"
    echo "...%myDIR%"
    goto :REPO_DIR

:REPO_DIR
    rem -----  RepoDir ----
    SET "Ln_PythonExe=Y:\LnFree\Pgm\WinPython-64bit-3.5.3.1Qt5\python-3.5.3.amd64\python.exe"
    SET "ProgramName=__main__.py"
    SET "ProgramName=LnStartProgram_20171107"
    SET "ProgramName=LnStartProgram_2018-01-17"
    SET "ProgramName=LnStartProgram_2018-02-05"

    SET "CONFIG_FILE=%myDIR%\%ProgramName%.ini"
    SET "MainProgram=%myDIR%\%ProgramName%.zip"


    rem -----  RepoDir ----
    goto :Process

:START_DIR
    rem -----  StartDir ----
    SET "Ln_PythonExe=..\..\LnFree\Pgm\WinPython-64bit-3.5.3.1Qt5\python-3.5.3.amd64\python.exe"
    SET "ProgramName=LnStartProgram_20171107"
    SET "ProgramName=LnStartProgram_2018-01-17"
    SET "ProgramName=LnStartProgram_2018-02-05"


    SET "CONFIG_FILE=%myDIR%\%ProgramName%.ini"
    SET "MainProgram=%myDIR%\%ProgramName%.zip"
    rem -----  StartDir ----
    goto :Process


:Process
    set "CMD=%Ln_PythonExe% %MainProgram% %1 --config-file %CONFIG_FILE% --subst=y: --execute" %2 %3 %4 %5 %6 %7 %8 %9
    echo.
    echo %CMD%
    echo.
    %CMD%
    set "rCODE=%ERRORLEVEL%"

:EOF
    echo "rCODE: %rCODE%"
    echo.
    if not "%rCODE%" == "0" pause
    @endlocal


    :: @endlocal
    :: echo "%CD%"