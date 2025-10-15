# RIME TLPA 打包安裝程式

## 概述

本專案提供完整的 RIME TLPA 台語輸入法配置工具打包和安裝解決方案，能夠自動：

1. 根據 `release-include.txt` 指定的檔案進行打包
2. 備份使用者現有的 `default.custom.yaml`
3. 複製所有 RIME 配置檔案到正確位置
4. 自動觸發 RIME 重新部署

## 檔案結構

```
rime-tlpa/
├── release-include.txt          # 指定要包含的 RIME 檔案清單
├── config/
│   └── default.custom.yaml     # 新的 RIME 設定檔
├── tools/
│   ├── build_system.py         # 完整建置系統
│   ├── rime_installer.py       # RIME TLPA 安裝程式
│   └── test_xlit_rules.py      # RIME 驗證工具
└── release/                    # 發布目錄
    ├── rime_files/             # 打包後的 RIME 檔案
    ├── RIME_TLPA_Installer.exe # 安裝程式
    ├── RIME_TLPA_Validator.exe # 驗證工具
    ├── install.bat             # Windows 批次安裝腳本
    └── *.zip                   # 完整發布套件
```

## 使用方式

### 1. 建置發布套件

執行完整建置系統來創建發布套件：

```bash
python tools/build_system.py
```

這會：
- 清理舊的建置檔案
- 安裝必要的依賴套件
- 根據 `release-include.txt` 複製 RIME 檔案
- 打包 Python 腳本為 .exe 檔案
- 創建 Windows 安裝腳本
- 生成完整的發布 ZIP 套件

### 2. 安裝 RIME TLPA

有三種安裝方式：

#### 方式一：使用 GUI 安裝程式
```bash
.\release\RIME_TLPA_Installer.exe
```

#### 方式二：使用批次腳本
```bash
.\release\install.bat
```

#### 方式三：手動安裝
1. 將 `release\rime_files\*` 中的所有檔案複製到 `%APPDATA%\Rime\`
2. 備份原有的 `default.custom.yaml`
3. 在 RIME 小狼毫右鍵選擇「重新部署」

## 安裝程式功能

### 自動備份
- 自動備份現有的 `default.custom.yaml` 為 `default.custom.yaml.bak_時間戳`
- 確保使用者原有設定不會遺失

### 智能檔案複製
- 根據 `release-include.txt` 指定的檔案清單進行複製
- 自動檢測並處理檔案複製錯誤
- 提供詳細的複製進度和結果報告

### 自動部署
- 嘗試自動觸發 RIME 重新部署
- 如果自動部署失敗，提供手動部署指引

### 錯誤處理
- 檢查 RIME 是否已安裝
- 驗證所有必要檔案是否存在
- 提供清楚的錯誤訊息和解決建議

## release-include.txt 格式

這個檔案指定了要包含在發布套件中的 RIME 檔案：

```yaml
# 註解以 # 開頭
# 一行一個檔案名稱

# 鍵盤按鍵練習工具
kb_hong_im.schema.yaml
kb_ipa.schema.yaml

# 共用函式庫
rime.lua
keymap_piau_tian.yaml
lib_hau_suan_ji_tuann.yaml

# 支援台語拼音（TLPA）
tlpa_phing_im.schema.yaml
tlpa_hong_im.schema.yaml
tl_ji_khoo_peh_ue.dict.yaml

# 其他檔案...
```

## default.custom.yaml 處理

安裝程式會：

1. **備份現有檔案**：將使用者現有的 `default.custom.yaml` 備份
2. **複製新檔案**：從 `config/default.custom.yaml` 複製新的設定
3. **保留使用者設定**：備份檔案讓使用者可以手動合併設定

新的 `default.custom.yaml` 包含：
- RIME TLPA 相關的輸入方案清單
- 優化的設定參數
- 台語輸入法特有的配置

## 驗證工具

`RIME_TLPA_Validator.exe` 提供：
- 驗證 RIME schema 檔案的 xlit 規則正確性
- 檢查字符對映是否匹配
- 診斷常見的配置錯誤

## 完成的需求

✅ **指定打包檔案**：根據 `release-include.txt` 複製到 `~\AppData\Roaming\Rime\`

✅ **變更 RIME 輸入方案設定檔**：
1. 自動備份現有的 `default.custom.yaml` 為 `.bak` 檔案
2. 從 `config/` 目錄複製新的 `default.custom.yaml` 到 RIME 目錄