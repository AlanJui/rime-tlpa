-- lua/bpm2_converter.lua
-- V0.1.0 (2026/5/17)：台語注音二式（BPM2）轉換模組
-- TLPA（台語音標）→ BPM2（台語注音二式）轉換
--
-- 韻母與調號與 TLPA 完全相同，只有聲母需對照轉換。
--
-- 使用方式：
--   local bpm2 = require("bpm2_converter")
--   print(bpm2.convert("tong1"))  -- "dong1"
--   print(bpm2.convert("ngoo5"))  -- "ngoo5"
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

--- TLPA → BPM2 轉換
-- 韻母與調號與 TLPA 相同，只轉換聲母部分。
-- @param  tlpa  string  台語音標（如 "tong1", "ngoo5", "lun2"）
-- @return string  台語注音二式（如 "dong1", "ngoo5", "lun2"）
function M.convert(tlpa)
    local conv = require("tlpa_converter")
    local parts = conv.split(tlpa)
    if not parts then return tlpa end
    local zero = (parts.siann == "\195\184" or parts.siann == "\195\152")
    local b2_siann = zero and "" or (BPM2_SIANN[parts.siann] or parts.siann)
    return b2_siann .. parts.un .. parts.tiau
end

return M
