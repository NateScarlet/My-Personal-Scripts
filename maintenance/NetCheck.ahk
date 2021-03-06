#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.
;~ if not A_IsAdmin ;确保管理员权限
;~ {
   ;~ Run *RunAs "%A_ScriptFullPath%"  ; 需要 v1.0.92.01+
   ;~ ExitApp
;~ }
CoordMode, Mouse, Client



ahkcs := "http://www.steampowerd.com"
Menu, Tray, Icon, imageres.dll, 85

Loop
{
        ;~ 图标变化
        If (W_InternetCheckConnection(ahkcs))
        {
                NetStatus := "网络正常"
                Menu, Tray, Icon, imageres.dll, 21
        }
        else
        {
                NetStatus := "网络中断"
                Menu, Tray, Icon, imageres.dll, 85
        }
        ;~ 气泡提示
        If (NetStatus != LastNetStatus)
        {
                TrayTip, , %NetStatus%
                LastNetStatus := NetStatus
        }
        Sleep, 1000
}
;        判断是否可以与某个 URL 建立连接

W_InternetCheckConnection(lpszUrl)
{
        FLAG_ICC_FORCE_CONNECTION := 0x1
        dwReserved := 0x0
        return, DllCall("Wininet.dll\InternetCheckConnection", "Ptr", &lpszUrl, "UInt", FLAG_ICC_FORCE_CONNECTION, "UInt", dwReserved, "Int")
}