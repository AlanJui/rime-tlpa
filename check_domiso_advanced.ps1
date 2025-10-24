# DoMiSo 造字檔案查看器 - 進階版本
# 包含字型載入功能

param(
    [string]$FontPath = "C:\work\DoMiSo_Zu_Im\EUDC.TTE"
)

Write-Host "=== DoMiSo 造字檔案進階查看器 ===" -ForegroundColor Green

# 檢查檔案是否存在
if (-not (Test-Path $FontPath)) {
    Write-Host "錯誤：檔案不存在 - $FontPath" -ForegroundColor Red
    exit 1
}

$fontFile = Get-Item $FontPath
Write-Host "目標檔案：$($fontFile.FullName)" -ForegroundColor Yellow
Write-Host "檔案大小：$($fontFile.Length) bytes" -ForegroundColor Yellow
Write-Host "修改時間：$($fontFile.LastWriteTime)" -ForegroundColor Yellow

# 創建互動式 HTML 查看器
$outputFile = "DoMiSo_Interactive_Viewer.html"
Write-Host "`n正在創建互動式查看器：$outputFile" -ForegroundColor Yellow

$content = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DoMiSo 造字檔案互動查看器</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
        }
        .font-selector {
            margin: 20px 0;
            padding: 15px;
            background-color: #e8f4f8;
            border-radius: 5px;
        }
        .controls {
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }
        .control-group label {
            font-size: 12px;
            font-weight: bold;
            color: #333;
        }
        select, input {
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        .char-grid {
            display: grid;
            grid-template-columns: repeat(16, 1fr);
            gap: 2px;
            margin: 20px 0;
            border: 2px solid #ddd;
            padding: 10px;
            border-radius: 5px;
            background: white;
        }
        .char-cell {
            border: 1px solid #ccc;
            text-align: center;
            padding: 5px;
            font-size: 24px;
            width: 50px;
            height: 50px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
            background: white;
            transition: all 0.2s;
        }
        .char-cell:hover {
            background-color: #e6f3ff;
            transform: scale(1.1);
            z-index: 10;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            cursor: pointer;
        }
        .unicode-label {
            font-size: 9px;
            color: #666;
            position: absolute;
            bottom: 2px;
            font-family: monospace;
        }
        .header-cell {
            background-color: #4a5568;
            color: white;
            font-weight: bold;
            font-size: 11px;
            font-family: monospace;
        }
        .row-header {
            background-color: #2d3748;
            color: white;
            font-weight: bold;
            font-size: 11px;
            font-family: monospace;
        }
        .char-info {
            position: fixed;
            top: 50px;
            right: 20px;
            background: white;
            border: 3px solid #4a5568;
            padding: 20px;
            border-radius: 10px;
            display: none;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            z-index: 1000;
            min-width: 200px;
        }
        .char-display {
            font-size: 48px;
            text-align: center;
            margin: 10px 0;
            padding: 20px;
            border: 2px solid #eee;
            border-radius: 5px;
            background: #f9f9f9;
        }
        .range-info {
            background: #e8f4f8;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            border-left: 4px solid #4a5568;
        }
        .used-chars {
            background: #e6ffed;
            color: #22543d;
            font-weight: bold;
        }
        .empty-chars {
            background: #fed7d7;
            color: #742a2a;
        }
        .stats {
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }
        .stat-box {
            flex: 1;
            padding: 15px;
            text-align: center;
            border-radius: 5px;
            color: white;
        }
        .stat-used { background: #48bb78; }
        .stat-empty { background: #f56565; }
        .stat-total { background: #4a5568; }
    </style>
    <script>
        let currentFont = 'Arial';
        let fontSize = 24;

        function showCharInfo(unicode, char, element) {
            const info = document.getElementById('char-info');
            const decimal = parseInt(unicode.replace('U+',''), 16);

            document.getElementById('info-unicode').textContent = unicode;
            document.getElementById('info-char').textContent = char;
            document.getElementById('info-decimal').textContent = decimal;
            document.getElementById('info-font').textContent = currentFont;

            // 設定顯示字元的字型
            const charDisplay = document.getElementById('info-char');
            charDisplay.style.fontFamily = currentFont;

            info.style.display = 'block';
        }

        function hideCharInfo() {
            document.getElementById('char-info').style.display = 'none';
        }

        function changeFont() {
            const fontSelect = document.getElementById('font-select');
            currentFont = fontSelect.value;

            // 更新所有字元的字型
            const cells = document.querySelectorAll('.char-cell:not(.header-cell):not(.row-header)');
            cells.forEach(cell => {
                cell.style.fontFamily = currentFont;
            });

            updateStats();
        }

        function changeFontSize() {
            const sizeInput = document.getElementById('font-size');
            fontSize = parseInt(sizeInput.value);

            const cells = document.querySelectorAll('.char-cell:not(.header-cell):not(.row-header)');
            cells.forEach(cell => {
                cell.style.fontSize = fontSize + 'px';
            });
        }

        function updateStats() {
            // 這裡可以添加統計功能
            console.log('字型已更改為:', currentFont);
        }

        window.onload = function() {
            changeFont();
        }
    </script>
</head>
<body onload="changeFont()">
    <div class="container">
        <div class="header">
            <h1>🔤 DoMiSo 造字檔案互動查看器</h1>
            <p>檔案來源：$FontPath</p>
            <p>生成時間：$(Get-Date -Format "yyyy-MM-dd HH:mm:ss")</p>
        </div>

        <div class="font-selector">
            <div class="controls">
                <div class="control-group">
                    <label for="font-select">選擇字型：</label>
                    <select id="font-select" onchange="changeFont()">
                        <option value="Arial">Arial</option>
                        <option value="新細明體, SimSun">新細明體</option>
                        <option value="標楷體, DFKai-SB">標楷體</option>
                        <option value="微軟正黑體, Microsoft JhengHei">微軟正黑體</option>
                        <option value="Consolas, monospace">Consolas</option>
                        <option value="Times New Roman">Times New Roman</option>
                    </select>
                </div>
                <div class="control-group">
                    <label for="font-size">字型大小：</label>
                    <input type="range" id="font-size" min="12" max="48" value="24" onchange="changeFontSize()">
                    <span id="size-display">24px</span>
                </div>
            </div>
        </div>

        <div class="stats">
            <div class="stat-box stat-total">
                <div style="font-size: 24px; margin-bottom: 5px;">📊</div>
                <div>總範圍</div>
                <div style="font-size: 18px; font-weight: bold;">1024 個位置</div>
            </div>
            <div class="stat-box stat-used">
                <div style="font-size: 24px; margin-bottom: 5px;">✅</div>
                <div>已使用</div>
                <div style="font-size: 18px; font-weight: bold;" id="used-count">檢查中...</div>
            </div>
            <div class="stat-box stat-empty">
                <div style="font-size: 24px; margin-bottom: 5px;">⬜</div>
                <div>未使用</div>
                <div style="font-size: 18px; font-weight: bold;" id="empty-count">檢查中...</div>
            </div>
        </div>

        <div id="char-info" class="char-info">
            <h4>📝 字元詳細資訊</h4>
            <p><strong>Unicode：</strong><span id="info-unicode"></span></p>
            <div class="char-display" id="info-char"></div>
            <p><strong>十進位：</strong><span id="info-decimal"></span></p>
            <p><strong>當前字型：</strong><span id="info-font"></span></p>
        </div>
"@

# 生成四個主要區段
$sections = @(
    @{Name = "🔤 私人使用區域 A"; Range = "U+E000-U+E0FF"; Start = 0xE000; End = 0xE0FF },
    @{Name = "🔤 私人使用區域 B"; Range = "U+E100-U+E1FF"; Start = 0xE100; End = 0xE1FF },
    @{Name = "🔤 私人使用區域 C"; Range = "U+E200-U+E2FF"; Start = 0xE200; End = 0xE2FF },
    @{Name = "🔤 私人使用區域 D"; Range = "U+E300-U+E3FF"; Start = 0xE300; End = 0xE3FF }
)

foreach ($section in $sections) {
    $content += "`n        <div class='range-info'>`n"
    $content += "            <h3>$($section.Name) ($($section.Range))</h3>`n"
    $content += "            <p>範圍：$($section.Range)，共 256 個字元位置</p>`n"
    $content += "        </div>`n"
    $content += "        <div class='char-grid'>`n"

    # 生成表頭
    $content += "            <div class='char-cell header-cell'></div>`n"
    for ($col = 0; $col -lt 16; $col++) {
        $content += "            <div class='char-cell header-cell'>+$($col.ToString('X'))</div>`n"
    }

    # 生成字元網格
    for ($row = $section.Start; $row -le $section.End; $row += 16) {
        $rowHex = $row.ToString("X4")
        $content += "            <div class='char-cell row-header'>$rowHex</div>`n"

        for ($col = 0; $col -lt 16; $col++) {
            $unicode = $row + $col
            if ($unicode -le $section.End) {
                $char = [char]$unicode
                $unicodeStr = "U+" + $unicode.ToString("X4")
                $content += "            <div class='char-cell' onmouseover='showCharInfo(`"$unicodeStr`", `"$char`", this)' onmouseout='hideCharInfo()'>$char<span class='unicode-label'>$($unicode.ToString('X4'))</span></div>`n"
            }
        }
    }

    $content += "        </div>`n"
}

$content += @"

        <div class="range-info">
            <h3>📋 使用說明</h3>
            <ul>
                <li><strong>滑鼠懸停</strong>任意字元格查看詳細資訊</li>
                <li><strong>更換字型</strong>可能顯示不同的造字內容</li>
                <li><strong>調整字型大小</strong>以獲得最佳查看效果</li>
                <li><strong>有字形顯示</strong>表示該 Unicode 位置有造字</li>
                <li><strong>空白或方框</strong>表示該位置沒有造字</li>
            </ul>

            <h4>💡 提示</h4>
            <p>如果字元無法正確顯示，請嘗試：</p>
            <ul>
                <li>更換不同的字型選項</li>
                <li>使用 BabelPad 等專業 Unicode 編輯器</li>
                <li>確認造字檔案已正確安裝到系統</li>
            </ul>
        </div>
    </div>

    <script>
        // 更新字型大小顯示
        document.getElementById('font-size').oninput = function() {
            document.getElementById('size-display').textContent = this.value + 'px';
            changeFontSize();
        }
    </script>
</body>
</html>
"@

$content | Out-File -FilePath $outputFile -Encoding UTF8
Write-Host "互動式查看器已創建：$outputFile" -ForegroundColor Green

# 開啟檔案
Write-Host "正在開啟互動式查看器..." -ForegroundColor Yellow
Start-Process $outputFile

Write-Host "`n=== 完成 ===" -ForegroundColor Green
Write-Host "互動式查看器功能：" -ForegroundColor Cyan
Write-Host "✅ 可切換不同字型查看造字" -ForegroundColor Green
Write-Host "✅ 可調整字型大小" -ForegroundColor Green
Write-Host "✅ 滑鼠懸停顯示字元詳細資訊" -ForegroundColor Green
Write-Host "✅ 涵蓋 U+E000-E3FF 共1024個位置" -ForegroundColor Green