-----------------------------------------------------------------------------------------
-- jump_select：令【候選字清單】中的【標示游標】移動，提供：到頂端/到中間/到底端的三種快捷鍵
-----------------------------------------------------------------------------------------
-- 固定對齊「畫面 5 行」：頂=Home；中=Home+Down×2；底=Home+Down×4
-- 快捷鍵：Ctrl+/（頂）、Ctrl+.（中）、Ctrl+,（底）
-- 注意：F20/F24 是代理鍵，會在 schema 的 key_binder 被翻成 Home/Down
-----------------------------------------------------------------------------------------
local function press_key_n(env, key_name, n)
  for _ = 1, n do env.engine:process_key(KeyEvent(key_name)) end
end

local function norm(r)
  if r:sub(1,8) == "Release+" then return r:sub(9) end
  return r
end

function jump_select(key, env)
  local ctx = env.engine.context

  -- 若【候選字清單】尚未展開，終止處理
  if not ctx:has_menu() then return 2 end

  -- 取得【輸入列】的【按鍵】
  local r = norm(key:repr())

  -- 若【按鍵】為代理鍵：【F20】或【F24】，則終止處理
  -- 避免自觸發（忽略我們送出的代理鍵）
  if r == "F20" or r == "F24" then return 2 end

  -- 候選字視窗中游標移動快捷鍵：頂端/中位/底端
  local go_top    = (r == "Control+comma")  or (r == "Control+,")
  local go_middle = (r == "Control+period") or (r == "Control+.")
  local go_bottom = (r == "Control+slash")

  -- 若【按鍵】不是【候選字清單】的快捷鍵，終止處理
  if not (go_top or go_middle or go_bottom) then return 2 end

  -- 為後續處理之便，先將【標示游標】移到頂端
  -- 送出代理鍵：F20（Home）
  env.engine:process_key(KeyEvent("F20"))

  -- 計算【標示游標】的【往下移動次數】
  -- 移到：中間=2、底端=4（頂端=0）
  local steps = go_middle and 2 or (go_bottom and 4 or 0)
  -- 透過代理鍵：F24（Down）及上述所得之【往下移動次數】，完成【標示游標】之移動
  if steps > 0 then press_key_n(env, "F24", steps) end  -- F24 → Down
  return 1
end

------------------------------------------------------------------------------------------
-- aux_commit：提供輸入法的【輸出】，可選擇
-- （1）漢字、（2）【羅馬拼音字母】、（3）【方音符號】、（4）【帶調號之方音符號】、
-- （5）候選字清單顯示結果：【羅馬拼音字母】＋【方音符號】一起輸出（候選字清單的顯示結果）
------------------------------------------------------------------------------------------
-- 扶：〔hu5〕  【ㄏㄨˊ】
-- Space → 漢字
-- Enter → 羅馬拼音字母：hu5
-- Ctrl+Enter → 方音符號：ㄏㄨˊ
-- Shift+Enter → 帶調號方音符號：ㄏㄨ5
-- Ctrl+Shift+Enter → 候選字清單顯示結果：〔hu5〕  【ㄏㄨˊ】
------------------------------------------------------------------------------------------

local function get_forms_from_candidate(env)
  local ctx = env.engine.context
  local cand = ctx:get_selected_candidate()
  if not cand then return nil end
  local c = cand.comment or ""
  local tlpa = c:match("〔%s*([%w_]+)%s*〕")
  local bpmf = c:match("【%s*([^】]+)%s*】")
  return { tlpa = tlpa, bpmf = bpmf }
end

local function get_inline_forms(env)
  local ctx = env.engine.context
  local tlpa  = ctx.input or ""
  local bpmf  = ""
  if ctx.get_script_text then bpmf = ctx:get_script_text() or "" end
  if tlpa == "" then tlpa = nil end
  if bpmf == "" then bpmf = nil end
  return { tlpa = tlpa, bpmf = bpmf }
end

local TONE_MARKS = "[ˊˋ˪˫˙]"
local function strip_bpmf_marks(bpmf)
  return bpmf and bpmf:gsub(TONE_MARKS, "") or bpmf
end

-- 上標數字
local supers_map = {
  ["ˊ"]="⁵",
  ["ˋ"]="²",
  ["˪"]="³",
  ["˫"]="⁷",
  ["˙"]="⁸"
}

-- 上標數字（將 ˊˋ˪˫˙ 換成 ⁵²³⁷⁸，接上 TLPA 的尾碼數字）
local function bpmf_to_supers(bpmf, tlpa)
  if not bpmf then return nil end
  local out, had = bpmf, false
  for mark, sup in pairs(supers_map) do
    if out:find(mark, 1, true) then out = out:gsub(mark, sup); had = true end
  end
  -- 若完全沒符號而且你想依 TLPA 自動補上標，這裡可加；目前不強制補。
  return out
end

-- 一般數字（去掉 ˊˋ˪˫˙，接上 TLPA 的尾碼數字）
local function bpmf_to_digit(bpmf, tlpa)
  if not bpmf then return nil end
  local base = strip_bpmf_marks(bpmf) or bpmf
  local tone = tlpa and tlpa:match("(%d)$") or nil
  if tone and #tone == 1 then return base .. tone else return base end
end

local function norm_repr(r)
  r = r:gsub("^Release%+", ""):gsub("^ISO_Enter$", "Return")
  return r:lower()
end

