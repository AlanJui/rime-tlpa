# 檢查 DoMiSo_Zu_Im 目錄下的造字檔案
# 作者：AlanJui
# 日期：2025-10-25

param(
    [string]$FontPath = "C:\work\DoMiSo_Zu_Im"
)

Write-Host "=== 檢查 DoMiSo 造字檔案 ===" -ForegroundColor Green
Write-Host "目標目錄：$FontPath" -ForegroundColor Yellow

# 檢查目錄是否存在
if (-not (Test-Path $FontPath)) {
    Write-Host "錯誤：目錄不存在 - $FontPath" -ForegroundColor Red
    exit 1
}

# 尋找造字檔案
$fontFiles = Get-ChildItem $FontPath -Recurse | Where-Object { $_.Extension -match "\.(ttf|otf|tte|euf|fon)$" }

if ($fontFiles.Count -eq 0) {
    Write-Host "在指定目錄中未找到字型檔案" -ForegroundColor Red
    exit 1
}

Write-Host "`n找到的字型檔案：" -ForegroundColor Green
foreach ($file in $fontFiles) {
    Write-Host "  - $($file.Name) ($($file.Length) bytes, 修改時間: $($file.LastWriteTime))" -ForegroundColor Yellow
}

# 嘗試安裝字型檔案以供查看
$eudcFile = $fontFiles | Where-Object { $_.Name -eq "EUDC.TTE" }
if ($eudcFile) {
    Write-Host "`n找到主要造字檔案：$($eudcFile.FullName)" -ForegroundColor Green

    # 暫時複製到系統字型目錄（需要管理員權限）
    $systemFontPath = "C:\Windows\Fonts\DoMiSo_EUDC.TTE"

    try {
        Write-Host "嘗試複製造字檔案到系統目錄..." -ForegroundColor Yellow
        Copy-Item $eudcFile.FullName $systemFontPath -Force
        Write-Host "複製成功！" -ForegroundColor Green
        $fontInstalled = $true
    }
    catch {
        Write-Host "複製失敗（可能需要管理員權限）：$($_.Exception.Message)" -ForegroundColor Red
        $fontInstalled = $false
    }
}

# 創建 HTML 查看器
$outputFile = "DoMiSo_eudc_viewer.html"
Write-Host "`n正在創建 HTML 查看器：$outputFile" -ForegroundColor Yellow

