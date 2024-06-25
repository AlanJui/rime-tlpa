-- custom.lua
local function custom_commit_text(env)
	local context = env.engine.context
	if context:has_menu() and context:is_composing() then
		local composition = context.composition
		local input = context.input
		local candidate = context:get_selected_candidate().text

		-- 定義拼音字母和方音符號之間的對映
		local mapping = {
			["1"] = "ㄅ",
			["q"] = "ㄆ",
			["a"] = "ㄇ",
			["2"] = "ㄉ",
			["w"] = "ㄊ",
			["s"] = "ㄋ",
			["x"] = "ㄌ",
			["e"] = "ㄍ",
			["d"] = "ㄎ",
			["c"] = "ㄏ",
			["v"] = "ㄫ",
			["r"] = "ㄗ",
			["f"] = "ㄘ",
			["t"] = "ㄙ",
			["g"] = "ㄧ",
			["y"] = "ㄨ",
			["h"] = "ㆬ",
			["n"] = "ㄚ",
			["u"] = "ㆦ",
			["j"] = "ㄜ",
			["m"] = "ㄝ",
			["8"] = "ㄞ",
			["i"] = "ㄠ",
			["k"] = "ㄢ",
			["9"] = "ㄣ",
			["l"] = "ㄤ",
			["0"] = "ㄥ",
			["p"] = "声",
			[";"] = "ㆠ",
			["z"] = "ㆣ",
			["!"] = "ㆡ",
			["E"] = "ㆪ",
			["Y"] = "ㆫ",
			["U"] = "ㆩ",
			["J"] = "ㆧ",
			["*"] = "ㆥ",
			["I"] = "ㆮ",
			["<"] = "ㆯ",
			["("] = "˪",
			["L"] = "ˋ",
			["3"] = "˫",
			["4"] = "ˊ",
			["5"] = "．",
		}

		-- 將輸入的拼音轉換成對應的方音符號
		local phonetic_input = input:gsub(".", function(c)
			return mapping[c] or c
		end)

		local script_text = string.format("%s[%s]", candidate, phonetic_input)
		env.engine:commit_text(script_text)
		context:clear()
	end
end

return { func = custom_commit_text }
