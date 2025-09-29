# Windows 11 安裝小狼毫輸入法操作指引

## 一、簡介
小狼毫（Weasel）是 **RIME 輸入法引擎** 在 Windows 平台上的版本。它支援多種輸入方案，如注音、拼音、倉頡、台語拼音等，並能高度自訂。本文將指引您在 **Windows 11** 系統中安裝與設定小狼毫輸入法。

---

## 二、下載安裝檔

1. 開啟瀏覽器，進入官方下載頁：
   [Rime 官方下載頁 (GitHub Releases)](https://github.com/rime/weasel/releases)

![下載小狼毫輸入法](https://github.com/AlanJui/rime-tlpa/blob/main/docs/static/img/Weasel_Install_001.png)

2. 找到最新版本，例如：
   `weasel-x.x.x-installer.exe`
   （檔名中的 `x.x.x` 代表版本號）

3. 點擊下載並存到電腦中（建議放在「下載」資料夾）。

---

## 三、安裝步驟

1. **執行安裝檔**
   在下載的檔案上 **雙擊滑鼠左鍵**。

![下載小狼毫輸入法](https://github.com/AlanJui/rime-tlpa/blob/main/docs/static/img/Weasel_Install_002.png)

2. **允許安裝**
   若 Windows 跳出「是否允許此應用對您的裝置進行變更？」，請選擇 **是**。

3. **安裝選項**
   - 建議保持預設設定，點擊 **下一步**。
   - 勾選「安裝完成後立即部署」選項（Deployment），方便快速啟用。

4. **完成安裝**
   點擊 **完成**，小狼毫即安裝至系統。

---

## 四、啟用小狼毫輸入法

1. **打開設定**
   `開始功能表 → 設定 → 時間與語言 → 語言與地區`

![進入設定功能](https://github.com/AlanJui/rime-tlpa/blob/main/docs/static/img/Weasel_Install_003.png)

2. **選擇語言**
   在「慣用語言」中找到「繁體中文（台灣）」或「簡體中文（中華人民共和國）」。

![在繁體中文輸入新增小狼毫輸入法](https://github.com/AlanJui/rime-tlpa/blob/main/docs/static/img/Weasel_Install_004.png)

3. **新增輸入法**
   - 點選 **選項**
   - 在輸入法清單中點選 **新增鍵盤**
   - 選擇 **小狼毫輸入法**（Weasel Input Method）

![新增小狼毫鍵盤](https://github.com/AlanJui/rime-tlpa/blob/main/docs/static/img/Weasel_Install_005.png)

4. **切換輸入法**
   - 使用 **Win + Space** 或 **Ctrl + Shift** 即可切換輸入法。
   - 輸入法列會顯示「中」或「EN」，切換時可見「小狼毫」標示。

![新增小狼毫鍵盤](https://github.com/AlanJui/rime-tlpa/blob/main/docs/static/img/Weasel_Install_006.png)

---

## 五、基本操作

- **切換中英文**：
  `Shift` 或 `Ctrl + Space`

- **候選字選擇**：
  使用 **數字鍵（1-9）** 選擇候選字。

- **設定選單**：
  在輸入狀態下，按 **Ctrl + `（鍵盤左上角 Esc 下方的鍵）**，即可開啟設定選單。

![在小狼毫切換輸入法](https://github.com/AlanJui/rime-tlpa/blob/main/docs/static/img/Weasel_Install_008.png)

---

## 六、輸入法自訂

小狼毫的一大特色是可以透過 **配置檔案（YAML）** 來自訂輸入方案：

1. 找到配置資料夾：
   預設路徑：
   ```
   %AppData%\Rime
   ```

![小狼毫設定檔目錄路徑](https://github.com/AlanJui/rime-tlpa/blob/main/docs/static/img/Weasel_Install_007.png)

2. 編輯檔案：
   - `default.custom.yaml` → 系統設定
   - `weasel.custom.yaml` → 外觀與鍵盤配置
   - 各語言方案（如 `bopomofo.schema.yaml`、`pinyin.schema.yaml`）

3. 修改完成後，使用 **「重新部署」**（Deploy）讓設定生效。
   方式：
   - 右鍵點擊系統輸入法圖示 → 選擇 **「重新部署」**

---

## 七、常見問題

1. **輸入法未出現？**
   - 請確認「設定 → 語言與地區 → 輸入法」是否已新增小狼毫。
   - 若無，請重新安裝。

2. **無法切換輸入法？**
   - 確認熱鍵是否衝突，可在「設定 → 時間與語言 → 鍵盤 → 進階鍵盤設定」中調整。

3. **修改設定檔無效？**
   - 確認已執行「重新部署」。
   - YAML 語法必須正確，注意縮排與冒號格式。

---

## 八、結語

透過以上步驟，您已能在 Windows 11 系統中安裝並啟用小狼毫輸入法。小狼毫除了支援多種語言方案，還能透過 YAML 檔案進行高度自訂，非常適合需要繁體中文拼音、注音或台語拼音輸入的使用者。
