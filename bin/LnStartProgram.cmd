@echo off
    @setlocal

    echo "%CD%"
    CD /D "%~dp0"
    echo "%CD%"
    goto :REPO_DIR

:REPO_DIR
    rem -----  RepoDir ----
    SET "Ln_PythonExe=Y:\LnFree\Pgm\WinPython-64bit-3.5.3.1Qt5\python-3.5.3.amd64\python.exe"
    SET "MainProgram=..\__main__.py"
    SET "CONFIG_FILE=..\conf\LnStartProgram.ini"
    rem -----  RepoDir ----
    goto :Process

:START_DIR
    rem -----  StartDir ----
    SET "Ln_PythonExe=..\..\LnFree\Pgm\WinPython-64bit-3.5.3.1Qt5\python-3.5.3.amd64\python.exe"
    SET "MainProgram=.\LnStartProgram_20171025.zip"
    SET "CONFIG_FILE=.\LnStartProgram.ini"
    rem -----  StartDir ----
    goto :Process


:Process
    set "CMD=%Ln_PythonExe% %MainProgram% %1 --config-file %CONFIG_FILE% --subst=y:" %2 %3 %4 %5 %6 %7 %8 %9
    echo.
    echo %CMD%
    echo.
    %CMD%
    set "rCODE=%ERRORLEVEL%"

:EOF
    echo "rCODE: %rCODE%"
    if not "%rCODE%" == "0" pause
    @endlocal


    :: @endlocal
    :: echo "%CD%"