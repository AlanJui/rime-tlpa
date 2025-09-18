-----------------------------------------------------------------------------------------
-- jump_select：候選單快速跳轉（只移動高亮，不上屏）

-- 固定對齊「畫面 5 行」：頂=Home；中=Home+Down×2；底=Home+Down×4
-- 按（Ctrl+.）鍵，即可將高亮移動到候選頁中間位置
-- 熱鍵：Ctrl+/（頂）、Ctrl+.（中）、Ctrl+,（底）
-- 注意：F20/F24 是代理鍵，會在 schema 的 key_binder 被翻成 Home/Down
local function press_key_n(env, key_name, n)
  for _ = 1, n do env.engine:process_key(KeyEvent(key_name)) end
end

local function norm(r)
  if r:sub(1,8) == "Release+" then return r:sub(9) end
  return r
end

function jump_select(key, env)
  local ctx = env.engine.context
  if not ctx:has_menu() then return 2 end

  local r = norm(key:repr())

  -- 避免自觸發（忽略我們送出的代理鍵）
  if r == "F20" or r == "F24" then return 2 end

  -- 候選字視窗中游標移動快捷鍵：頂端/中位/底端
  local go_top    = (r == "Control+comma")  or (r == "Control+,")
  local go_middle = (r == "Control+period") or (r == "Control+.")
  local go_bottom = (r == "Control+slash")

  if not (go_top or go_middle or go_bottom) then return 2 end

  -- 回頂（F20 → Home）
  env.engine:process_key(KeyEvent("F20"))

  -- 固定步數：中=2、底=4（頂=0）
  local steps = go_middle and 2 or (go_bottom and 4 or 0)
  if steps > 0 then press_key_n(env, "F24", steps) end  -- F24 → Down
  return 1
end
