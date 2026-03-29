# redeploy_rime.ps1 v0.2
# RIME 重新部署腳本
#
# 說明：
#   WeaselDeployer.exe 在兩種情況下會自動開啟【輸入法設定】視窗：
#   (1) 未傳入 /deploy 參數
#   (2) 工作目錄中找不到 default.custom.yaml（即非 Rime 使用者設定目錄）
#   因此，執行時必須：指定 /deploy 參數，並將工作目錄切換至 Rime 使用者設定目錄。

Write-Host "正在重新部署 RIME..." -ForegroundColor Yellow

# 1. 停止服務
Stop-Process -Name "WeaselServer" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# 2. 定位路徑
#    $env:APPDATA 可自動對應目前登入使用者的 AppData\Roaming，不需寫死使用者帳號
$rimeRoot = "C:\Program Files\Rime"
$userDir = "$env:APPDATA\Rime"

$versionDir = Get-ChildItem -Path $rimeRoot -Directory |
Where-Object { $_.Name -like "weasel-*" } |
Sort-Object LastWriteTime -Descending |
Select-Object -First 1

if (-not $versionDir) {
    Write-Host "找不到 RIME 安裝目錄！" -ForegroundColor Red
    exit 1
}

$deployerPath = Join-Path $versionDir.FullName "WeaselDeployer.exe"
$serverPath = Join-Path $versionDir.FullName "WeaselServer.exe"

if (-not (Test-Path $deployerPath)) {
    Write-Host "找不到 WeaselDeployer.exe！" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $userDir)) {
    Write-Host "找不到 Rime 使用者設定目錄：$userDir" -ForegroundColor Red
    exit 1
}

Write-Host "部署器：$deployerPath" -ForegroundColor Green
Write-Host "用戶目錄：$userDir" -ForegroundColor Cyan

# 3. 複製設定檔至 Rime 使用者設定目錄
$sourceDir = $PSScriptRoot
$files = @(
    # 輸入方案：拼音
    "phing_im_tlpa.schema.yaml",
    "phing_im_bp.schema.yaml",
    "phing_im_bpm2.schema.yaml",
    # 輸入方案：注音
    "zu_im_tlpa.schema.yaml",
    "zu_im_bpm2.schema.yaml",
    # 輸入方案：反切
    "huan_ciat_tps.schema.yaml",
    "huan_ciat_tlpa.schema.yaml",
    # 候選字清單
    "hau_suan_tuann_bp.yaml",
    "hau_suan_tuann_bpm2.yaml",
    "hau_suan_tuann_tlpa.yaml",
    "hau_suan_tuann_tlpa_and_tps.yaml",
    "hau_suan_tuann_tps.yaml",
    # 詞典
    "ji_khoo_tl.dict.yaml",
    "ji_khoo_bpm2.dict.yaml",
    # 鍵盤映射
    "keymap_piau_tian.yaml",
    # Lua 腳本
    "rime.lua",
    "lua\tlpa_converter.lua"
)

foreach ($file in $files) {
    $src = Join-Path $sourceDir $file
    $dst = Join-Path $userDir $file
    $dstFolder = Split-Path $dst -Parent
    if (-not (Test-Path $dstFolder)) {
        New-Item -ItemType Directory -Path $dstFolder | Out-Null
    }
    if (Test-Path $src) {
        Copy-Item -Path $src -Destination $dst -Force
        Write-Host "已複製：$file" -ForegroundColor Cyan
    }
    else {
        Write-Host "找不到來源檔：$file" -ForegroundColor Red
    }
}

# 4. 切換工作目錄至 Rime 使用者設定目錄，再執行部署
#    WeaselDeployer.exe 會檢查 Shell 本身的工作目錄是否含 default.custom.yaml，
#    必須在 Shell 層級先 cd，而非僅透過 Start-Process -WorkingDirectory 指定。
$originalDir = Get-Location
Set-Location $userDir

& $deployerPath /deploy

Set-Location $originalDir

Write-Host "重新部署完成！" -ForegroundColor Green

# 5. 重啟服務
if (Test-Path $serverPath) {
    Write-Host "正在重啟小狼毫服務（WeaselServer）..." -ForegroundColor Yellow
    Start-Process -FilePath $serverPath
}

# Write-Host "完成！按任意鍵結束..." -ForegroundColor Cyan
# $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host "小狼毫服務重啟已完成！" -ForegroundColor Green