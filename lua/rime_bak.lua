
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