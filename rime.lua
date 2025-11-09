-- RIME API 依賴於運行時環境，無需顯式引入

---@diagnostic disable: undefined-global

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

-- ========= 解析候選註解 / inline 的多音節工具 =========

-- 從候選註解抓所有 〔...〕 與 【...】（相容你重排後的「雙欄」與原始「配對」）
local function parse_comment_all(comment)
  if not comment or comment == "" then return {}, {} end
  local tlpa, zh = {}, {}
  -- 抓所有 TLPA
  for t in comment:gmatch("〔(.-)〕") do table.insert(tlpa, t) end
  -- 抓所有注音
  for z in comment:gmatch("【(.-)】") do table.insert(zh, z) end
  -- 若抓不到，再試「一對一對」的樣式
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
    bp = bp:gsub("'", " ")  -- 將連續輸入分隔符號轉空白
    for seg in bp:gmatch("%S+") do
      seg = seg:gsub("'", "")
      table.insert(bp_list, seg)
    end
    -- 若仍只得到一段但原始含 '，再保底拆
    if #bp_list <= 1 and bp:find("'", 1, true) then
      for seg in bp:gmatch("[^']+") do
        seg = seg:gsub("%s+", "")
        if #seg > 0 then table.insert(bp_list, seg) end
      end
    end
  end
  return tl_list, bp_list
end

-- ========== 注音聲調處理 ==========
local TONE_MARKS = "[ˊˋ˪˫˙]"
local function strip_bpmf_marks_one(s) return s and s:gsub(TONE_MARKS, "") or s end

-- 使用【上標數字】標示聲調之【調號】值
local supers_digit = { ["1"]="¹", ["2"]="²", ["3"]="³", ["4"]="⁴",
                       ["5"]="⁵", ["6"]="⁶", ["7"]="⁷", ["8"]="⁸" }

local function tlpa_with_supers(tl)
  if not tl then return tl end
  local stem, tone = tl:match("^(.-)([1-8])$")
  return stem and (stem .. (supers_digit[tone] or "")) or tl
end

-- 依 supers_tone 選擇 TLPA 的呈現（上標或數字）
local function tlpa_render_by_option(tl, use_supers)
  if use_supers then
    return tlpa_with_supers(tl)
  else
    return tl -- 保持數字結尾
  end
end

-- 由 TLPA 取調號（最後一碼 1-8）
local function tone_from_tlpa(tl)
  return tl and tl:match("([1-8])$") or nil
end

-- 注音 + TLPA 調號 → 上標數字調
local function bpmf_with_supers_by_tl(bpmf, tlpa)
  if not bpmf then return nil end
  local base = strip_bpmf_marks_one(bpmf)
  local t = tone_from_tlpa(tlpa)
  return t and (base .. (supers_digit[t] or "")) or base
end

-- 注音 + TLPA 調號 → 尾隨數字調
local function bpmf_with_digit_by_tl(bpmf, tlpa)
  if not bpmf then return nil end
  local base = strip_bpmf_marks_one(bpmf)
  local t = tone_from_tlpa(tlpa)
  return t and (base .. t) or base
end

-- 對列表逐一套函數，再用空白接回
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
  return tl_list, bp_list
end

-- 定義按受處理的快捷鍵：使用【正規表示式】判斷
local function norm_repr(r)
  -- -- 能截獲的按鍵：Alt+Enter、Ctrl+Enter、Shift+Enter、Ctrl+Shift+Enter
  -- r = r:gsub("^Release%+", "")
  --      :gsub("ISO_Enter$", "Return")
  --      :gsub("Alt%+ISO_Enter$", "Alt+Return")
  -- 能截獲的按鍵：Enter、Ctrl+Enter、Shift+Enter、Ctrl+Shift+Enter
  r = r:gsub("^Release%+", ""):gsub("^ISO_Enter$", "Return")
  return r:lower()
end

-- ============= 主函式：aux_commit（多音節友善） =============
function aux_commit(key, env)
  local ctx = env.engine.context
  local r = norm_repr(key:repr())

  -- local want_tlpa   = (r == "return")                 -- Enter
  local want_tlpa   = (r == "return")                 -- Enter
  local want_bpmf   = (r == "control+return")         -- Ctrl+Enter
  local want_shift  = (r == "shift+return")           -- Shift+Enter（上標/數字）
  local want_both   = (r == "control+shift+return")   -- Ctrl+Shift+Enter（雙欄）

  if not (want_tlpa or want_bpmf or want_shift or want_both) then return 2 end

  local tl_list, bp_list = get_multiforms(env)

  -- Enter：TLPA（★音節之間「空白分隔」）
  -- if want_tlpa and #tl_list > 0 then
  --   env.engine:commit_text(table.concat(tl_list, " "))
  --   ctx:clear(); return 1
  -- end
-- Enter：TLPA（依 supers_tone 輸出上標或數字；音節之間空白）

  if want_tlpa and #tl_list > 0 then
    local use_supers = ctx:get_option("supers_tone")
    local out = map_join(tl_list, function(tl) return tlpa_render_by_option(tl, use_supers) end)
    env.engine:commit_text(out)
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
    local left = (#tl_list > 0) and ("〔" .. table.concat(tl_list, "〕 〔") .. "〕") or ""
    local right = (#bp_list > 0) and ("  【" .. table.concat(bp_list, "】 【") .. "】") or ""
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
  local tlpa, zu_im = {}, {}

  -- 抓所有 〔...〕（最小擷取）
  for t in s:gmatch("〔(.-)〕") do
    table.insert(tlpa, t)
  end

  -- 抓所有 【...】（最小擷取）
  for zu_im_hu_ho in s:gmatch("【(.-)】") do
    table.insert(zu_im, zu_im_hu_ho)
  end

  if #tlpa >= 2 and #tlpa == #zu_im then
    return "〔" .. table.concat(tlpa, "〕 〔") .. "〕"
           .. "  "
           .. "【" .. table.concat(zu_im, "】 【") .. "】"
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