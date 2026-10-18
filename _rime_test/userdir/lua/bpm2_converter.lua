-- lua/bpm2_converter.lua
-- v0.1.0 (2026/6/2)：補齊高韻/箴韻韻母轉換
-- v0.1.0 (2026/5/17)：台語注音二式（BPM2）轉換模組
-- TLPA（台語音標）→ BPM2（台語注音二式）轉換
--
-- 聲母需對照轉換；韻母大部分相同，但有以下差異：
--   TLPA o  (高韻)   → BPM2 or   (如：ho5  → hor5)
--   TLPA oh (高韻入聲)→ BPM2 orh  (如：hoh4 → horh4, 由 or+h 組成)
--   TLPA om (箴韻)   → BPM2 oom  (如：hom1 → hoom1)
--   TLPA op (箴韻入聲)→ BPM2 oop  (如：hop4 → hoop4)
--
-- 使用方式：
--   local bpm2 = require("bpm2_converter")
--   print(bpm2.convert("tong1"))  -- "dong1"
--   print(bpm2.convert("ngoo5"))  -- "ngoo5"
--   print(bpm2.convert("ho5"))    -- "hor5"
--   print(bpm2.convert("lun2"))   -- "lun2"

local M = {}

-- ============================================================
-- TLPA 聲母 → BPM2 聲母 對照表
-- （依 100_閩南語聲韻調對映指引.md）
-- ============================================================
local BPM2_SIANN = {
    p   = "b",   ph  = "p",   b   = "bb",  m   = "m",
    t   = "d",   th  = "t",   n   = "n",   l   = "l",
    z   = "z",   c   = "c",   j   = "zz",  s   = "s",
    k   = "g",   kh  = "k",   g   = "gg",  ng  = "ng",
    h   = "h",
    -- 顎化聲母（介音 i 起頭之音節）
    zi  = "j",   ci  = "ch",  ji  = "jj",  si  = "sh",
}

-- ============================================================
-- TLPA 韻母 → BPM2 韻母 差異表
-- （其餘韻母與 TLPA 相同，僅列出有差異的）
-- ============================================================
local BPM2_UN = {
    -- 高韻：TLPA o / oh → BPM2 or / orh
    ["o"]   = "or",
    ["oh"]  = "orh",
    -- 箴韻：TLPA om / op → BPM2 oom / oop
    ["om"]  = "oom",
    ["op"]  = "oop",
}

--- TLPA → BPM2 轉換
-- 聲母依對照表轉換；高韻/箴韻韻母亦須轉換。
-- @param  tlpa  string  台語音標（如 "tong1", "ho5", "hom1"）
-- @return string  台語注音二式（如 "dong1", "hor5", "hoom1"）
function M.convert(tlpa)
    local conv = require("tlpa_converter")
    local parts = conv.split(tlpa)
    if not parts then return tlpa end
    local zero = (parts.siann == "\195\184" or parts.siann == "\195\152")
    local siann = parts.siann
    local un = parts.un
    -- 曾／出／入／時 + i 起頭韻母：z／c／j／s → zi／ci／ji／si，再對成 j／ch／jj／sh。
    -- 誌 TL zi3 應入庫 ji3。若存成 zi3，用戶詞典整詞編碼失敗，事誌不會留下。
    if not zero and un:sub(1, 1) == "i" then
        if siann == "z" then siann = "zi"
        elseif siann == "c" then siann = "ci"
        elseif siann == "j" then siann = "ji"
        elseif siann == "s" then siann = "si"
        end
    end
    local b2_siann = zero and "" or (BPM2_SIANN[siann] or siann)
    local b2_un    = BPM2_UN[un] or un
    return b2_siann .. b2_un .. parts.tiau
end

return M
