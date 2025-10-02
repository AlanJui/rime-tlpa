@echo off
echo ============================================
echo   清除 RIME (Weasel) 輸入法快取檔案
echo   位置: %APPDATA%\Rime\build
echo ============================================

REM 停止輸入法服務（Weasel）
taskkill /IM weaselserver.exe /F >nul 2>&1

REM 刪除 build 資料夾
if exist "%APPDATA%\Rime\build" (
    rmdir /S /Q "%APPDATA%\Rime\build"
    echo 已刪除 build 資料夾。
) else (
    echo 找不到 build 資料夾，可能已經清除。
)

REM 重新啟動 Weasel 服務
@REM start "" "C:\Program Files (x86)\Rime\weaselserver.exe"
start "" "C:\Program Files\Rime\weasel-0.17.4\WeaselServer.exe"

echo ============================================
echo   清除完成！請重新部署輸入法。
echo ============================================
pause
