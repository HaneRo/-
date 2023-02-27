Function Set-IEProxy {
    param(
        [bool]$Enable = $false,
        [string]$ProxyServer,
        [ValidateRange(1, 65535)]
        [int]$port
    )

    #设置IE代理
    $proxyRegPath = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    $enableProxy = Get-ItemProperty -Path $proxyRegPath -Name ProxyEnable
    if ( -not $Enable) {
        Set-ItemProperty -path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings" -Name "ProxyEnable" -value 0
        Write-Host "IE代理已禁用。"
    }
    else {
        Set-ItemProperty -path $proxyRegPath -Name "ProxyEnable" -value 1
        Set-ItemProperty -path $proxyRegPath -Name "ProxyServer" -value ( $ProxyServer + ":" + $port )
        Write-Host "IE代理已启用"
    }
}

Function sed($Filename, $Oldvalue, $Newvalue) {
    if (Test-Path $Filename) {
        $content = get-content $Filename
        clear-content $Filename
        foreach ($line in $content) {
            $liner = $line.Replace($Oldvalue, $Newvalue)
            Add-content $Filename -Value $liner
        }
    }
}

Function UpdateConfig {
    Copy-Item $Env:USERPROFILE\.config\clash\config.yaml $Env:USERPROFILE\.config\clash\config.yaml.old
    Invoke-WebRequest (Get-Content $Env:ProgramFiles\Clash\sub.txt) -UseBasicParsing -OutFile $Env:USERPROFILE\.config\clash\config.yaml

    sed $Env:USERPROFILE\.config\clash\config.yaml "port: 7890" "mixed-port: 1080"
    sed $Env:USERPROFILE\.config\clash\config.yaml "socks-port: 7891" "secret: zero*9*9"
    sed $Env:USERPROFILE\.config\clash\config.yaml "log-level: info" "log-level: error"
    sed $Env:USERPROFILE\.config\clash\config.yaml "external-controller: :9090" "external-controller: :9999"
}



if (Test-Connection 10.10.10.10 -tcpport 1080) {
    Write-Output "关闭Clash，恢复网络"
    Set-IEProxy -Enable $false
    Get-Process -Name clash | Stop-Process
}
elseif (Test-Connection baidu.com -tcpport 443) {
    Write-Output "更新Clash配置文件"
    Set-IEProxy -Enable $false
    Get-Process -Name clash | Stop-Process
    UpdateConfig
    Start-Process $Env:ProgramFiles\Clash\clash.exe -ArgumentList  '-ext-ui "A:\Program Files\Clash\ui"' -WindowStyle Hidden
    Set-IEProxy  -Enable $true -ProxyServer 127.0.0.1 -port 1080
}else{
    Write-Output "未连接网络，关闭Clash"
    Set-IEProxy -Enable $false
    Get-Process -Name clash | Stop-Process
}
