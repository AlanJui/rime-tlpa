-- 已改名：請改用 sql/ji_tian_schema.sql
-- 本檔保留相同 DDL，以利舊路徑相容。

CREATE TABLE IF NOT EXISTS 漢字庫 (
    識別號  INTEGER PRIMARY KEY AUTOINCREMENT,
    漢字   TEXT    NOT NULL,
    漢字標音 TEXT    NOT NULL,
    常用度  REAL    DEFAULT 0.1,
    摘要說明 TEXT    DEFAULT 'NA',
    時間戳記 TEXT    DEFAULT (DATETIME('now', 'localtime'))
                 NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_漢字_漢字標音 ON 漢字庫 (
    漢字,
    漢字標音
);

CREATE TRIGGER IF NOT EXISTS trg_ensure_default_summary
         AFTER INSERT
            ON 漢字庫
          WHEN NEW.摘要說明 IS NULL
BEGIN
    UPDATE 漢字庫
       SET 摘要說明 = 'N/A'
     WHERE rowid = NEW.rowid;
END;
