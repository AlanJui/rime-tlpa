# RIME-TLPA 台語輸入法部署腳本
# 作者: AI助手
# 日期: 2026-03-08

Write-Host "=== RIME-TLPA 台語輸入法部署腳本 ===" -ForegroundColor Green
Write-Host ""

# 設定變數
$RimeUserDir = "$env:APPDATA\Rime"
$ProjectDir = Get-Location
$BackupDir = "$RimeUserDir\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# 檢查RIME是否安裝
if (-not (Test-Path "C:\Program Files\Rime")) {
    Write-Host "錯誤：未找到RIME安裝，請先安裝小狼毫輸入法" -ForegroundColor Red
    Write-Host "下載網址：https://rime.im/" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ 檢測到RIME已安裝" -ForegroundColor Green

# 創建RIME用戶目錄（如果不存在）
if (-not (Test-Path $RimeUserDir)) {
    New-Item -ItemType Directory -Path $RimeUserDir -Force
    Write-Host "✓ 創建RIME用戶目錄：$RimeUserDir" -ForegroundColor Green
} else {
    Write-Host "✓ RIME用戶目錄已存在：$RimeUserDir" -ForegroundColor Green
}

# 創建備份目錄
Write-Host "正在創建備份..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $BackupDir -Force

# 備份現有配置
if (Test-Path "$RimeUserDir\default.custom.yaml") {
    Copy-Item "$RimeUserDir\default.custom.yaml" "$BackupDir\" -Force
    Write-Host "✓ 已備份 default.custom.yaml" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 開始部署台語輸入法文件 ===" -ForegroundColor Cyan

# 需要複製的文件列表
$FilesToCopy = @(
    # 主要方案文件
    "tlpa_phing_im.schema.yaml",
    "tlpa_hong_im.schema.yaml",
    "tlpa_khau_ik_zu_im.schema.yaml",
    "sgi_zu_im.schema.yaml",
    "sgi_ping_im.schema.yaml",
    "zu_im_2_phing_im.schema.yaml",
    "zu_im_2_hong_im.schema.yaml",
    "bp_phing_im.schema.yaml",
    "bp_hong_im.schema.yaml",

    # 字典文件
    "tl_han_ji_khoo.dict.yaml",
    "tl_ji_khoo.dict.yaml",
    "tl_ji_khoo_ciann_ji.dict.yaml",
    "tl_ji_khoo_II.dict.yaml",
    "tl_ji_khoo_kah_kut_bun.dict.yaml",
    "tl_ji_khoo_kong_un.dict.yaml",
    "tl_ji_khoo_nga_siok_thong.dict.yaml",
    "tl_ji_khoo_peh_ue.dict.yaml",
    "tl_ji_khoo_zu_ting.dict.yaml",
    "zu_im_2.dict.yaml",
    "bp_ji_khoo.dict.yaml",

    # 庫文件
    "tlpa_lib_hau_suan_tuann.yaml",
    "tlpa_lib_hong_im_hau_suan_ji_tuann.yaml",
    "tlpa_lib_zu_im_hau_suan_ji_tuann.yaml",
    "tlpa_kik_kan_sip_goo_im_libs.yaml",
    "zu_im_2_libs.yaml",
    "zu_im_2_hau_suan_zzi_duann.yaml",
    "bp_libs.yaml",
    "bp_libs_hst_phing_im.yaml",
    "bp_libs_hst_zu_im.yaml",
    "bp_libs_R0.yaml",
    "bp_libs_R1.yaml",

    # 其他配置文件
    "rime.lua",
    "keymap_piau_tian.yaml",
    "lib_hau_suan_ji_tuann.yaml",
    "lib_phing_im.yaml",
    "lib_sip_ngoo_im.yaml",
    "lib_zu_im.yaml"
)

# 複製文件
$CopiedCount = 0
$SkippedCount = 0

foreach ($file in $FilesToCopy) {
    if (Test-Path "$ProjectDir\$file") {
        try {
            Copy-Item "$ProjectDir\$file" "$RimeUserDir\" -Force
            Write-Host "✓ 已複製：$file" -ForegroundColor Green
            $CopiedCount++
        } catch {
            Write-Host "✗ 複製失败：$file - $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "⚠ 文件不存在：$file" -ForegroundColor Yellow
        $SkippedCount++
    }
}

# 複製lua目錄
if (Test-Path "$ProjectDir\lua") {
    if (-not (Test-Path "$RimeUserDir\lua")) {
        New-Item -ItemType Directory -Path "$RimeUserDir\lua" -Force
    }
    Copy-Item "$ProjectDir\lua\*" "$RimeUserDir\lua\" -Recurse -Force
    Write-Host "✓ 已複製 lua 目錄" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== 配置輸入法方案 ===" -ForegroundColor Cyan

# 創建或更新 default.custom.yaml
$DefaultCustomContent = @"
customization:
  distribution_code_name: Weasel
  distribution_version: 0.16.0
  generator: "Rime::SwitcherSettings"
  modified_time: "$(Get-Date -Format 'ddd MMM dd HH:mm:ss yyyy')"
  rime_version: 1.11.2

patch:
  "log/level": "info"
  schema_list:
    # 台語拼音輸入法 (TLPA)
    - { schema: tlpa_phing_im }     # 拼音輸入法【台語音標】
    - { schema: tlpa_hong_im }      # 注音輸入法【台語音標】
    - { schema: tlpa_khau_ik_zu_im } # 巧易注音輸入法

    # 極簡注音
    - { schema: sgi_zu_im }         # 極簡注音符號【十五音】

    # 台語注音二式
    - { schema: zu_im_2_phing_im }  # 台語注音二式拼音輸入法
    - { schema: zu_im_2_hong_im }   # 台語注音二式注音輸入法

    # 閩拼方案 (BP)
    - { schema: bp_phing_im }       # 閩拼方案拼音輸入法
    - { schema: bp_hong_im }        # 閩拼方案注音輸入法
"@

# 寫入配置文件
$DefaultCustomContent | Out-File -FilePath "$RimeUserDir\default.custom.yaml" -Encoding UTF8
Write-Host "✓ 已創建 default.custom.yaml 配置文件" -ForegroundColor Green

Write-Host ""
Write-Host "=== 部署統計 ===" -ForegroundColor Cyan
Write-Host "成功複製文件：$CopiedCount 個" -ForegroundColor Green
Write-Host "跳過文件：$SkippedCount 個" -ForegroundColor Yellow
Write-Host "備份目錄：$BackupDir" -ForegroundColor Blue

Write-Host ""
Write-Host "=== 重要提醒 ===" -ForegroundColor Yellow
Write-Host "1. 請重新部署RIME輸入法以使配置生效"
Write-Host "2. 在系統托盤找到RIME圖標，右鍵選擇「重新部署」"
Write-Host "3. 或者按 Ctrl+` 調出輸入法選單，選擇台語輸入法"
Write-Host "4. 如需恢復原配置，請使用備份目錄中的文件"

Write-Host ""
Write-Host "=== 部署完成！===" -ForegroundColor Green
Write-Host "現在您可以使用以下台語輸入法：" -ForegroundColor Cyan
Write-Host "• 台語拼音輸入法 (TLPA)" -ForegroundColor White
Write-Host "• 台語注音輸入法 (方音符號)" -ForegroundColor White
Write-Host "• 極簡注音符號 (十五音)" -ForegroundColor White
Write-Host "• 台語注音二式輸入法" -ForegroundColor White
Write-Host "• 閩拼方案輸入法 (BP)" -ForegroundColor White

Write-Host ""
Read-Host "按任意鍵繼續..."
