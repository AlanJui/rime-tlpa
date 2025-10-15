@echo off
echo ================================
echo RIME TLPA 台語輸入法配置工具安裝
echo ================================
echo.

REM 設定目錄變數
set RIME_DIR=%APPDATA%\Rime
set INSTALL_DIR=%ProgramFiles%\RIME TLPA Tools

echo RIME 配置目錄: %RIME_DIR%
echo 工具安裝目錄: %INSTALL_DIR%
echo.

REM 檢查 RIME 目錄是否存在
if not exist "%RIME_DIR%" (
    echo ❌ 錯誤: RIME 配置目錄不存在
    echo 請先安裝 RIME 小狼毫輸入法
    echo 下載網址: https://rime.im/
    pause
    exit /b 1
)

echo ✅ 找到 RIME 配置目錄

REM 創建工具安裝目錄
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%" 2>nul

REM 備份現有的 default.custom.yaml
if exist "%RIME_DIR%\default.custom.yaml" (
    echo 📋 備份現有的 default.custom.yaml...
    copy "%RIME_DIR%\default.custom.yaml" "%RIME_DIR%\default.custom.yaml.bak" >nul
    echo    已備份為 default.custom.yaml.bak
)

REM 複製 RIME 配置檔案 (根據 release-include.txt)
echo 📄 複製 RIME 配置檔案...
if exist "rime_files\*" (
    copy "rime_files\*" "%RIME_DIR%\" >nul
    echo    已複製所有 RIME 配置檔案
) else (
    echo ❌ 錯誤: 找不到 rime_files 目錄
    pause
    exit /b 1
)

REM 複製工具程式檔案
if exist "*.exe" (
    echo 🔧 複製工具程式檔案...
    copy "*.exe" "%INSTALL_DIR%\" >nul 2>&1
    echo    已複製工具程式到安裝目錄
)

echo.
echo ✅ 安裝完成!
echo.
echo 📝 後續步驟:
echo 1. 開啟 RIME 小狼毫系統匣圖示
echo 2. 右鍵選擇「重新部署」
echo 3. 等待部署完成 (可能需要幾分鐘)
echo 4. 切換到 TLPA 台語輸入法方案
echo.
echo 📂 已安裝的檔案位置:
echo    RIME 配置: %RIME_DIR%
echo    工具程式: %INSTALL_DIR%
echo.
pause
