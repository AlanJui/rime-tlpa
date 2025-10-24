# 詳細掃描私人使用區域造字
# 生成完整的 Unicode 映射表

Write-Host "=== 生成私人使用區域完整映射 ===" -ForegroundColor Green

$outputFile = "eudc_mapping_full.html"
$content = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>私人使用區域字元映射表</title>
    <style>
        body { font-family: '新細明體', SimSun, serif; font-size: 14px; }
        .char-grid { display: grid; grid-template-columns: repeat(16, 1fr); gap: 2px; }
        .char-cell {
            border: 1px solid #ccc;
            text-align: center;
            padding: 5px;
            font-size: 18px;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .unicode-label { font-size: 10px; color: #666; }
        .header { background-color: #f0f0f0; font-weight: bold; }
    </style>
</head>
<body>
    <h1>私人使用區域字元映射表 (U+E000-U+E1FF)</h1>
    <p>生成時間: $(Get-Date)</p>
    <p>說明：如果格子中顯示字形（不是空白或方框），表示該 Unicode 位置有造字</p>

    <div class="char-grid">
"@

# 生成表頭
for ($col = 0; $col -lt 16; $col++) {
    $content += "        <div class='char-cell header'>+$($col.ToString('X'))</div>`n"
}

# 生成字元網格 (E000-E1FF, 共512個字元)
for ($row = 0xE000; $row -le 0xE1FF; $row += 16) {
    # 行標題
    $rowHex = $row.ToString("X4")
    $content += "        <div class='char-cell header'>$rowHex</div>`n"

    # 該行的16個字元
    for ($col = 0; $col -lt 16; $col++) {
        $unicode = $row + $col
        $char = [char]$unicode
        $unicodeStr = $unicode.ToString("X4")
        $content += "        <div class='char-cell' title='U+$unicodeStr'>$char<br><span class='unicode-label'>$unicodeStr</span></div>`n"
    }
}

$content += @"
    </div>

    <h2>使用說明</h2>
    <ul>
        <li>每個格子顯示一個 Unicode 字元</li>
        <li>格子下方顯示該字元的 Unicode 編碼</li>
        <li>如果看到實際字形，表示該位置有造字</li>
        <li>如果看到空白或方框，表示該位置沒有造字</li>
        <li>滑鼠懸停可以看到 Unicode 編碼</li>
    </ul>

    <h2>完整私人使用區域範圍</h2>
    <ul>
        <li>基本私人使用區域：U+E000 - U+F8FF (6,400個位置)</li>
        <li>本表僅顯示：U+E000 - U+E1FF (512個位置)</li>
    </ul>
</body>
</html>
"@

$content | Out-File -FilePath $outputFile -Encoding UTF8
Write-Host "HTML 映射表已創建：$outputFile" -ForegroundColor Green
Write-Host "請用瀏覽器開啟此文件查看結果" -ForegroundColor Yellow

# 自動開啟文件
Start-Process $outputFile