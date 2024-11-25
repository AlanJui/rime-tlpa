@echo off

:: 定義目標資料夾和文件路徑
set RIME_DIR=%APPDATA%\Rime
set CUSTOM_FILE=%RIME_DIR%\default.custom.yaml

:: 確保目標資料夾存在
if not exist "%RIME_DIR%" (
    echo 無法找到 RIME 資料夾，請確認已安裝 RIME 輸入法。
    pause
    exit /b
)

:: ===========================================================
:: 複製文件到 RIME 資料夾
:: ===========================================================
echo 正在安裝【輸入法按鍵練習工具】...
copy kb_*.schema.yaml "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製 kb_*.schema.yaml，請確認文件是否存在。
    pause
    exit /b
)

echo 正在安裝【閩拼式輸入法】...
copy BP_*.schema.yaml "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製 BP_*.schema.yaml，請確認文件是否存在。
    pause
    exit /b
)

echo 正在安裝【注音符號輸入法】...
copy zu_im_*.schema.yaml "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製 zu_im_*.schema.yaml，請確認文件是否存在。
    pause
    exit /b
)

echo 正在安裝【台語音標輸入法】...
copy tlpa_*.schema.yaml "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製 tlpa_*.schema.yaml，請確認文件是否存在。
    pause
    exit /b
)

echo 正在安裝【反切輸入法】...
copy huan_ciat_*.schema.yaml "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製 huan_ciat_*.schema.yaml，請確認文件是否存在。
    pause
    exit /b
)

:: ===========================================================
:: 複製輸入法使用之漢字庫到 RIME 資料夾
:: ===========================================================

:: 複製白話音用漢字庫
copy tl_ji_khoo_peh_ue*.dict.yaml "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製 tl_ji_khoo_peh_ue*.dict.yaml，請確認文件是否存在。
    pause
    exit /b
)

:: 複製雅俗通十五音用漢字庫
copy tl_ji_khoo_nga_siok_thong.dict.yaml "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製 tl_ji_khoo_nga_siok_thong.dict.yaml，請確認文件是否存在。
    pause
    exit /b
)

:: 複製《廣韻》用漢字庫
copy tl_ji_khoo_kong_un.dict.yaml "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製 tl_ji_khoo_kong_un.dict.yaml，請確認文件是否存在。
    pause
    exit /b
)

:: 複製輸入法使用之【標點符號】
copy piau_tian_hu_ho.yaml "%RIME_DIR%"
copy keymap_*.yaml "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製標點符號檔【keymap_*.yaml】，請確認文件是否存在。
    pause
    exit /b
)

copy .\config\weasel.custom.yaml "%RIME_DIR%"
copy rime.lua "%RIME_DIR%"
if %errorlevel% neq 0 (
    echo 無法複製 Lua 腳本，請確認文件是否存在。
    pause
    exit /b
)

:: 如果 default.custom.yaml 不存在，創建新文件
if not exist "%CUSTOM_FILE%" (
    echo "default.custom.yaml 不存在，正在創建..."
    echo patch: > "%CUSTOM_FILE%"
)

:: 檢查文件是否已包含設定
findstr "方音符號鍵盤練習" "%CUSTOM_FILE%" >nul
if %errorlevel% equ 0 (
    echo "設定已存在，無需重複追加。"
    goto end
)

:: 追加設定到文件末尾
echo 正在將設定追加到 default.custom.yaml...
type settings_to_append.txt >> "%CUSTOM_FILE%"

:end
echo 設定已成功追加到 default.custom.yaml
echo 所有文件已成功安裝至 %RIME_DIR%。
echo 請右鍵點擊系統托盤中的 RIME 圖標，選擇 "重新部署" 以啟用新方案。
pause

