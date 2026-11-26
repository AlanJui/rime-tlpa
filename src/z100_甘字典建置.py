import os
import sqlite3

import pandas as pd

# 檔案路徑設定
csv_file = "ChhoeTaigi_KamJitian.csv"
db_file = "Kam_Ji_Tian.db"
json_file = "Kam_Ji_Tian.json"

# 1. 檢查並讀取本地 CSV 檔案
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"找不到檔案：{csv_file}，請確認檔案是否放在與此腳本相同的資料夾中。")

# 強制以字串讀取並將空值填補為空字串，避免頁碼或數字調被轉為浮點數
df = pd.read_csv(csv_file, dtype=str).fillna("")

# 2. 篩選常用核心欄位（自動檢查欄位是否存在，確保腳本穩定執行）
target_cols = [
    "DictWordID",
    "HanLoTaibunPoj",
    "KipUnicode",
    "KipInput",
    "PojUnicode",
    "PojInput",
    "KaisoehHanLoPoj",
    "PageNumber"
]
available_cols = [col for col in target_cols if col in df.columns]
df_filtered = df[available_cols]

# 3. 匯出為 JSON 格式（若不需要可將此行註解掉）
df_filtered.to_json(json_file, orient="records", force_ascii=False, indent=2)

# 4. 匯出為 SQLite3 資料庫 (Kam_Ji_Tian.db)
conn = sqlite3.connect(db_file)
df_filtered.to_sql("entries", conn, if_exists="replace", index=False)

# 5. 建立查詢索引以加速檢索
cursor = conn.cursor()
if "HanLoTaibunPoj" in available_cols:
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_hanlo ON entries (HanLoTaibunPoj);")
if "KipInput" in available_cols:
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_kip ON entries (KipInput);")
if "PojInput" in available_cols:
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_poj ON entries (PojInput);")

conn.commit()
conn.close()

print(f"轉換完成！共匯入 {len(df_filtered)} 筆資料至 {db_file}（資料表名稱：entries）。")
