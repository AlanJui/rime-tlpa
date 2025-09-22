
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
-- 注意：本功能須配合 schema 的 key_binder，將 Enter、Ctrl+Enter、Shift+Enter、Ctrl+Shift+Enter 綁定到 lua_aux_commit
-- 例如：
--   "key_binder/bindings/accept": "lua_aux_commit"
--   "key_binder/bindings/accept_next": "lua_aux_commit"
--   "key_binder/bindings/accept_previous": "lua_aux_commit"
--   "key_binder/bindings/accept_alternate": "lua_aux_commit"
------------------------------------------------------------------------------------------
-- 另外，請在 schema 的 switches 中加入「supers_tone」選項
-- 例如：
--  "switches": [
--    { "name": "supers_tone", "reset": 1, "states": ["上標", "一般"] }
--  ]
------------------------------------------------------------------------------------------
-- 這樣 Shift+Enter 輸出時，會依「supers_tone」選項，決定輸出「上標」或「一般數字」
------------------------------------------------------------------------------------------
-- 【程式處理指引】：
-- 能從候選註解（不論是原本「配對顯示」或你剛重排後的「左 TLPA、右注音」）解析出所有音節。

-- 沒候選單時，改從 inline 取資料：TLPA 取 ctx.input（自動依 ' 切音節）、注音取 ctx:get_script_text()（會是像 ㄅ'ㄙ，自動拆成 ㄅ、ㄙ）。

-- Enter：輸出 TLPA（多音節用 ' 連接）
-- Ctrl+Enter：輸出注音（保留聲調符號，音節間一格空白）
-- Shift+Enter：依 supers_tone 輸出上標或數字（每個音節各自轉換，再以空白連接）
-- Ctrl+Shift+Enter：輸出「候選雙欄格式」：〔tlpa1〕 〔tlpa2〕 … 【bpmf1】 【bpmf2】 …
------------------------------------------------------------------------------------------

-- ========= 連續輸入版：解析候選註解 / inline，並依快捷鍵提交 =========
-- 抓所有 〔...〕 與 【...】（支援你重排後的「雙欄」與原始「配對」）
local function parse_comment_all(comment)
  if not comment or comment == "" then return {}, {} end
  local tlpa, zh = {}, {}
  -- 先抓所有 〔...〕 / 【...】（應付「雙欄」）
  for t in comment:gmatch("〔(.-)〕") do table.insert(tlpa, t) end
  for z in comment:gmatch("【(.-)】") do table.insert(zh, z) end
  -- 若抓不到，嘗試抓「一對一對」：〔...〕【...】〔...〕【...】
  if #tlpa == 0 or #zh == 0 then
    for L, R in comment:gmatch("〔(.-)〕%s*【(.-)】") do
      table.insert(tlpa, L); table.insert(zh, R)
    end
  end
  return tlpa, zh
end

-- 從 inline 抓多音節：TLPA 用 ' 拆；注音用 ' 或空白拆，並去掉多餘分隔
local function split_inline(ctx)
  local tl = ctx.input or ""
  local bp = (ctx.get_script_text and ctx:get_script_text()) or ""
  local tl_list, bp_list = {}, {}
  if tl ~= "" then
    for seg in tl:gmatch("[^']+") do table.insert(tl_list, seg) end
  end
  if bp ~= "" then
    -- 先把 連續輸入用的 ' 變空白，再依空白切；並去掉殘留單引號
    bp = bp:gsub("'", " ")
    for seg in bp:gmatch("%S+") do
      seg = seg:gsub("'", "")
      table.insert(bp_list, seg)
    end
    -- 某些佈景會用「ㄅ'ㄙ」但沒有空白，補救：直接逐段抓「注音字母+調號」
    if #bp_list <= 1 and bp:find("'", 1, true) then
      for seg in bp:gmatch("[^']+") do
        seg = seg:gsub("%s+", "")
        if #seg > 0 then table.insert(bp_list, seg) end
      end
    end
  end
  return tl_list, bp_list
end

-- 去掉注音的聲調記號
local TONE_MARKS = "[ˊˋ˪˫˙]"
local function strip_bpmf_marks_one(s) return s and s:gsub(TONE_MARKS, "") or s end

-- 數字 -> 上標數字
local supers_digit = { ["1"]="¹", ["2"]="²", ["3"]="³", ["4"]="⁴",
                       ["5"]="⁵", ["6"]="⁶", ["7"]="⁷", ["8"]="⁸" }

