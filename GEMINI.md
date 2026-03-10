# Gemini CLI 專案指令集 (GEMINI.md)

## 專案定位

本專案為 **RIME-TLPA 台語輸入法整合方案**，旨在提供跨平台的台語輸入支援（包含 TLPA、BP、方音符號、十五音等體系）。專案核心由 Rime 方案 (.schema.yaml)、字典 (.dict.yaml)、Lua 擴充 (rime.lua) 以及 Python 字典轉換工具構成。

## 關鍵路徑

- **Rime 方案檔**: 根目錄下的 `*.schema.yaml`
- **字典檔**: 根目錄下的 `*.dict.yaml`（注意：大規模修改需透過 `tools/` 中的 Python 工具處理）
- **Lua 擴充**: `rime.lua` (Rime 的動態邏輯)
- **轉換工具**: `tools/` 與 `src/` (處理音標系統轉換，如 TLPA -> BP)
- **部署腳本**: `deploy_rime_tlpa.ps1` (將文件同步至 Rime 使用者目錄)

## 開發規範

1. **YAML 格式**: Rime 的 YAML 檔對縮排極為敏感，修改時必須保持原本的縮排風格。
2. **字典維護**:
   - 避免直接手動修改大型字典檔 (`tl_han_ji_khoo.dict.yaml`)。
   - 偏好修改 Excel 資料源或執行 `tools/` 下的轉換腳本來產生字典。
3. **編碼要求**: 所有的 `.yaml`, `.dict.yaml`, `.lua` 檔案必須使用 **UTF-8 (無 BOM)** 編碼。
4. **測試驗證**: 修改方案後，必須執行 `deploy_rime_tlpa.ps1` 並重啟 Rime 服務 (`tools/restart_rime_service.bat`) 以進行驗證。
5. **版本控制**: 不得隨意提交 `build/` 目錄或 Rime 部署產生的二進位快取檔 (`*.bin`)。
6. 註解保留原則 (Critical): 嚴禁刪除或簡化原有的註解。註解中包含 Rime 特性記錄、已知 Bug 避讓（坑洞）及版本相容性說明，修改程式碼時必須完整保留。

## 常用指令與自動化

- **重啟 RIME**: `.\tools\restart_rime_service.bat`
- **本地部署測試**: `powershell -File .\deploy_rime_tlpa.ps1`
- **建置安裝檔**: 參考 `tools/build_installer.py` 與 `*.spec` 檔案。

## AI 指令行為準則 (Mandates)

- **嚴禁事項**: 未經確認不得修改 `_archived/` 內的任何檔案。
- 註解完整性: 修改 .yaml 或 .lua 時，禁止為了追求程式碼簡潔而抹除原有註解。若必須重構受影響的邏輯，應將原註解遷移至新邏輯旁。
- **字典變更**: 當被要求修改字典內容時，應先檢查 `tools/` 中是否有對應的 Python 腳本可以自動化處理，而非直接編輯 `.dict.yaml`。
- **Lua 修改**: 修改 `rime.lua` 時，需考慮跨平台相容性 (Windows, macOS, Linux)。
