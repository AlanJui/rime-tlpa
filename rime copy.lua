-- v0.1.0.0
number_translator = require("number")
custom_commit_text_translator = require("custom")
-- piau_im_translator = require("piau_im")

-- function get_date(input, seg, env)
-- 	--- 以 show_date 爲開關名或 key_binder 中 toggle 的對象
-- 	on = env.engine.context:get_option("show_date")
-- 	if on and input == "date" then
-- 		--- Candidate(type, start, end, text, comment)
-- 		yield(Candidate("date", seg.start, seg._end, os.date("%Y年%m月%d日"), " 日期"))
-- 	end
-- end
---
-- function single_char_first(input, env)
-- 	--- 以 single_char 爲開關名或 key_binder 中 toggle 的對象
-- 	on = env.engine.context:get_option("single_char")
-- 	local cache = {}
-- 	for cand in input:iter() do
-- 		if not on or utf8.len(cand.text) == 1 then
-- 			yield(cand)
-- 		else
-- 			table.insert(cache, cand)
-- 		end
-- 	end
-- 	for i, cand in ipairs(cache) do
-- 		yield(cand)
-- 	end
-- end

-----------------------------------------------------------------------------------------
-- 候選單之游標移動功能
-----------------------------------------------------------------------------------------
-- （1）只「移動高亮」不上屏。
-- （2）自動偵測 menu.page_size 與當前頁候選數（最後一頁不足時也 OK）。
-- （3）先用多次 Up 把選取「歸零到頂端」，再精準往下移動到目標位。
-- （4）不佔用注音用掉的字母鍵，只用 Ctrl 組合鍵。
--
-----------------------------------------------------------------------------------------
-- 【操作按鍵】：
-- function jump_select(key, env)
-- Lua 回傳值要用數字：1 = kAccepted（吃掉事件、不再往後傳）、2 = kNoop（放行）。
-----------------------------------------------------------------------------------------
-- jump_select：候選單快速跳轉（只移動高亮，不上屏）
-- Ctrl+Alt+J → 跳到本頁最後一個
-- Ctrl+Alt+K → 跳到本頁中間
-- Ctrl+Alt+H → 回到本頁頂端

local function press_key_n(env, key_name, n)
  for _ = 1, n do env.engine:process_key(KeyEvent(key_name)) end
end

local function move_to_top(env, page_size)
  press_key_n(env, "Up", math.max(1, (page_size or 9) + 2))
end

function jump_select(key, env)
  local context = env.engine.context
  if not context:has_menu() then return 2 end

  local menu = context.menu
  local page_size = (menu and menu.page_size) or 9
  local cand_count = (menu and menu:candidate_count()) or 0
  if cand_count == 0 then return 2 end

  local repr = key:repr()  -- 例如 "Control+Alt+J"
  local target_index

  if repr == "Control+Alt+J" then
    target_index = math.min(page_size, cand_count)
  elseif repr == "Control+Alt+K" then
    target_index = math.min(math.ceil(page_size / 2), cand_count)
  elseif repr == "Control+Alt+H" then
    target_index = 1
  else
    return 2
  end

  -- Debug 觀察用
  env.engine:commit_text("[J]")   -- 偵錯（按鍵有攔到就會上屏 [J]，確認後再刪掉）
  move_to_top(env, page_size)
  if target_index > 1 then
    press_key_n(env, "Down", target_index - 1)
  end
  return 1
end
