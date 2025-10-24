# 檢查系統造字檔案中已使用的 Unicode 編碼
# 作者：AlanJui
# 日期：2025-10-25

Write-Host "=== 檢查系統造字檔案 ===" -ForegroundColor Green

# 檢查造字檔案是否存在
$eudcPath = "C:\Windows\Fonts\EUDC.TTE"
if (Test-Path $eudcPath) {
    Write-Host "找到造字檔案：$eudcPath" -ForegroundColor Yellow
    $fileInfo = Get-Item $eudcPath
    Write-Host "檔案大小：$($fileInfo.Length) bytes"
    Write-Host "最後修改：$($fileInfo.LastWriteTime)"
}
else {
    Write-Host "未找到造字檔案：$eudcPath" -ForegroundColor Red
}

Write-Host "`n=== 建議的檢查方法 ===" -ForegroundColor Green
Write-Host "1. 使用字元對應表 (charmap) 檢查"
Write-Host "2. 使用 BabelPad 逐一檢查 U+E000-U+F8FF 範圍"
Write-Host "3. 創建測試文件包含所有私人使用區字元"

# 創建測試用的 Unicode 範圍文件
$outputFile = "unicode_private_use_test.txt"
Write-Host "`n正在創建測試文件：$outputFile" -ForegroundColor Yellow

$content = @"
私人使用區域字元測試文件
生成時間：$(Get-Date)

私人使用區域範圍：U+E000 - U+F8FF

以下是私人使用區域的字元（如果顯示為字形而非方框，表示該位置有造字）：

"@

# 生成 U+E000 到 U+E0FF 的字元（前256個位置作為樣本）
for ($i = 0xE000; $i -le 0xE0FF; $i++) {
    $unicode = [char]$i
    $hex = $i.ToString("X4")
    if (($i - 0xE000) % 16 -eq 0) {
        $content += "`nU+$hex`: "
    }
    $content += "$unicode "
}

$content += @"


測試說明：
1. 如果看到實際字形（不是方框□），表示該 Unicode 位置有造字
2. 如果看到方框□或空白，表示該位置沒有造字
3. 完整範圍：U+E000 到 U+F8FF（共6400個位置）

建議使用工具：
- BabelPad：最佳的 Unicode 字元查看工具
- 字元對應表：Windows 內建工具
- 支援 Unicode 的文字編輯器

"@

$content | Out-File -FilePath $outputFile -Encoding UTF8
Write-Host "測試文件已創建：$outputFile" -ForegroundColor Green
Write-Host "請在支援 Unicode 的編輯器中開啟此文件查看結果"