-- 從 TLPA 取調號數字（最後一碼 1-8）
local function tone_from_tlpa(tl)
  return tl and tl:match("([1-8])$") or nil
end

-- 依 TLPA 的調號，把注音換成「上標數字調」
-- 例：ㄍㄧㆰ + 1 → ㄍㄧㆰ¹
local function bpmf_with_supers_by_tl(bpmf, tlpa)
  if not bpmf then return nil end
  local base = strip_bpmf_marks_one(bpmf)
  local t = tone_from_tlpa(tlpa)
  return t and (base .. (supers_digit[t] or "")) or base
end

-- 依 TLPA 的調號，把注音換成「尾隨數字調」
-- 例：ㄍㄧㆰ + 1 → ㄍㄧㆰ1
local function bpmf_with_digit_by_tl(bpmf, tlpa)
  if not bpmf then return nil end
  local base = strip_bpmf_marks_one(bpmf)
  local t = tone_from_tlpa(tlpa)
  return t and (base .. t) or base
end

-- 將一列音節做轉換（map）後，用空白接回
local function map_join(list, f)  -- f(elem, idx) -> string
  local out = {}
  for i, v in ipairs(list) do out[i] = f(v, i) or "" end
  return table.concat(out, " ")
end

-- 從「候選」拿多音節；失敗就退回 inline
local function get_multiforms(env)
  local ctx = env.engine.context
  local tl_list, bp_list = {}, {}

  if ctx:has_menu() then
    local cand = ctx:get_selected_candidate()
    if cand then
      tl_list, bp_list = parse_comment_all(cand.comment or "")
    end
  end
  if #tl_list == 0 and #bp_list == 0 then
    tl_list, bp_list = split_inline(ctx)
  end
  -- 正規化：長度對齊（若其中一邊空，就容忍不齊）
  return tl_list, bp_list
end

-- 快捷鍵規範化
local function norm_repr(r)
  r = r:gsub("^Release%+", ""):gsub("^ISO_Enter$", "Return")
  return r:lower()
end

-- ============= 主函式：aux_commit（多音節友善） =============
function aux_commit(key, env)
  local ctx = env.engine.context
  local r = norm_repr(key:repr())

  local want_tlpa   = (r == "return")                 -- Enter
  local want_bpmf   = (r == "control+return")         -- Ctrl+Enter
  local want_shift  = (r == "shift+return")           -- Shift+Enter（上標/數字）
  local want_both   = (r == "control+shift+return")   -- Ctrl+Shift+Enter（雙欄）

  if not (want_tlpa or want_bpmf or want_shift or want_both) then return 2 end

  local tl_list, bp_list = get_multiforms(env)

  -- Enter：TLPA（★不再用 '，直接無分隔串接）
  if want_tlpa and #tl_list > 0 then
    env.engine:commit_text(table.concat(tl_list, " "))  -- ← 由【空白】取代 "'"
    ctx:clear(); return 1
  end

  -- Ctrl+Enter：注音（保留符號；音節間一格空白）
  if want_bpmf and #bp_list > 0 then
    env.engine:commit_text(table.concat(bp_list, " "))
    ctx:clear(); return 1
  end

  -- Shift+Enter：依 supers_tone 選「上標」或「尾隨數字」
  if want_shift and #bp_list > 0 then
    local use_supers = ctx:get_option("supers_tone")
    local out
    if use_supers then
      out = map_join(bp_list, function(x, i) return bpmf_with_supers_by_tl(x, tl_list[i]) end)
    else
      out = map_join(bp_list, function(x, i) return bpmf_with_digit_by_tl(x, tl_list[i]) end)
    end
    if out and #out > 0 then env.engine:commit_text(out); ctx:clear(); return 1 end
  end

  -- Ctrl+Shift+Enter：候選雙欄格式
  if want_both and (#tl_list > 0 or #bp_list > 0) then
    local left = ""
    if #tl_list > 0 then left = "〔" .. table.concat(tl_list, "〕 〔") .. "〕" end
    local right = ""
    if #bp_list > 0 then right = "  【" .. table.concat(bp_list, "】 【") .. "】" end
    local out = (left .. right):gsub("^%s+", "")
    if #out > 0 then env.engine:commit_text(out); ctx:clear(); return 1 end
  end

  return 2
end