@echo off

rem ###################################################
rem __author__  : 'Loreto Notarantonio'
rem __version__ : '26-10-2017 08.44.44'
rem
rem mi aspetto le seguenti variabili:
rem     PROGRAM_TO_START
rem ed assumiamo che questo script si trovi dentro:
rem     <any_path>\LnStart\LnStartProgram\LnStartProgram.cmd
rem
rem ###################################################

goto :Process

rem ####################################################
rem # :CalculateRootDir
rem ####################################################
:CalculateRootDir

    chdir   /D "%~dp0..\..\"                    &:: e spostiamoci sulla presunta RootDIR
    set     "Ln_Drive=%~d0"
    set     "Ln_RootDir=%CD%"                   &:: impostiamo la ROOT dir
    set     "Ln_StartDir=%Ln_RootDir%\LnStart"


    @echo.
    @echo "Ln_Drive      : %Ln_Drive%"
    @echo "Ln_RootDir    : %Ln_RootDir%"
    :: @echo "Ln_StartDir   : %Ln_StartDir%"
    @echo.

    exit /b


rem ####################################################
rem # :process
rem ###################################################
:Process
    set "Ln_myENV=DEVEL"
    set "Ln_myENV=PROD"

    call :CalculateRootDir
    SET "Ln_PythonDir=%Ln_RootDir%\LnFree\Pgm\WinPython-64bit-3.5.3.1Qt5\python-3.5.3.amd64"
    SET "Ln_PythonExe=%Ln_PythonDir%\python.exe"

    if "%Ln_myENV%" == "PROD" (
        rem -----  StartDir ----
        SET "MainProgram=%Ln_RootDir%\LnStart\StartProgram\LnStartProgram_20171025.zip"
        SET "CONFIG_FILE=%Ln_RootDir%\LnStart\StartProgram\LnStartProgram.ini"
        rem -----  StartDir ----
    ) else (
        rem -----  GIT-REPO ----
        SET "CONFIG_FILE=%Ln_RootDir%\GIT-REPO\Python3\LnStartProgram\conf\LnStartProgram_2.ini"
        SET "MainProgram=%Ln_RootDir%\GIT-REPO\Python3\LnStartProgram\bin\LnStartProgram_20171025.zip"
        SET "MainProgram=%Ln_RootDir%\GIT-REPO\Python3\LnStartProgram\__main__.py"
        rem -----  GIT-REPO ----
    )


    if "%PROGRAM_TO_START%" == "" set "PROGRAM_TO_START=UNKNOWN"
    rem il caller va messo tra ' altrimenti il \ del path dà errore
    set "CMD=%Ln_PythonExe% %MainProgram% --rootDir='%Ln_RootDir%' --program %PROGRAM_TO_START%  --config-file %CONFIG_FILE% --subst=y:"

    echo.
    echo %CMD% %*
    echo.
    %CMD% %*

:Esci