@ECHO OFF 
SET "el=None"
SET "SCRIPTS="\\SERVER\scripts\comp\ae""
SETLOCAL enabledelayedexpansion

call :linkdir "C:\Program Files\Adobe\Adobe After Effects CC 2017\Support Files\Scripts"
call :linkdir "C:\Program Files\Adobe\Adobe After Effects CC 2016\Support Files\Scripts"
call :linkdir "C:\Program Files\Adobe\Adobe After Effects CC 2015\Support Files\Scripts"
call :linkdir "C:\Program Files\Adobe\Adobe After Effects CC\Support Files\Scripts"
call :linkdir "C:\Program Files\Adobe\Adobe After Effects CS6\Support Files\Scripts"
call :linkdir "C:\Program Files\Adobe\Adobe After Effects CS5\Support Files\Scripts"
call :linkdir "C:\Program Files\Adobe\Adobe After Effects CS4\Support Files\Scripts"
call :linkdir "C:\Program Files\Adobe\Adobe After Effects CS3\Support Files\Scripts"
call :linkdir "C:\Program Files\Adobe\Adobe After Effects CS2\Support Files\Scripts"
call :linkdir "C:\Program Files\Adobe\Adobe After Effects CS\Support Files\Scripts"

IF %el%==None (
    ECHO û�ҵ�AE��װ�ļ���
)
IF %el%==1 (
    ECHO ���ù���ԱȨ������
)
IF %el%==ignore (
    ECHO �ļ����Ѵ���, ��Ҫ�������ֶ�ɾ��
)
IF %el%==0 (
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
    SET "el=!ERRORLEVEL!"
)
GOTO :EOF