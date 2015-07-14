; Activate window of given PID

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; DetectHiddenWindows, On
#SingleInstance force

key=""
Hotkey, y, Off
Hotkey, n, Off
input_pid = %1% ; First argument
hotkeys = %2% ; Second argument

WinGet, console_pid, PID, A

IfWinNotExist, ahk_pid %input_pid%
{
    MsgBox Could not activate %input_pid% :(
}
WinActivate, ahk_pid %input_pid%
IfEqual hotkeys, True
{
    Hotkey, y, On
    Hotkey, n, On
}
Else
{
    ExitApp
}
return

y::
    Hotkey, y, Off
    ; ControlSend,, y{Enter}, ahk_pid %console_pid% 
    key=y
    Goto MinimizeAndShowConsole
    return

n::
    Hotkey, n, Off
    ; ControlSend,, n{Enter}, ahk_pid %console_pid%
    key=n
    Goto MinimizeAndShowConsole
    return

MinimizeAndShowConsole:
IfWinActive, ahk_pid %input_pid%
{
    WinMinimize
}
WinActivate, ahk_pid %console_pid%
SendInput %key%{Enter}
ExitApp