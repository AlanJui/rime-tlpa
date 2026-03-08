# RIME-TLPA 台語輸入法部署指南

## 系統環境檢查
✅ Windows系統已確認
✅ RIME (小狼毫) 已安裝在: C:\Program Files\Rime
✅ RIME用戶目錄: C:\Users\AlanJui\AppData\Roaming\Rime

## 手動部署步驟

### 第一步：複製核心文件到RIME用戶目錄

請將以下文件從專案目錄複製到 `%APPDATA%\Rime\` 目錄：

#### 主要方案文件 (.schema.yaml)
- tlpa_phing_im.schema.yaml (台語拼音輸入法)
- tlpa_hong_im.schema.yaml (台語注音輸入法)
- tlpa_khau_ik_zu_im.schema.yaml (巧易注音輸入法)
- sgi_zu_im.schema.yaml (使用注音符號的十五音輸入法)
- sgi_ping_im.schema.yaml (使用羅馬拼音的十五音輸入法)
- zu_im_2_phing_im.schema.yaml (台語注音二式拼音)
- zu_im_2_hong_im.schema.yaml (台語注音二式注音)
- bp_phing_im.schema.yaml (閩拼方案拼音)
- bp_hong_im.schema.yaml (閩拼方案注音)

#### 字典文件 (.dict.yaml)
- tl_han_ji_khoo.dict.yaml (主要台語字典)
- tl_ji_khoo_peh_ue.dict.yaml (白話音字典)
- 其他字典文件 (按需要複製)

#### 庫文件 (.yaml)
- tlpa_lib_hau_suan_tuann.yaml
- tlpa_kik_kan_sip_goo_im_libs.yaml
- zu_im_2_libs.yaml
- bp_libs.yaml
- rime.lua
- keymap_piau_tian.yaml

#### 配置文件
- default.custom.yaml (已在專案目錄中準備好)

### 第二步：快速複製指令 (在命令提示符中執行)

```cmd
# 設定目標目錄
set DEST=%APPDATA%\Rime

# 複製核心方案文件
copy tlpa_phing_im.schema.yaml "%DEST%\"
copy tlpa_hong_im.schema.yaml "%DEST%\"
copy sgi_zu_im.schema.yaml "%DEST%\"
copy zu_im_2_phing_im.schema.yaml "%DEST%\"
copy bp_phing_im.schema.yaml "%DEST%\"

# 複製主要字典
copy tl_han_ji_khoo.dict.yaml "%DEST%\"
copy tl_ji_khoo_peh_ue.dict.yaml "%DEST%\"

# 複製庫文件
copy tlpa_lib_hau_suan_tuann.yaml "%DEST%\"
copy tlpa_kik_kan_sip_goo_im_libs.yaml "%DEST%\"
copy rime.lua "%DEST%\"
copy keymap_piau_tian.yaml "%DEST%\"

# 複製配置文件
copy default.custom.yaml "%DEST%\"
```

### 第三步：重新部署RIME

1. 在系統托盤找到RIME (小狼毫) 圖標
2. 右鍵點擊圖標
3. 選擇「重新部署」或「Deploy」
4. 等待部署完成

### 第四步：選擇輸入法

1. 切換到RIME輸入法
2. 按 `Ctrl + ` 調出輸入法選單
3. 選擇想要使用的台語輸入法：
   - 拼音輸入法【台語音標】
   - 注音輸入法【台語音標】
   - 極簡注音符號【十五音】
   - 台語注音二式拼音輸入法
   - 閩拼方案拼音輸入法

## 測試輸入法

### 台語拼音輸入法 (tlpa_phing_im)
- 輸入: `tai5 gi2` → 候選字: 台語
- 輸入: `ho2 lo5` → 候選字: 河洛

### 注音輸入法 (tlpa_hong_im)
- 使用方音符號按鍵輸入

### 聲調輸入方式
- 第1調 (陰平): `;`
- 第2調 (上聲): `\`
- 第3調 (陰去): `_`
- 第5調 (陽平): `/`
- 第7調 (陽去): `-`
- 第4調 (陰入): `[`
- 第8調 (陽入): `]`

## 常見問題

### Q: 部署後看不到台語輸入法選項
A: 請檢查:
1. 文件是否正確複製到RIME用戶目錄
2. default.custom.yaml是否正確配置
3. 重新部署是否成功完成

### Q: 輸入沒有候選字
A: 請確保:
1. 字典文件已正確複製
2. 方案文件中的字典路徑正確
3. 重新部署RIME

### Q: 按鍵對應不正確
A: 請檢查:
1. keymap_piau_tian.yaml是否已複製
2. 方案文件中的按鍵配置

## 支援的輸入法特色

1. **多種標音系統**: 支援TLPA、BP、台語注音二式
2. **完整聲調**: 支援台語八聲調
3. **變調處理**: 自動處理閩南話變調規則
4. **鼻化韻母**: 支援鼻化符號標記
5. **地方腔調**: 相容泉州、漳州、廈門腔

部署完成後，您就可以開始使用這套完整的台語輸入法系統了！
