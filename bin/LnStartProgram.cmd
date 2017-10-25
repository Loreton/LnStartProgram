@echo off

rem ###################################################
rem __author__  : 'Loreto Notarantonio'
rem __version__ : '25-10-2017 10.54.47'
rem
rem mi aspetto le seguenti variabili:
rem     Ln.RootDir
rem     Ln.StartDir
rem     PROGRAM_TO_START
rem
rem ###################################################

goto :Process

rem ####################################################
rem # :CalculateRootDir
rem ####################################################
:CalculateRootDir
    if not exist "%Ln.RootDir%" (
        echo.
        chdir /D  "%~dp0..\..\"              &:: e spostiamoci sulla presunta RootDIR
        set "Ln.Drive=%~d0"
        set "Ln.RootDir=%CD%"                   &:: impostiamo la ROOT dir
        set "Ln.StartDir=%Ln.RootDir%LnStart"
    )

    @echo "Ln.Drive      : %Ln.Drive%"
    @echo "Ln.RootDir    : %Ln.RootDir%"
    @echo "Ln.StartDir   : %Ln.StartDir%"

    exit /b


rem ####################################################
rem # :process
rem ###################################################
:Process
    call :CalculateRootDir
    SET "Ln.PythonDir=%Ln.RootDir%\LnFree\Pgm\WinPython-64bit-3.5.3.1Qt5\python-3.5.3.amd64"
    SET "Ln.PythonExe=%Ln.PythonDir%\python.exe"

    SET "MainProgram=%Ln.RootDir%\GIT-REPO\Python3\LnStartProgram\__main__.py"
    SET "MainProgram=%Ln.StartDir%\LnStartProgram\LnStartProgram_20171025.zip"

    rem il caller va messo tra ' altrimenti il \ del path dà errore
    set "CMD=%Ln.PythonExe% %MainProgram% --rootDir='%Ln.RootDir%' --program %PROGRAM_TO_START% --subst=y:"

    echo %CMD% %*
    %CMD% %*

:Esci