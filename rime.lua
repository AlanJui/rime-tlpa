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
