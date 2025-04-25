reg add "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-TCP" /v UserAuthentication /t REG_DWORD /d "0" /f

set rule group="remote desktop" new enable=Yes

netsh firewall set service type = remotedesktop mode = enable

netsh advfirewall firewall set rule group="remote desktop" new enable=Yes

netsh firewall set service type = remotedesktop mode = enable


REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f

netsh advfirewall firewall add rule name="Open Remote Desktop" protocol=TCP dir=in localport=3389 action=allow