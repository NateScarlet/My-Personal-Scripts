@ECHO OFF 

SET "el=None"
SET "SCRIPTS="\\SERVER\scripts\comp\ae""
SET "SCRIPT_UI="\\SERVER\scripts\comp\ScriptUI.jsx""
SET "STARTUP="\\SERVER\scripts\comp\Startup.jsx""
SET "SHUTDOWN="\\SERVER\scripts\comp\Shutdown.jsx""

SETLOCAL enabledelayedexpansion

call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CC 2017\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CC 2016\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CC 2015\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CC 2014\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CC\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CS6\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CS5\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CS4\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CS3\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CS2\Support Files\Scripts"
call :linkdir "%ProgramFiles%\Adobe\Adobe After Effects CS\Support Files\Scripts"
call :linkdir "D:\Program Files\Adobe\Adobe After Effects CS6\Support Files\Scripts"

ECHO.
IF %el%==None (
    ECHO û�ҵ�AE��װ�ļ���
) ELSE  IF %el%==1 (
    ECHO ���ù���ԱȨ������
) ELSE IF %el%==ignore (
    ECHO �ļ����Ѵ���, ��Ҫ�������ֶ�ɾ��
) ELSE IF %el%==0 (
    ECHO �ѳɹ���װ
    ECHO ��AE�˵� "�ļ�" -^> "�ű�"�¿����ҵ��������ϵĽű�
)
PAUSE

:linkdir
IF EXIST "%~1" (
    CD /D "%~1"
    IF EXIST comp (
        SET "el=ignore"
        GOTO :EOF 
    )
    MKLINK /D "comp" %SCRIPTS%
    MKLINK "ScriptUI Panels\������.jsx" %SCRIPT_UI%
    MKLINK "Startup\custom_startup.jsx" %STARTUP%
    MKLINK "Shutdown\custom_shutdown.jsx" %SHUTDOWN%
    SET "el=!ERRORLEVEL!"
)
GOTO :EOF