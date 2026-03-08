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
echo === 複製輸入法方案文件 ===

REM 複製主要方案文件
copy "tlpa_phing_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1
if exist "%RIME_DIR%\tlpa_phing_im.schema.yaml" echo ✓ tlpa_phing_im.schema.yaml
copy "tlpa_hong_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tlpa_hong_im.schema.yaml
copy "tlpa_khau_ik_zu_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tlpa_khau_ik_zu_im.schema.yaml
copy "sgi_zu_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ sgi_zu_im.schema.yaml
copy "sgi_ping_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ sgi_ping_im.schema.yaml
copy "zu_im_2_phing_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ zu_im_2_phing_im.schema.yaml
copy "zu_im_2_hong_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ zu_im_2_hong_im.schema.yaml
copy "bp_phing_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ bp_phing_im.schema.yaml
copy "bp_hong_im.schema.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ bp_hong_im.schema.yaml

echo.
echo === 複製字典文件 ===

REM 複製字典文件
copy "tl_han_ji_khoo.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tl_han_ji_khoo.dict.yaml
copy "tl_ji_khoo.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tl_ji_khoo.dict.yaml
copy "tl_ji_khoo_ciann_ji.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tl_ji_khoo_ciann_ji.dict.yaml
copy "tl_ji_khoo_II.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tl_ji_khoo_II.dict.yaml
copy "tl_ji_khoo_kah_kut_bun.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tl_ji_khoo_kah_kut_bun.dict.yaml
copy "tl_ji_khoo_kong_un.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tl_ji_khoo_kong_un.dict.yaml
copy "tl_ji_khoo_nga_siok_thong.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tl_ji_khoo_nga_siok_thong.dict.yaml
copy "tl_ji_khoo_peh_ue.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tl_ji_khoo_peh_ue.dict.yaml
copy "tl_ji_khoo_zu_ting.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tl_ji_khoo_zu_ting.dict.yaml
copy "zu_im_2.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ zu_im_2.dict.yaml
copy "bp_ji_khoo.dict.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ bp_ji_khoo.dict.yaml

echo.
echo === 複製庫文件 ===

REM 複製庫文件
copy "tlpa_lib_hau_suan_tuann.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tlpa_lib_hau_suan_tuann.yaml
copy "tlpa_lib_hong_im_hau_suan_ji_tuann.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tlpa_lib_hong_im_hau_suan_ji_tuann.yaml
copy "tlpa_lib_zu_im_hau_suan_ji_tuann.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tlpa_lib_zu_im_hau_suan_ji_tuann.yaml
copy "tlpa_kik_kan_sip_goo_im_libs.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ tlpa_kik_kan_sip_goo_im_libs.yaml
copy "zu_im_2_libs.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ zu_im_2_libs.yaml
copy "zu_im_2_hau_suan_zzi_duann.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ zu_im_2_hau_suan_zzi_duann.yaml
copy "bp_libs.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ bp_libs.yaml
copy "bp_libs_hst_phing_im.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ bp_libs_hst_phing_im.yaml
copy "bp_libs_hst_zu_im.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ bp_libs_hst_zu_im.yaml
copy "bp_libs_R0.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ bp_libs_R0.yaml
copy "bp_libs_R1.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ bp_libs_R1.yaml

echo.
echo === 複製其他配置文件 ===

REM 複製其他重要文件
copy "rime.lua" "%RIME_DIR%\" >nul 2>&1 && echo ✓ rime.lua
copy "keymap_piau_tian.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ keymap_piau_tian.yaml
copy "lib_hau_suan_ji_tuann.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ lib_hau_suan_ji_tuann.yaml
copy "lib_phing_im.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ lib_phing_im.yaml
copy "lib_sip_ngoo_im.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ lib_sip_ngoo_im.yaml
copy "lib_zu_im.yaml" "%RIME_DIR%\" >nul 2>&1 && echo ✓ lib_zu_im.yaml

REM 複製lua目錄
if exist "lua" (
    if not exist "%RIME_DIR%\lua" mkdir "%RIME_DIR%\lua"
    copy "lua\*" "%RIME_DIR%\lua\" >nul 2>&1 && echo ✓ lua目錄
)

echo.
echo === 創建default.custom.yaml配置 ===

REM 創建default.custom.yaml
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
echo     # 台語拼音輸入法 ^(TLPA^)
echo     - { schema: tlpa_phing_im }     # 拼音輸入法【台語音標】
echo     - { schema: tlpa_hong_im }      # 注音輸入法【台語音標】
echo     - { schema: tlpa_khau_ik_zu_im } # 巧易注音輸入法
echo.
echo     # 極簡注音
echo     - { schema: sgi_zu_im }         # 極簡注音符號【十五音】
echo.
echo     # 台語注音二式
echo     - { schema: zu_im_2_phing_im }  # 台語注音二式拼音輸入法
echo     - { schema: zu_im_2_hong_im }   # 台語注音二式注音輸入法
echo.
echo     # 閩拼方案 ^(BP^)
echo     - { schema: bp_phing_im }       # 閩拼方案拼音輸入法
echo     - { schema: bp_hong_im }        # 閩拼方案注音輸入法
) > "%RIME_DIR%\default.custom.yaml"

echo ✓ 已創建default.custom.yaml

echo.
echo === 部署完成！ ===
echo.
echo 請按照以下步驟完成設置：
echo 1. 在系統托盤找到RIME（小狼毫）圖標
echo 2. 右鍵點擊選擇「重新部署」
echo 3. 等待部署完成後，按 Ctrl+` 調出輸入法選單
echo 4. 選擇您想使用的台語輸入法
echo.
echo 可用的台語輸入法：
echo • 台語拼音輸入法 (TLPA)
echo • 台語注音輸入法 (方音符號)
echo • 極簡注音符號 (十五音)
echo • 台語注音二式輸入法
echo • 閩拼方案輸入法 (BP)
echo.

pause
