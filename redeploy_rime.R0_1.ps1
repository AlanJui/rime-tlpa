# redeploy_rime.ps1 v0.1
#
# RIME重新部署腳本
Write-Host "正在重新部署RIME..." -ForegroundColor Yellow

# 查找RIME進程並嘗試重啟
$rimeProcess = Get-Process -Name "WeaselServer" -ErrorAction SilentlyContinue
if ($rimeProcess) {
    Write-Host "找到RIME進程，正在重啟..." -ForegroundColor Green
    Stop-Process -Name "WeaselServer" -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
}

# 嘗試啟動RIME部署
$rimePath = "C:\Program Files\Rime\weasel-*\WeaselDeployer.exe"
$deployerPath = Get-ChildItem -Path "C:\Program Files\Rime" -Name "WeaselDeployer.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($deployerPath) {
    $fullPath = "C:\Program Files\Rime\$deployerPath"
    Write-Host "執行RIME部署器: $fullPath" -ForegroundColor Green
    Start-Process -FilePath $fullPath -ArgumentList "/deploy" -Wait
    Write-Host "RIME重新部署完成！" -ForegroundColor Green
} else {
    Write-Host "未找到RIME部署器，請手動重新部署" -ForegroundColor Red
    Write-Host "請在系統托盤右鍵點擊RIME圖標，選擇「重新部署」" -ForegroundColor Yellow
}

Write-Host "按任意鍵繼續..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
