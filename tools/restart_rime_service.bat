@echo off
REM 停止輸入法服務（Weasel）
taskkill /IM weaselserver.exe /F >nul 2>&1

REM 重新啟動 Weasel 服務
@REM start "" "C:\Program Files (x86)\Rime\weaselserver.exe"
start "" "C:\Program Files\Rime\weasel-0.17.4\WeaselServer.exe"

echo ============================================
echo   RIME 服務已重啟！請重新部署輸入法。
echo ============================================
