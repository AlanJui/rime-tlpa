# version: "v0.1.0.0"
#!/bin/bash

# 定義目標資料夾和文件路徑
#================================================================================
# Linux iBus-RIME: "HOME/.config/ibus/rime"
# macOS: ~/Library/Rime
#================================================================================
# RIME_USER_DIR="$HOME/.config/ibus/rime"  # Linux 路徑，macOS 改為 ~/Library/Rime
RIME_USER_DIR="$HOME/.config/rime"  # Linux 路徑，macOS 改為 ~/Library/Rime
CUSTOM_FILE="$RIME_USER_DIR/default.custom.yaml"

# 確保目標資料夾存在
if [ ! -d "$RIME_USER_DIR" ]; then
  echo "RIME 資料夾未找到，請確認您已安裝 RIME 輸入法。"
  exit 1
fi

# 複製方案文件到 RIME 資料夾
echo "正在複製必要文件..."
cp ./my_*.schema.yaml "$RIME_USER_DIR/"
cp ./kb_*.schema.yaml "$RIME_USER_DIR/"
cp ./zu_im_*.schema.yaml "$RIME_USER_DIR/"
cp ./tlpa_*.schema.yaml "$RIME_USER_DIR/"
cp ./huan_ciat_*.schema.yaml "$RIME_USER_DIR/"
cp ./keymap_*.schema.yaml "$RIME_USER_DIR/"
cp ./lib_*.yaml "$RIME_USER_DIR/"
cp ./tl_ji_khoo_*.dict.yaml "$RIME_USER_DIR/"
cp ./config/default.custom.yaml "$RIME_USER_DIR/"  # 如果有自定義配置文件
cp ./config/weasel.custom.yaml "$RIME_USER_DIR/"  # 如果有自定義配置文件
cp ./rime.lua "$RIME_USER_DIR/"   # 複製 Lua 腳本
cp ./lua/*.lua "$RIME_USER_DIR/"   # 複製 Lua 腳本

# 如果有其他必要的文件，也可以在此複製
# cp ./other_file "$RIME_USER_DIR/"
# 如果 default.custom.yaml 不存在，創建新文件
if [ ! -f "$CUSTOM_FILE" ]; then
  echo "default.custom.yaml 不存在，正在創建..."
  echo "patch:" > "$CUSTOM_FILE"
fi

# 檢查文件中是否已包含設定（避免重複追加）
if grep -q "方音符號鍵盤練習" "$CUSTOM_FILE"; then
  echo "設定已存在，無需重複追加。"
else
  # 將您的設定追加到文件末尾
  cat << EOF >> "$CUSTOM_FILE"

#------------------------------------------------------------------------
# 實驗/測試用
#------------------------------------------------------------------------
# - { schema: my_Tai_Gi_BoPoMo_Module }   # 台語ㄅㄆㄇ（模組結構）
# - { schema: Tai_Gi_BoPoMo }             # 台語ㄅㄆㄇ
# - { schema: my_bopomofo }
# - { schema: my_hong_im }
#------------------------------------------------------------------------
# 注音輸入法鍵盤練習
#------------------------------------------------------------------------
- { schema: kb_hong_im }        # 方音按鍵練習
- { schema: kb_zu_im }          # 注音按鍵練習
- { schema: kb_taigi_bopomo }   # 台語ㄅㄆㄇ按鍵練習
#------------------------------------------------------------------------
# 方音/注音符號輸入法
#------------------------------------------------------------------------
- { schema: zu_im_hong_im }         # 方音符號
- { schema: zu_im_piau_im }         # 十五音及方音符號
- { schema: zu_im_tlpa }            # 台語音標-注音
- { schema: zu_im_tai_gi_bopomo }   # 台語ㄅㄆㄇ
#------------------------------------------------------------------------
# TLPA 台語音標輸入法
#------------------------------------------------------------------------
- { schema: tlpa_phing_im } # 拼音輸入法，台語音標（TLPA）
- { schema: tlpa_piau_im }  # 拼音輸入法，十五音及方音符號
- { schema: tlpa_zu_im }    # 拼音輸入法，台語音標-注音
- { schema: tlpa_hong_im }  # 拼音輸入法，台語ㄅㄆㄇ
#------------------------------------------------------------------------
# 反切輸入法（拼音字母）
#------------------------------------------------------------------------
- { schema: huan_ciat_kong_un }         # 廣韻
- { schema: huan_ciat_sip_ngoo_im }     # 台灣改良之進階十五音
- { schema: huan_ciat_nga_siok_thong }  # 雅俗通十五音
#------------------------------------------------------------------------

EOF
  echo "設定已成功追加到 default.custom.yaml"
fi

# 通知用戶重新部署
echo "文件已成功複製至 $RIME_USER_DIR"
echo "請重新部署 RIME 輸入法（例如，按 Ctrl + `，並選擇重新部署）。"
