-- custom.lua
local function custom_commit_text(env)
	local context = env.engine.context
	if context:has_menu() and context:is_composing() then
		local composition = context.composition
		local input = context.input
		local candidate = context:get_selected_candidate().text

		-- 定義拼音字母和方音符號之間的對映
		local mapping = {
      -- ["-"] = "ｎ",
      ["ㄅ"] = "p",
      ["ㄅㄏ"] = "b",
      ["ㄆ"] = "ph",
      ["ㄇ"] = "m",
      ["ㄉ"] = "t",
      ["ㄊ"] = "th",
      ["ㄋ"] = "n",
      ["ㄌ"] = "l",
      ["ㄍ"] = "k",
      ["ㄍㄏ"] = "g",
      ["ㄎ"] = "kh",
      ["ㄏ"] = "h",
      ["ㄗ"] = "c",
      ["ㄘ"] = "ch",
      ["ㄙ"] = "s",
      ["ㄖ"] = "j",
      ["ㄐㄧ"] = "ci-",
      ["ㄑㄧ"] = "chi-",
      ["ㄒㄧ"] = "si-",
      ["ㄥ"] = "ng",
      ["ㄧ"] = "i",
      ["ㄥㄧ"] = "Ni",
      ["ㄨ"] = "u",
      ["ㄥㄨ"] = "Nu",
      ["ㄚ"] = "a",
      ["ㄥㄚ"] = "Na",
      ["ㄝ"] = "e",
      ["ㄥㄝ"] = "Ne",
      ["ㄛ"] = "oo",
      ["ㄥㄛ"] = "Noo",
      ["ㄜ"] = "o",
      ["ㄢ"] = "an",
      ["ㄞ"] = "ai",
      ["ㄥㄞ"] = "Nai",
      ["ㄠ"] = "au",
      ["ㄥㄠ"] = "Nau",
      ["ㄛㄇ"] = "om",
      ["ㄚㄇ"] = "am",
      ["ㄛㄥ"] = "ong",
      ["ㄤ"] = "ang",
      ["ㆨ"] = "ir",
      ["ㄣ"] = "n",
      ["ˉ"] = "1",
      ["ˋ"] = "2",
      ["_"] = "3",
      ["ˇ"] = "5",
      ["+"] = "7",
      ["ˊ"] = "8",
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

-- return { func = custom_commit_text }
return custom_commit_text