$content = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DoMiSo 造字檔案查看器</title>
    <style>
        body {
            font-family: '新細明體', SimSun, serif;
            font-size: 14px;
            margin: 20px;
        }
        .info-section {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .char-grid {
            display: grid;
            grid-template-columns: repeat(16, 1fr);
            gap: 2px;
            margin-bottom: 30px;
        }
        .char-cell {
            border: 1px solid #ccc;
            text-align: center;
            padding: 5px;
            font-size: 20px;
            width: 50px;
            height: 50px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }
        .char-cell:hover {
            background-color: #e6f3ff;
            cursor: pointer;
        }
        .unicode-label {
            font-size: 8px;
            color: #666;
            position: absolute;
            bottom: 1px;
            left: 1px;
        }
        .header {
            background-color: #d0d0d0;
            font-weight: bold;
            font-size: 12px;
        }
        .section-title {
            background-color: #4CAF50;
            color: white;
            padding: 10px;
            margin: 20px 0 10px 0;
            border-radius: 3px;
        }
        .char-info {
            position: fixed;
            top: 10px;
            right: 10px;
            background: white;
            border: 2px solid #333;
            padding: 15px;
            border-radius: 5px;
            display: none;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
    </style>
    <script>
        function showCharInfo(unicode, char) {
            const info = document.getElementById('char-info');
            document.getElementById('info-unicode').textContent = unicode;
            document.getElementById('info-char').textContent = char;
            document.getElementById('info-decimal').textContent = parseInt(unicode.replace('U+',''), 16);
            info.style.display = 'block';
        }

        function hideCharInfo() {
            document.getElementById('char-info').style.display = 'none';
        }
    </script>
</head>
<body>
    <h1>DoMiSo 造字檔案查看器</h1>

    <div class="info-section">
        <h3>檔案資訊</h3>
        <p><strong>來源目錄：</strong>$FontPath</p>
        <p><strong>生成時間：</strong>$(Get-Date)</p>
        <p><strong>造字檔案：</strong></p>
        <ul>
"@

foreach ($file in $fontFiles) {
    $content += "            <li>$($file.Name) - $($file.Length) bytes (修改時間: $($file.LastWriteTime))</li>`n"
}

$content += @"
        </ul>
        <p><strong>使用說明：</strong></p>
        <ul>
            <li>滑鼠懸停任意字元可查看詳細資訊</li>
            <li>有字形顯示的位置表示該 Unicode 有造字</li>
            <li>空白或方框表示該位置沒有造字</li>
        </ul>
    </div>

    <div id="char-info" class="char-info">
        <h4>字元資訊</h4>
        <p><strong>Unicode：</strong><span id="info-unicode"></span></p>
        <p><strong>字元：</strong><span id="info-char" style="font-size: 24px;"></span></p>
        <p><strong>十進位：</strong><span id="info-decimal"></span></p>
    </div>
"@

# 生成多個區段的字元映射
$sections = @(
    @{Name = "私人使用區域 A (U+E000-U+E0FF)"; Start = 0xE000; End = 0xE0FF },
    @{Name = "私人使用區域 B (U+E100-U+E1FF)"; Start = 0xE100; End = 0xE1FF },
    @{Name = "私人使用區域 C (U+E200-U+E2FF)"; Start = 0xE200; End = 0xE2FF },
    @{Name = "私人使用區域 D (U+E300-U+E3FF)"; Start = 0xE300; End = 0xE3FF }
)

foreach ($section in $sections) {
    $content += "`n    <div class='section-title'>$($section.Name)</div>`n"
    $content += "    <div class='char-grid'>`n"

    # 生成表頭
    $content += "        <div class='char-cell header'></div>`n"
    for ($col = 0; $col -lt 16; $col++) {
        $content += "        <div class='char-cell header'>+$($col.ToString('X'))</div>`n"
    }

    # 生成字元網格
    for ($row = $section.Start; $row -le $section.End; $row += 16) {
        # 行標題
        $rowHex = $row.ToString("X4")
        $content += "        <div class='char-cell header'>$rowHex</div>`n"

        # 該行的16個字元
        for ($col = 0; $col -lt 16; $col++) {
            $unicode = $row + $col
            if ($unicode -le $section.End) {
                $char = [char]$unicode
                $unicodeStr = "U+" + $unicode.ToString("X4")
                $content += "        <div class='char-cell' onmouseover='showCharInfo(`"$unicodeStr`", `"$char`")' onmouseout='hideCharInfo()'>$char<span class='unicode-label'>$($unicode.ToString('X4'))</span></div>`n"
            }
        }
    }

    $content += "    </div>`n"
}

$content += @"

    <div class="info-section">
        <h3>說明</h3>
        <p>此工具顯示了 DoMiSo 造字檔案中的字元映射。每個格子代表一個 Unicode 位置：</p>
        <ul>
            <li><strong>有字形：</strong>該 Unicode 位置已定義造字</li>
            <li><strong>空白/方框：</strong>該 Unicode 位置未定義造字</li>
            <li><strong>格子標籤：</strong>顯示該位置的 Unicode 編碼（16進位）</li>
        </ul>
        <p><strong>注意：</strong>字元的顯示效果取決於系統是否正確載入了造字檔案。</p>
    </div>
</body>
</html>
"@

$content | Out-File -FilePath $outputFile -Encoding UTF8
Write-Host "HTML 查看器已創建：$outputFile" -ForegroundColor Green

# 自動開啟檔案
Write-Host "正在開啟 HTML 查看器..." -ForegroundColor Yellow
Start-Process $outputFile

Write-Host "`n=== 完成 ===" -ForegroundColor Green
Write-Host "如果字元無法正確顯示，可能需要：" -ForegroundColor Yellow
Write-Host "1. 以管理員身份執行此腳本" -ForegroundColor Yellow
Write-Host "2. 手動安裝造字檔案到系統" -ForegroundColor Yellow
Write-Host "3. 使用 BabelPad 等專業工具查看" -ForegroundColor Yellow