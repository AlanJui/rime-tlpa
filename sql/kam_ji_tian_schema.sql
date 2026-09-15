-- 甘字典漢字庫 Schema
-- 參考：docs/420_甘字典漢字庫指引.md

CREATE TABLE IF NOT EXISTS 漢字庫 (
    識別號  INTEGER PRIMARY KEY AUTOINCREMENT,
    漢字   TEXT    NOT NULL,
    台羅音標 TEXT    NOT NULL,
    常用度  REAL    DEFAULT 0.1,
    摘要說明 TEXT    DEFAULT 'NA',
    時間戳記 TEXT    DEFAULT (DATETIME('now', 'localtime'))
                 NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_漢字_台羅音標 ON 漢字庫 (
    漢字,
    台羅音標
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
