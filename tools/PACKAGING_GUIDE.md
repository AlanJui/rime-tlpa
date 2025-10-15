# RIME 工具打包指南

## 使用 PyInstaller 創建 .exe 檔案

### 1. 安裝 PyInstaller

```bash
pip install pyinstaller
```

### 2. 基本打包命令

#### 打包 test_xlit_rules.py
```bash
# 產生單一 .exe 檔案
pyinstaller --onefile tools/test_xlit_rules.py

# 產生帶控制台視窗的 .exe
pyinstaller --onefile --console tools/test_xlit_rules.py

# 產生無控制台視窗的 .exe (適用於 GUI 應用)
pyinstaller --onefile --windowed tools/test_xlit_rules.py
```

### 3. 進階選項

```bash
# 自訂輸出檔名和圖示
pyinstaller --onefile \
           --name "RIME_TLPA_Validator" \
           --icon="icon.ico" \
           --console \
           tools/test_xlit_rules.py

# 包含額外的資料檔案
pyinstaller --onefile \
           --add-data "*.yaml;." \
           --add-data "docs;docs" \
           tools/test_xlit_rules.py
```

### 4. 使用 spec 檔案進行詳細配置

創建 `rime_tools.spec` 檔案來自訂打包設定。

### 5. 輸出位置

編譯完成後，.exe 檔案會在：
- `dist/` 目錄中
- 檔名為腳本名稱或 `--name` 指定的名稱

### 6. 常見問題解決

#### 缺少模組錯誤
```bash
# 手動指定隱藏匯入
pyinstaller --onefile --hidden-import=module_name script.py
```

#### 檔案大小過大
```bash
# 排除不必要的套件
pyinstaller --onefile --exclude-module=tkinter script.py
```

### 7. 測試打包結果

1. 在沒有安裝 Python 的電腦上測試
2. 檢查所有功能是否正常
3. 確認資料檔案是否正確包含

## Auto-py-to-exe (GUI 方式)

如果偏好圖形界面：

```bash
pip install auto-py-to-exe
auto-py-to-exe
```

然後在瀏覽器中進行可視化配置。