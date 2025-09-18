-----------------------------------------------------------------------------------------
-- 【操作按鍵】：
-- function jump_select(key, env)
-- Lua 回傳值要用數字：1 = kAccepted（吃掉事件、不再往後傳）、2 = kNoop（放行）。
-----------------------------------------------------------------------------------------
-- jump_select：候選單快速跳轉（只移動高亮，不上屏）
-- Ctrl+Alt+J → 跳到本頁最後一個
-- Ctrl+Alt+K → 跳到本頁中間
-- Ctrl+Alt+H → 回到本頁頂端

-- -- 放在 rime.lua，暫時用來診斷：只要有候選單，就把收到的按鍵 repr 吐出來
-- function jump_select(key, env)
--   local context = env.engine.context
--   if not context:has_menu() then
--     return 2
--   end
--   env.engine:commit_text("[LUA:" .. key:repr() .. "]")
--   return 1
-- end

-- jump_select：候選單快速跳轉（只移動高亮，不上屏）
-- F13 → 跳到底端；F14 → 跳到中間；F15 → 回到頂端
-- 這些 F13~F15 由 key_binder 在 has_menu 時，將你的熱鍵轉送而來。

-- 只處理「跳中位」：F24 觸發 → Home 到頂 → Down 若干次
-- 配合 weasel.custom.yaml：
--   - Control+comma  → End   （到底，前端處理）
--   - Control+slash  → Home  （到頂，前端處理）
--   - Control+period → F24   （中位，交本函式處理）

local function press_key_n(env, key_name, n)
  for _ = 1, n do
    env.engine:process_key(KeyEvent(key_name))
  end
end

local function normalize_repr(repr)
  if repr:sub(1, 8) == "Release+" then
    return repr:sub(9)
  end
  return repr
end

function jump_select(key, env)
  local context = env.engine.context
  -- 僅在候選單開啟時作用
  if not context:has_menu() then
    return 2  -- kNoop
  end

  local r = normalize_repr(key:repr())
  -- 只吃 F24（中位）；頂/底交給前端 Home/End，不在這裡處理
  if r ~= "F24" then
    return 2
  end

  local menu = context.menu
  -- 讀取當前頁大小；若前端 style/page_size 已設為 5，這裡會反映為 5
  local page_size = (menu and menu.page_size) or 9
  -- 中位：ceil(page_size/2)，要按 Down 的次數 = 中位索引-1
  local steps = math.max(0, math.ceil(page_size / 2) - 1)

  -- 先到頂（Home），再往下走 steps 步
  env.engine:process_key(KeyEvent("Home"))
  -- Debug
  env.engine:commit_text("{MID:" .. tostring(page_size) .. "}")
  if steps > 0 then
    press_key_n(env, "Down", steps)
  end

  return 1  -- kAccepted：事件已處理並吃掉
end
