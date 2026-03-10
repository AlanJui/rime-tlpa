# redeploy_rime.ps1 v0.1.1
# "C:\Program Files\Rime\weasel-0.17.4\WeaselDeployer.exe" /deploy
# RIME 重新部署腳本 (強制指定用戶目錄版)
Write-Host "正在重新部署 RIME..." -ForegroundColor Yellow

# 1. 停止服務
Stop-Process -Name "WeaselServer" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# 2. 定位路徑
$rimeRoot = "C:\Program Files\Rime"
$userDir = "C:\Users\AlanJui\AppData\Roaming\Rime" # 您指定的用戶目錄

# 找出最新的版本目錄
$versionDir = Get-ChildItem -Path $rimeRoot -Directory |
               Where-Object { $_.Name -like "weasel-*" } |
               Sort-Object LastWriteTime -Descending |
               Select-Object -First 1

if ($versionDir) {
    $fullPath = Join-Path $versionDir.FullName "WeaselDeployer.exe"

    if (Test-Path $fullPath) {
        Write-Host "執行部署器：$fullPath" -ForegroundColor Green
        Write-Host "用戶目錄：$userDir" -ForegroundColor Cyan

        # 關鍵繞行邏輯：
        # /deploy 觸發部署
        # /p 指定用戶資料夾位址，防止跳出設定選單
        $deployArgs = "/deploy /p `"$userDir`""

        Start-Process -FilePath $fullPath `
                      -ArgumentList $deployArgs `
                      -WorkingDirectory $versionDir.FullName `
                      -Wait

        Write-Host "重新部署完成！" -ForegroundColor Green
    }
}

# 3. 重啟服務
$serverExe = Join-Path $versionDir.FullName "WeaselServer.exe"
if (Test-Path $serverExe) {
    Start-Process -FilePath $serverExe -WorkingDirectory $versionDir.FullName
}

Write-Host "按任意鍵繼續..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
