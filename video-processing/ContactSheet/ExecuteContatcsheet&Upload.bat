
CHCP 936 > nul
@ECHO OFF
TITLE ɫ�����ɺ�_�ϴ�
SET "dateA=%date:~5,2%%date:~8,2%"

SET "folderA="\\192.168.1.7\z\SNJYW\Comp\image\%dateA%""
REM �������ϴ�Ŀ���ļ���·�� %dateA%����ǰ����

ECHO ��ǰ����:	%dateA%
ECHO �ϴ�Ŀ���ļ���:	%folderA%
START /WAIT POWERSHELL -command "& '"%~dp0excuteContactSheet.bat"'"
XCOPY /Y /D /I "%~dp0ContactSheet*.png" %folderA%
REM PAUSE