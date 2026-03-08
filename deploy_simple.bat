@echo off
echo === RIME-TLPA 台語輸入法部署 ===
echo.

set RIME_DIR=%APPDATA%\Rime
echo RIME用戶目錄: %RIME_DIR%

if not exist "%RIME_DIR%" (
    mkdir "%RIME_DIR%"
    echo 已創建RIME用戶目錄
)

echo.
echo === 複製核心文件 ===

REM 複製主要方案文件
copy "tlpa_phing_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\tlpa_phing_im.schema.yaml" echo ✓ tlpa_phing_im.schema.yaml

copy "tlpa_hong_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\tlpa_hong_im.schema.yaml" echo ✓ tlpa_hong_im.schema.yaml

copy "sgi_zu_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\sgi_zu_im.schema.yaml" echo ✓ sgi_zu_im.schema.yaml

copy "zu_im_2_phing_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\zu_im_2_phing_im.schema.yaml" echo ✓ zu_im_2_phing_im.schema.yaml

copy "bp_phing_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\bp_phing_im.schema.yaml" echo ✓ bp_phing_im.schema.yaml

REM 複製主要字典
copy "tl_han_ji_khoo.dict.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\tl_han_ji_khoo.dict.yaml" echo ✓ tl_han_ji_khoo.dict.yaml

copy "tl_ji_khoo_peh_ue.dict.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\tl_ji_khoo_peh_ue.dict.yaml" echo ✓ tl_ji_khoo_peh_ue.dict.yaml

REM 複製重要庫文件
copy "tlpa_lib_hau_suan_tuann.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\tlpa_lib_hau_suan_tuann.yaml" echo ✓ tlpa_lib_hau_suan_tuann.yaml

copy "tlpa_kik_kan_sip_goo_im_libs.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\tlpa_kik_kan_sip_goo_im_libs.yaml" echo ✓ tlpa_kik_kan_sip_goo_im_libs.yaml

copy "rime.lua" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\rime.lua" echo ✓ rime.lua

copy "keymap_piau_tian.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\keymap_piau_tian.yaml" echo ✓ keymap_piau_tian.yaml

echo.
echo === 創建配置文件 ===

(
echo customization:
echo   distribution_code_name: Weasel
echo   distribution_version: 0.16.0
echo   generator: "Rime::SwitcherSettings"
echo   modified_time: "%date% %time%"
echo   rime_version: 1.11.2
echo.
echo patch:
echo   "log/level": "info"
echo   schema_list:
echo     # 台語拼音輸入法
echo     - { schema: tlpa_phing_im }
echo     - { schema: tlpa_hong_im }
echo     - { schema: sgi_zu_im }
echo     - { schema: zu_im_2_phing_im }
echo     - { schema: bp_phing_im }
) > "%RIME_DIR%\default.custom.yaml"

echo ✓ 已創建default.custom.yaml

echo.
echo === 部署完成！ ===
echo.
echo 接下來請：
echo 1. 在系統托盤右鍵點擊RIME圖標
echo 2. 選擇「重新部署」
echo 3. 按 Ctrl+` 選擇台語輸入法
echo.