-- ========= 主處理器（含選項切換的 Shift+Enter） =========
function aux_commit(key, env)
  local ctx = env.engine.context
  local r = norm_repr(key:repr())

  local want_tlpa   = (r == "return")                 -- Enter
  local want_bpmf   = (r == "control+return")         -- Ctrl+Enter
  local want_shift  = (r == "shift+return")           -- Shift+Enter（依開關輸出）
  local want_both   = (r == "control+shift+return")   -- Ctrl+Shift+Enter（兩段一起）

  if not (want_tlpa or want_bpmf or want_shift or want_both) then return 2 end

  -- 1) 候選清單優先
  local tlpa, bpmf
  if ctx:has_menu() then
    local f = get_forms_from_candidate(env)
    if f then tlpa, bpmf = f.tlpa, f.bpmf end
  end
  -- 2) fallback：inline 組字
  if (not tlpa or not bpmf) then
    local g = get_inline_forms(env)
    tlpa = tlpa or g.tlpa
    bpmf = bpmf or g.bpmf
  end

  -- 3) 按鍵行為
  if want_tlpa and tlpa then
    env.engine:commit_text(tlpa); ctx:clear(); return 1
  end
  if want_bpmf and bpmf then
    env.engine:commit_text(bpmf); ctx:clear(); return 1
  end
  if want_shift and bpmf then
    -- ⬇️ 這裡依 option「supers_tone」切換上標／一般數字
    local use_supers = ctx:get_option("supers_tone")
    local out = use_supers and bpmf_to_supers(bpmf, tlpa) or bpmf_to_digit(bpmf, tlpa)
    if out and #out > 0 then env.engine:commit_text(out); ctx:clear(); return 1 end
  end
  if want_both and (tlpa or bpmf) then
    local left  = tlpa and ("〔" .. tlpa .. "〕") or ""
    local right = bpmf and (" 【" .. bpmf .. "】") or ""
    local out = (left .. right):gsub("^%s+", "")
    if #out > 0 then env.engine:commit_text(out); ctx:clear(); return 1 end
  end

  return 2
end

------------------------------------------------------------------------------------------
-- 在候選註解前加上模式標籤：〔上標〕或〔一般〕
------------------------------------------------------------------------------------------
function supers_indicator(input, env)
  local on = env.engine.context:get_option("supers_tone")
  local tag = on and "〔上標〕 " or "〔一般〕 "
  for cand in input:iter() do
    -- 生成新的候選（不改動 text / segment）
    local c = cand:get_genuine()
    local new = Candidate(cand.type, cand.start, cand._end, cand.text,
                          tag .. (cand.comment or ""))
    -- 保留原本的屬性
    new.preedit = cand.preedit
    yield(new)
  end
end

-----------------------------------------------------------------------
-- filter Debug Tools
-----------------------------------------------------------------------
-- 驗證 FILTER　的觸發能被 RIME 攔截：不管候選內容是什麼，前面一律加上 [LUA] 標記
function force_mark_filter(input, env)
  for cand in input:iter() do
    local old = cand.comment or ""
    local nc = Candidate(cand.type, cand.start, cand._end, cand.text, "[LUA] " .. old)
    nc.quality = cand.quality
    yield(nc)
  end
end

-- 最小測試：僅在 comment 後面加 " [OK]"，不重排不改 text
-- 預期：
-- (1)注音輸入列仍是【ㄅ'ㄙ】
-- (2)候選照常彈出
-- (3)註解末尾出現 [OK]
function append_ok_filter(input, env)
  for cand in input:iter() do
    local old = cand.comment or ""
    local nc = cand:clone()         -- 關鍵：clone 保留 preedit/屬性
    nc.comment = old .. " [OK]"
    yield(nc)
  end
end

--------------------------------------------------------------------------
-- reformat_comment_filter：重排候選註解中的羅馬拼音與注音符號
--------------------------------------------------------------------------
-- 為處理【連續輸入】時，【候選字清單】中漢字的【羅馬拼音字母】、【注音符號】亦能正確顯示。
-- 輸入法自【拼音/注音輸入列】接收：羅馬拼音字母/注音符號後，在【候選字清單】的顯示，格式為：
-- 〔羅馬字母1〕 【注音符號1】  〔羅馬字母2〕 【注音符號2】 …
-- 透過 Lua filter: reformat_comment_filter 重排成：
-- 〔羅馬字母1〕 〔羅馬字母2〕 …  【注音符號1】 【注音符號2】 …
--------------------------------------------------------------------------

local function regroup_pairs_safe(s)
  if type(s) ~= "string" or s == "" then return s end
  local tlpa, zh = {}, {}

  -- 抓所有 〔...〕（最小擷取）
  for t in s:gmatch("〔(.-)〕") do
    table.insert(tlpa, t)
  end

  -- 抓所有 【...】（最小擷取）
  for z in s:gmatch("【(.-)】") do
    table.insert(zh, z)
  end

  if #tlpa >= 2 and #tlpa == #zh then
    return "〔" .. table.concat(tlpa, "〕 〔") .. "〕"
           .. "  "
           .. "【" .. table.concat(zh, "】 【") .. "】"
  end
  return s
end

function reformat_comment_filter(input, env)
  for cand in input:iter() do
    local old = cand.comment or ""
    local new = regroup_pairs_safe(old)

    if new ~= old then
      -- 關鍵：跟你現有的 supers_indicator 一樣的做法
      local c = cand:get_genuine()
      local nc = Candidate(c.type, c.start, c._end, c.text, new)
      -- 保留原來資訊，避免 preedit/彈窗異常
      nc.preedit  = cand.preedit
      nc.quality  = cand.quality
      -- 如你有自訂的屬性，也可在此補帶
      yield(nc)
    else
      yield(cand)
    end
  end
end

-----------------------------------------------------------------------