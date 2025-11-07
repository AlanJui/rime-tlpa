# convert_tlpa_to_bp_for_rime_dict.py 使用說明

## 程式功能

將【台語音標（TLPA+）】轉換成【台語注音二式（BP）】格式的 RIME 字典檔。

## 使用方式

### 基本語法
```bash
python convert_tlpa_to_bp_for_rime_dict.py [input_file] [output_file]
```

### 參數說明

- `input_file` (可選): 輸入檔案路徑
  - **預設值**: 專案根目錄下的 `tl_ji_khoo_peh_ue.dict.yaml`
  - 即: `.\tl_ji_khoo_peh_ue.dict.yaml`

- `output_file` (可選): 輸出檔案路徑
  - **預設值**: 專案根目錄下的 `bp_ji_khoo.dict.yaml`
  - 即: `.\bp_ji_khoo.dict.yaml`

## 使用範例

### 1. 使用預設檔案

```bash
cd tools
python convert_tlpa_to_bp_for_rime_dict.py
```

**結果**:

- 讀取: `C:\work\rime-tlpa\tl_ji_khoo_peh_ue.dict.yaml`
- 輸出: `C:\work\rime-tlpa\bp_ji_khoo.dict.yaml`

### 2. 指定輸入檔案，使用預設輸出

```bash
cd tools
python convert_tlpa_to_bp_for_rime_dict.py ../my_input.dict.yaml
```

**結果**:

- 讀取: `../my_input.dict.yaml`
- 輸出: `C:\work\rime-tlpa\bp_ji_khoo.dict.yaml`

### 3. 指定輸入和輸出檔案

```bash
cd tools
python convert_tlpa_to_bp_for_rime_dict.py ../input.dict.yaml ../output.dict.yaml
```

**結果**:

- 讀取: `../input.dict.yaml`
- 輸出: `../output.dict.yaml`

## 轉換範例

### 零聲母處理

| 台語音標 (TLPA) | 閩拼 (BP) | 說明 |
|-----------------|-----------|------|
| `i1` | `yi1` | 伊 |
| `iong2` | `yong2` | 楊 |
| `u3` | `wu3` | 有 |
| `uan2` | `wan2` | 彎 |

### 有聲母處理

| 台語音標 (TLPA) | 閩拼 (BP) | 說明 |
|-----------------|-----------|------|
| `tsiann1` | `zian1` | 正 |
| `siok8` | `siok8` | 俗 |
| `kong1` | `gong1` | 公 |

## 執行輸出

程式執行時會顯示：

```Bash
輸入檔案：C:\work\rime-tlpa\tl_ji_khoo_peh_ue.dict.yaml
輸出檔案：C:\work\rime-tlpa\bp_ji_khoo.dict.yaml
轉換完成，結果已寫入 C:\work\rime-tlpa\bp_ji_khoo.dict.yaml
```

## 錯誤處理

如果輸入檔案不存在，會顯示錯誤訊息並退出：

```Bash
錯誤：輸入檔案不存在 - [檔案路徑]
```

## 注意事項

1. 程式會自動檢測專案根目錄（工具位於 `tools/` 子目錄）
2. 輸出檔案如果已存在會被覆寫
3. 字典檔案的 `name` 欄位會自動更改為 `bp_ji_khoo`
4. 程式使用 UTF-8 編碼處理檔案