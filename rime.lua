-- Version: 0.2.3 (2026/4/29)
-- Version: 0.2.1 (2026/4/28)
-- RIME API 依賴於運行時環境，無需顯式引入

---@diagnostic disable: undefined-global

-- === DICTIONARIES ===

-- 十五音【聲母】與【台語音標】之對映關係
local siann_bu_dict = {
	["邊"] = "p",
	["頗"] = "ph",
	["門"] = "b",
	["毛"] = "m",
	["地"] = "t",
	["他"] = "th",
	["耐"] = "n",
	["柳"] = "l",
	["曾"] = "z",
	["出"] = "c",
	["時"] = "s",
	["入"] = "j",
	["求"] = "k",
	["去"] = "kh",
	["語"] = "g",
	["雅"] = "ng",
	["喜"] = "h",
	["英"] = "",
}

-- 十五音【韻母】與【台語音標】之對映對映關係
-- 前為【舒聲】韻母：調號為 1、2、3、5、6、7
-- 後為【促聲】韻母：調號為 4 或 8
local un_bu_dict = {
	["君"] = { "un", "ut" },
	["堅"] = { "ian", "iat" },
	["金"] = { "im", "ip" },
	["規"] = { "ui", "" },
	["嘉"] = { "ee", "eeh" },
	["干"] = { "an", "at" },
	["公"] = { "ong", "ok" },
	["乖"] = { "uai", "uaih" },
	["經"] = { "ing", "ik" },
	["觀"] = { "uan", "uat" },
	["沽"] = { "oo", "" },
	["嬌"] = { "iau", "iauh" },
	["稽"] = { "ei", "" },
	["恭"] = { "iong", "iok" },
	["高"] = { "o", "oh" },
	["皆"] = { "ai", "" },
	["巾"] = { "in", "it" },
	["姜"] = { "iang", "iak" },
	["甘"] = { "am", "ap" },
	["瓜"] = { "ua", "uah" },
	["江"] = { "ang", "ak" },
	["兼"] = { "iam", "iap" },
	["交"] = { "au", "auh" },
	["迦"] = { "ia", "iah" },
	["檜"] = { "ue", "ueh" },
	["監"] = { "ann", "ahnn" },
	["艍"] = { "u", "uh" },
	["膠"] = { "a", "ah" },
	["居"] = { "i", "ih" },
	["丩"] = { "iu", "" },
	["更"] = { "enn", "ehnn" },
	["褌"] = { "uinn", "" },
	["茄"] = { "io", "ioh" },
	["梔"] = { "inn", "ihnn" },
	["薑"] = { "ionn", "" },
	["驚"] = { "iann", "" },
	["官"] = { "uann", "" },
	["鋼"] = { "ng", "" },
	["伽"] = { "e", "eh" },
	["閒"] = { "ainn", "" },
	["姑"] = { "oonn", "" },
	["姆"] = { "m", "" },
	["光"] = { "uang", "uak" },
	["閂"] = { "uainn", "uaihnn" },
	["糜"] = { "uenn", "" },
	["嘄"] = { "iaunn", "iauhnn" },
	["箴"] = { "om", "op" },
	["爻"] = { "aunn", "" },
	["扛"] = { "onn", "ohnn" },
	["牛"] = { "iunn", "" },
}

-- 十五音【聲調】在【中文調號】與【阿拉伯字調號】之對映關係
local tiau_ho_map = {
	["一"] = 1,
	["二"] = 2,
	["三"] = 3,
	["四"] = 4,
	["五"] = 5,
	["六"] = 6,
	["七"] = 7,
	["八"] = 8,
}

-- 【白話字】與【台羅拼音】使用之聲調符號（調符）對照表
local POJ_TIAU_HU = {
	["1"] = "",
	["2"] = "́", -- U+0301
	["3"] = "̀", -- U+0300
	["4"] = "",
	["5"] = "̂", -- U+0302
	["6"] = "̌", -- U+030C
	["7"] = "̄", -- U+0304
	["8"] = "̍", -- U+030D
}

-- 方音符號之調符對映關係
local TPS_TIAU_HU = {
	["2"] = "ˋ",
	["3"] = "˪",
	["5"] = "ˊ",
	["7"] = "˫",
	["8"] = "˙",
}

-- 【上標數字】標示聲調之【調號】值
local supers_digit = {
	["1"] = "¹",
	["2"] = "²",
	["3"] = "³",
	["4"] = "⁴",
	["5"] = "⁵",
	["6"] = "⁶",
	["7"] = "⁷",
	["8"] = "⁸",
}

-- === END DICTIONARIES ===

local function convert_sni_to_tlpa(s)
	-- 將【十五音】轉換成【台語音標】
	local chars = {}
	for uchar in s:gmatch("[%z\1-\127\194-\244][\128-\191]*") do
		table.insert(chars, uchar)
	end
	if #chars ~= 3 then
		return nil
	end

	local un = chars[1]
	local tiau = chars[2]
	local siann = chars[3]

	local tiau_ho = tiau_ho_map[tiau]	-- 調號：tiau_ho
	local siann_bu = siann_bu_dict[siann]
	local un_bu = un_bu_dict[un]

	if not tiau_ho or not siann_bu or not un_bu then
		return nil
	end

	-- 依據【調號】選用【舒聲】或【促聲】韻母：調號為 4 或 8 時，使用促聲韻母；其他調號則使用舒聲韻母
	local jip_siann_tiau = (tiau_ho == 4 or tiau_ho == 8)  -- 入聲調號為 4 或 8 時，才使用 un_bu_dict 中的第二個元素（入聲調）
	un_bu = jip_siann_tiau and un_bu[2] or un_bu[1]  -- 根據是否為入聲調，選擇 un_bu_dict 中的對應元素

	return siann_bu .. un_bu .. tiau_ho
end

local function apply_poj_tiau_hu(syllable)
	-- 【台語音標】轉換成【白話字】或【台羅拼音】時，
	-- 原先之【調號】需轉換成【調符】，並套於【羅馬拼音字母】之上。
	local base, tone = syllable:match("^(.-)([1-8])$")
	if not base or not tone then
		return syllable
	end
	local mark = POJ_TIAU_HU[tone]
	if not mark or mark == "" then
		return base
	end

	local res = base
	if base:find("a") then
		res = base:gsub("a", "a" .. mark, 1)
	elseif base:find("oo") then
		res = base:gsub("oo", "o" .. mark .. "o", 1)
	elseif base:find("ee") then
		res = base:gsub("ee", "e" .. mark .. "e", 1)
	elseif base:find("e") then
		res = base:gsub("e", "e" .. mark, 1)
	elseif base:find("o") then
		res = base:gsub("o", "o" .. mark, 1)
	elseif base:find("iu") then
		res = base:gsub("iu", "i" .. "u" .. mark, 1)
	elseif base:find("ui") then
		res = base:gsub("ui", "u" .. "i" .. mark, 1)
	elseif base:find("i") then
		res = base:gsub("i", "i" .. mark, 1)
	elseif base:find("u") then
		res = base:gsub("u", "u" .. mark, 1)
	elseif base:find("m") then
		res = base:gsub("m", "m" .. mark, 1)
	elseif base:find("ng") then
		res = base:gsub("ng", "n" .. mark .. "g", 1)
	else
		res = base .. mark
	end
	return res
end

------------------------------------------------------------------------------------------
-- aux_commit：切換輸入方案【輸出】之【漢字標音】格式
-- Space → 漢字
-- Enter → 漢字標音（格式依選項而定）
------------------------------------------------------------------------------------------

function aux_commit(key, env)
	log.info("[debug] aux_commit triggered by key: " .. key:repr())
	local ctx = env.engine.context
	local r = key:repr():gsub("^Release%+", ""):gsub("^ISO_Enter$", "Return"):lower()

	if r == "return" or r == "kp_enter" then
		if not ctx:has_menu() then
			return 2
		end
		local cand = ctx:get_selected_candidate()
		if not cand then
			return 2
		end

		local gen_comm = cand.comment
		if not gen_comm or gen_comm == "" then
			gen_comm = cand:get_genuine().comment or ""
		end
		log.info("[aux_commit] cand.text=" .. (cand.text or "?") .. " comment=[" .. gen_comm .. "]")

		-- 【候選清單】兩欄式：左欄 〔韻+調+聲〕，右欄 【方音符號】
		local sni_list, tps_list = {}, {}
		for zo_pinn in gen_comm:gmatch("〔(.-)〕") do
			table.insert(sni_list, zo_pinn)
		end
		for ziann_pinn in gen_comm:gmatch("【(.-)】") do
			table.insert(tps_list, ziann_pinn)
		end

		log.info("[aux_commit] sni_list count=" .. #sni_list .. " tps_list count=" .. #tps_list)
		for i, v in ipairs(sni_list) do
			log.info("[aux_commit] sni_list[" .. i .. "]=[" .. v .. "]")
		end

		if #sni_list == 0 then
			log.info("[aux_commit] sni_list is empty, returning kNoop")
			return 2
		end

		-- 取得 tlpa_converter 模組（含 convert / split / INITIALS / FINALS）
		local conv = require("tlpa_converter")

		-- BPM2（台語注音二式）聲母對照表：TLPA 聲母 → BPM2 聲母（依 100_閩南語聲韻調對映指引.md）
		local BPM2_SIANN = {
			p="b",   ph="p",  b="bb",  m="m",
			t="d",   th="t",  n="n",   l="l",
			z="z",   c="c",   j="zz",  s="s",
			k="g",   kh="k",  g="gg",  ng="ng",
			h="h",
			-- 顎化聲母
			zi="j",  ci="ch", ji="jj", si="sh",
		}

		-- TLPA 數字調 → BPM2 數字調（與 TLPA 同，皆用 1-8）
		local function to_bpm2(tlpa)
			local parts = conv.split(tlpa)
			if not parts then return tlpa end
			local zero = (parts.siann == "\195\184" or parts.siann == "\195\152")
			local b2 = zero and "" or (BPM2_SIANN[parts.siann] or parts.siann)
			return b2 .. parts.un .. parts.tiau
		end

		-- [DBG] 確認目前 switch 狀態
		log.info("[aux_commit] key_in_piau_im_tps="  .. tostring(ctx:get_option("key_in_piau_im_tps")))
		log.info("[aux_commit] key_in_piau_im_tlpa=" .. tostring(ctx:get_option("key_in_piau_im_tlpa")))
		log.info("[aux_commit] key_in_piau_im_tl="   .. tostring(ctx:get_option("key_in_piau_im_tl")))
		log.info("[aux_commit] key_in_piau_im_poj="  .. tostring(ctx:get_option("key_in_piau_im_poj")))
		log.info("[aux_commit] key_in_piau_im_bp="   .. tostring(ctx:get_option("key_in_piau_im_bp")))
		log.info("[aux_commit] key_in_piau_im_bpm2=" .. tostring(ctx:get_option("key_in_piau_im_bpm2")))
		log.info("[aux_commit] key_in_piau_im_ipa="  .. tostring(ctx:get_option("key_in_piau_im_ipa")))
		log.info("[aux_commit] key_in_piau_im_sni="  .. tostring(ctx:get_option("key_in_piau_im_sni")))

		-- key_in_piau_im_* 決定 Enter 鍵輸出格式（310.md §輸入編輯列之漢字標音格式）
		local out_list = {}

		if ctx:get_option("key_in_piau_im_tps") then
			-- 方音符號：直接取右欄 【...】 內容
			for i, v in ipairs(tps_list) do
				out_list[i] = v
			end

		elseif ctx:get_option("key_in_piau_im_tlpa") then
			-- 台語音標（數字調號）：十五音 → TLPA
			for i, v in ipairs(sni_list) do
				local tlpa = convert_sni_to_tlpa(v)
				out_list[i] = tlpa and conv.convert(tlpa, "台語音標") or v
			end

		elseif ctx:get_option("key_in_piau_im_tl") then
			-- 台羅拼音（調符）：十五音 → TLPA → 台羅
			for i, v in ipairs(sni_list) do
				local tlpa = convert_sni_to_tlpa(v)
				out_list[i] = tlpa and conv.convert(tlpa, "台羅拼音") or v
			end

		elseif ctx:get_option("key_in_piau_im_poj") then
			-- 白話字（調符）：十五音 → TLPA → POJ
			for i, v in ipairs(sni_list) do
				local tlpa = convert_sni_to_tlpa(v)
				out_list[i] = tlpa and conv.convert(tlpa, "白話字") or v
			end

		elseif ctx:get_option("key_in_piau_im_bp") then
			-- 閩拼方案（調符）：十五音 → TLPA → BP
			for i, v in ipairs(sni_list) do
				local tlpa = convert_sni_to_tlpa(v)
				out_list[i] = tlpa and conv.convert(tlpa, "閩拼方案") or v
			end

		elseif ctx:get_option("key_in_piau_im_bpm2") then
			-- 台語注音二式（數字調號）：十五音 → TLPA → BPM2
			for i, v in ipairs(sni_list) do
				local tlpa = convert_sni_to_tlpa(v)
				out_list[i] = tlpa and to_bpm2(tlpa) or v
			end

		elseif ctx:get_option("key_in_piau_im_ipa") then
			-- 國際音標：十五音 → TLPA → IPA
			for i, v in ipairs(sni_list) do
				local tlpa = convert_sni_to_tlpa(v)
				out_list[i] = tlpa and conv.convert(tlpa, "國際音標") or v
			end

		else
			-- 預設（key_in_piau_im_sni）：十五音（韻+調+聲）原樣輸出
			for i, v in ipairs(sni_list) do
				out_list[i] = v
			end
		end

		local out_str = table.concat(out_list, " ")
		if #out_str > 0 then
			env.engine:commit_text(out_str)
			ctx:clear()
			return 1
		end
		return 2
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
		local new = Candidate(cand.type, cand.start, cand._end, cand.text, tag .. (cand.comment or ""))
		-- 保留原本的屬性
		new.preedit = cand.preedit
		yield(new)
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


local function convert_tl_to_tlpa(tl_str)
	if type(tl_str) ~= "string" or tl_str == "" then return "" end
	-- 處理聲母：台羅 (ts/tsh) => 台語音標 (z/c)
	local result = tl_str
	if result:match("^tsh") then
		result = result:gsub("^tsh", "c", 1)
	elseif result:match("^ts") then
		result = result:gsub("^ts", "z", 1)
	end
	return result
end

local function convert_tlpa_to_tps(tlpa_str)
	if type(tlpa_str) ~= "string" or tlpa_str == "" then return "" end
	local tones = { ["1"]="", ["2"]="ˋ", ["3"]="˪", ["4"]="", ["5"]="ˊ", ["6"]="ˋ", ["7"]="˫", ["8"]="˙", ["9"]="", ["0"]="" }
	local initials = { ["ph"]="ㄆ", ["kh"]="ㄎ", ["th"]="ㄊ", ["ng"]="ㄫ", ["p"]="ㄅ", ["b"]="ㆠ", ["m"]="ㄇ", ["t"]="ㄉ", ["n"]="ㄋ", ["l"]="ㄌ", ["k"]="ㄍ", ["g"]="ㆣ", ["h"]="ㄏ", ["s"]="ㄙ", ["j"]="ㆡ", ["z"]="ㄗ", ["c"]="ㄘ" }
	local finals = { ["aunn"]="ㆯ", ["ainn"]="ㆮ", ["iann"]="ㄧㆩ", ["iunn"]="ㄧㆫ", ["uann"]="ㄨㆩ", ["uenn"]="ㄨㆥ", ["oonn"]="ㆧ", ["ann"]="ㆩ", ["inn"]="ㆪ", ["unn"]="ㆫ", ["enn"]="ㆥ", ["onn"]="ㆧ", ["iong"]="ㄧㆲ", ["iang"]="ㄧㄤ", ["uang"]="ㄨㄤ", ["ong"]="ㆲ", ["ang"]="ㄤ", ["iam"]="ㄧㆰ", ["am"]="ㆰ", ["om"]="ㆱ", ["ian"]="ㄧㄢ", ["uan"]="ㄨㄢ", ["an"]="ㄢ", ["ing"]="ㄧㄥ", ["in"]="ㄧㄣ", ["un"]="ㄨㄣ", ["iai"]="ㄧㄞ", ["iau"]="ㄧㄠ", ["uai"]="ㄨㄞ", ["ai"]="ㄞ", ["au"]="ㄠ", ["ia"]="ㄧㄚ", ["io"]="ㄧㄜ", ["iu"]="ㄧㄨ", ["ua"]="ㄨㄚ", ["ue"]="ㄨㆤ", ["ui"]="ㄨㄧ", ["uainn"]="ㄨㆮ", ["uinn"]="ㄨㆪ", ["iaunn"]="ㄧㆯ", ["ioo"]="ㄧㆦ", ["ng"]="ㆭ", ["m"]="ㆬ", ["n"]="ㄣ", ["oo"]="ㆦ", ["a"]="ㄚ", ["i"]="ㄧ", ["u"]="ㄨ", ["e"]="ㆤ", ["o"]="ㄜ", ["ir"]="ㆨ" }
	local codas = { ["p"]="ㆴ", ["t"]="ㆵ", ["k"]="ㆻ", ["h"]="ㆷ" }

	local tone_num = tlpa_str:match("%d$")
	local s = tlpa_str:gsub("%d$", "")

	local coda_char = s:match("[ptkh]$")
	local initial_str = ""
	for _, len in ipairs({3, 2, 1}) do
		local pre = s:sub(1, len)
		if initials[pre] then
			if (pre == "ng" or pre == "m" or pre == "n") and s:len() == len then break end
			if (pre == "ng" or pre == "m" or pre == "n") and coda_char == "h" and s:len() == len + 1 then break end
			initial_str = initials[pre]
			s = s:sub(len + 1)
			break
		end
	end

	local coda_str = ""
	if coda_char and #s > 0 then
        local base = s:sub(1, -2)
        if base ~= "" and finals[base] then
            coda_str = codas[coda_char]
            s = base
        elseif base == "i" or base == "e" or base == "o" or base == "a" or base == "u" then
            coda_str = codas[coda_char]
            s = base
        end
	end

	if s:sub(1, 1) == "i" then
		if initial_str == "ㆡ" then initial_str = "ㆢ" end
		if initial_str == "ㄗ" then initial_str = "ㄐ" end
		if initial_str == "ㄘ" then initial_str = "ㄑ" end
		if initial_str == "ㄙ" then initial_str = "ㄒ" end
	end

	local final_str = finals[s] or s
	local tone_str = tone_num and tones[tone_num] or ""
	return initial_str .. final_str .. coda_str .. tone_str
end

local function convert_bpm2_to_tps(bpm2_str)
	if type(bpm2_str) ~= "string" or bpm2_str == "" then return "" end
	local tones = { ["1"]="", ["2"]="ˋ", ["3"]="˪", ["4"]="", ["5"]="ˊ", ["6"]="ˋ", ["7"]="˫", ["8"]="˙", ["9"]="", ["0"]="" }
	local initials = { ["ch"]="ㄑ", ["sh"]="ㄒ", ["jj"]="ㆢ", ["bb"]="ㆠ", ["gg"]="ㆣ", ["zz"]="ㆡ", ["ng"]="ㄫ", ["p"]="ㄆ", ["b"]="ㄅ", ["m"]="ㄇ", ["t"]="ㄊ", ["d"]="ㄉ", ["n"]="ㄋ", ["l"]="ㄌ", ["k"]="ㄎ", ["g"]="ㄍ", ["h"]="ㄏ", ["c"]="ㄘ", ["z"]="ㄗ", ["s"]="ㄙ", ["j"]="ㄐ" }
	local finals = { ["aunn"]="ㆯ", ["ainn"]="ㆮ", ["iann"]="ㄧㆩ", ["iunn"]="ㄧㆫ", ["uann"]="ㄨㆩ", ["uenn"]="ㄨㆥ", ["oonn"]="ㆧ", ["ann"]="ㆩ", ["inn"]="ㆪ", ["unn"]="ㆫ", ["enn"]="ㆥ", ["iong"]="ㄧㆲ", ["iang"]="ㄧㄤ", ["uang"]="ㄨㄤ", ["ong"]="ㆲ", ["ang"]="ㄤ", ["iam"]="ㄧㆰ", ["oom"]="ㆱ", ["am"]="ㆰ", ["ian"]="ㄧㄢ", ["uan"]="ㄨㄢ", ["an"]="ㄢ", ["ing"]="ㄧㄥ", ["iek"]="ㄧㆻ", ["in"]="ㄧㄣ", ["un"]="ㄨㄣ", ["iai"]="ㄧㄞ", ["iau"]="ㄧㄠ", ["uai"]="ㄨㄞ", ["ai"]="ㄞ", ["au"]="ㄠ", ["ia"]="ㄧㄚ", ["io"]="ㄧㄜ", ["iu"]="ㄧㄨ", ["ua"]="ㄨㄚ", ["ue"]="ㄨㆤ", ["ui"]="ㄨㄧ", ["uainn"]="ㄨㆮ", ["uinn"]="ㄨㆪ", ["iaunn"]="ㄧㆯ", ["ioo"]="ㄧㆦ", ["ng"]="ㆭ", ["m"]="ㆬ", ["n"]="ㄣ", ["oo"]="ㆦ", ["or"]="ㄜ", ["a"]="ㄚ", ["i"]="ㄧ", ["u"]="ㄨ", ["e"]="ㆤ", ["o"]="ㄜ", ["ir"]="ㆨ" }
	local codas = { ["p"]="ㆴ", ["t"]="ㆵ", ["k"]="ㆻ", ["h"]="ㆷ" }

	local tone_num = bpm2_str:match("%d$")
	local s = bpm2_str:gsub("%d$", "")

	local coda_char = s:match("[ptkh]$")
	local initial_str = ""
	for _, len in ipairs({2, 1}) do
		local pre = s:sub(1, len)
		if initials[pre] then
			if (pre == "ng" or pre == "m" or pre == "n") and s:len() == len then break end
			if (pre == "ng" or pre == "m" or pre == "n") and coda_char == "h" and s:len() == len + 1 then break end
			initial_str = initials[pre]
			s = s:sub(len + 1)
			break
		end
	end

	local coda_str = ""
	if coda_char and #s > 0 then
		local base = s:sub(1, -2)
		if base ~= "" and finals[base] then
			coda_str = codas[coda_char]
			s = base
		elseif base == "i" or base == "e" or base == "o" or base == "a" or base == "u" then
			coda_str = codas[coda_char]
			s = base
		end
	end

	local final_str = finals[s] or s
	local tone_str = tone_num and tones[tone_num] or ""
	return initial_str .. final_str .. coda_str .. tone_str
end

local function convert_tl_to_tps(tl_str)
	if type(tl_str) ~= "string" or tl_str == "" then return "" end
	local tlpa_str = convert_tl_to_tlpa(tl_str)
	return convert_tlpa_to_tps(tlpa_str)
end

local function format_comment(comment_string, mode, schema_id)
	-- comment_string: 原始 comment 字串
	--   左欄 〔...〕 為十五音，原始格式：【聲+韻+調】（如：柳君二）
	--   右欄 【...】 為方音符號
	-- mode: "tps"（方音符號）、"tlpa"（台語音標）、"sni"（十五音）
	if type(comment_string) ~= "string" or comment_string == "" then
		return comment_string
	end
	local left_col, right_col = {}, {}

	-- 取左欄的所有音節（輸入方案支援【連續輸入】，故音節數不一定為單一）
	for left in comment_string:gmatch("〔(.-)〕") do
		table.insert(left_col, left)
	end
	for right in comment_string:gmatch("【(.-)】") do
		table.insert(right_col, right)
	end

	if #left_col == 0 then
		return comment_string
	end

	local is_sni = schema_id and (schema_id:match("hau_suan") or schema_id:match("huan_ciat"))
	-- 將左欄每個音節從【聲+韻+調】重排為【韻+調+聲】（傳統十五音順序）
	-- 【例】：柳君二（聲+韻+調）→ 君二柳（韻+調+聲）
	local display_left = {}
	for _, s in ipairs(left_col) do
		local chars = {}
		for uchar in s:gmatch("[%z\1-\127\194-\244][\128-\191]*") do
			table.insert(chars, uchar)
		end
		-- 只有十五音（反切/校算）才需要倒裝字元順序
		if is_sni and #chars == 3 then
			-- 聲[1] + 韻[2] + 調[3]  →  韻[2] + 調[3] + 聲[1]
			table.insert(display_left, chars[2] .. chars[3] .. chars[1])
		else
			table.insert(display_left, s)
		end
	end

	-- 決定右欄（【...】）的內容
	local right
	if mode == "tlpa" then
		-- 台語音標：將已重排（韻+調+聲）之十五音傳入 convert_sni_to_tlpa
		right = {}
		for i, t in ipairs(display_left) do
			if is_sni then
				local roman = convert_sni_to_tlpa(t)
				right[i] = roman and roman or (right_col[i] or "")
			else
				right[i] = right_col[i] or ""
			end
		end
	elseif mode == "sni" then
		-- 僅十五音：不顯示右欄
		right = nil
	else
		-- 預設（tps）：方音符號，嘗試將右欄（可能是 TL, TLPA 或 BPM2）轉換為 TPS
		local is_bpm2 = schema_id and schema_id:match("bpm2")
		right = {}
		for i, v in ipairs(right_col) do
			if is_sni then
				right[i] = v -- 對於 SNI 如果有右欄，可能不適用 TLPA->TPS，維持原樣
			elseif is_bpm2 then
				local tps = convert_bpm2_to_tps(v)
				right[i] = (tps ~= "") and tps or v
			else
				local tps = convert_tl_to_tps(v)
				right[i] = (tps ~= "") and tps or v
			end
		end
	end

	local prefix = comment_string:match("^(%s*)") or ""

	if right == nil then
		-- 僅顯示十五音（韻+調+聲）
		if #display_left >= 2 then
			return "〔" .. table.concat(display_left, "〕 〔") .. "〕"
		else
			return prefix .. "〔" .. display_left[1] .. "〕"
		end
	end

	if #display_left >= 2 and #display_left == #right then
		return "〔"
			.. table.concat(display_left, "〕 〔")
			.. "〕"
			.. "  "
			.. "【"
			.. table.concat(right, "】 【")
			.. "】"
	end

	-- 單字（或右欄數量不符時）
	if #display_left == 1 then
		local r = right[1] or ""
		if r ~= "" then
			return prefix .. "〔" .. display_left[1] .. "〕【" .. r .. "】"
		else
			return prefix .. "〔" .. display_left[1] .. "〕"
		end
	end

	return comment_string
end

function reformat_comment_filter(input, env)
	-- hau_suan_piau_im_* 決定候選清單【漢字標音】顯示格式（310.md §候選清單之漢字標音格式）
	local ctx = env.engine.context
	local mode
	if ctx:get_option("hau_suan_piau_im_tlpa") then
		mode = "tlpa"	-- 台語音標
	else
		mode = "tps"	-- 預設：方音符號 (hau_suan_piau_im_tps)
	end

	-- [DBG] 確認 filter 被呼叫，及當前 mode
	log.info("[reformat_comment_filter] mode=" .. mode)

	local schema_id = env.engine.schema.schema_id

	-- 【候選清單】逐項處理：重排 comment 中左欄【十五音】與右欄【注音符號】
	for hau_suan in input:iter() do
		local old = hau_suan.comment or ""
		-- [DBG] 觀察每個候選的原始 comment 內容
		log.info("[reformat_comment_filter] raw comment=[" .. old .. "] text=" .. (hau_suan.text or "?"))
		local new = format_comment(old, mode, schema_id)
		-- [DBG] 觀察格式化後的結果
		log.info("[reformat_comment_filter] new comment=[" .. new .. "]")
		local c = hau_suan:get_genuine()
		local nc = Candidate(c.type, c.start, c._end, c.text, new)
		nc.preedit = c.preedit  -- 修正：應取 genuine 的 preedit
		nc.quality = hau_suan.quality
		yield(nc)
	end
end

-----------------------------------------------------------------------------------------
-- jump_select：【候選字清單】每一頁可顯示：5個選項。為求選字的操作便利性。
-- 能在【候選字清單】中，以快捷鍵移動【選擇游標】，能將選擇游標，快速移到：
-- 頂端（第1個選項）/中間（第3個選項）/底端（第5個選項）三種快捷鍵。
-----------------------------------------------------------------------------------------
-- 邏輯：先發送 Page_Up 重置到頁首，再依位移量補送 Down 鍵。
-- 快捷鍵（由右至左）：
-- （1）Ctrl+M（頂端 1st）
-- （2）Ctrl+,（中間 3rd）
-- （3）Ctrl+.（底端 5th）
-----------------------------------------------------------------------------------------
function jump_select(key, env)
	local ctx = env.engine.context
	if not ctx:has_menu() then
		return 2
	end -- kNoop

	local r = key:repr()
	if r:sub(1, 8) == "Release+" then
		return 2
	end

	local offset = -1
	local auto_commit = false

	-- 【直接選用】(Move and Commit)
	if r == "Control+1" then
		offset = 0
		auto_commit = true
	elseif r == "Control+2" then
		offset = 1
		auto_commit = true
	elseif r == "Control+3" then
		offset = 2
		auto_commit = true
	elseif r == "Control+4" then
		offset = 3
		auto_commit = true
	elseif r == "Control+5" then
		offset = 4
		auto_commit = true

	-- 【移動選擇游標】(Move only) - 調整為右到左順序
	elseif r == "Control+m" then
		-- 移到第3個 (Ctrl + M) -> 中間
		offset = 2
	elseif r == "Control+comma" or r == "Control+less" or r == "Control+<" then
		-- 移到第1個 (Ctrl + ,) -> 頂端
		offset = 0
	elseif r == "Control+period" or r == "Control+greater" or r == "Control+>" or r == "Control+." then
		-- 移到第5個 (Ctrl + .) -> 底端
		offset = 4
	end

	if offset == -1 then
		return 2
	end

	local comp = ctx.composition
	if comp:empty() then
		return 1
	end
	local seg = comp:back()
	if not seg.menu then
		return 1
	end

	local page_size = env.engine.schema.page_size
	local selected_index = seg.selected_index
	local page_start = math.floor(selected_index / page_size) * page_size
	local target_index = page_start + offset

	local available = seg.menu:prepare(target_index + 1)
	if target_index >= available then
		target_index = available - 1
	end

	env.engine:process_key(KeyEvent("Page_Up"))

	local steps = target_index - page_start
	for i = 1, steps do
		env.engine:process_key(KeyEvent("Down"))
	end

	if auto_commit then
		env.engine:process_key(KeyEvent("space"))
	end

	return 1 -- kAccepted
end

-----------------------------------------------------------------------
-- 疑似已棄用之程式碼
-----------------------------------------------------------------------

local function press_key_n(env, key_name, n)
	for _ = 1, n do
		env.engine:process_key(KeyEvent(key_name))
	end
end

local function norm(r)
	if r:sub(1, 8) == "Release+" then
		return r:sub(9)
	end
	return r
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
		local nc = cand:clone() -- 關鍵：clone 保留 preedit/屬性
		nc.comment = old .. " [OK]"
		yield(nc)
	end
end

-- ========= 解析候選註解 / inline 的多音節工具 =========

-- 從候選註解抓所有 〔...〕 與 【...】（相容你重排後的「雙欄」與原始「配對」）
local function parse_comment_all(comment)
	if not comment or comment == "" then
		return {}, {}
	end
	local tlpa, zh = {}, {}
	-- 抓所有 TLPA
	for t in comment:gmatch("〔(.-)〕") do
		table.insert(tlpa, t)
	end
	-- 抓所有注音
	for z in comment:gmatch("【(.-)】") do
		table.insert(zh, z)
	end
	-- 若抓不到，再試「一對一對」的樣式
	if #tlpa == 0 or #zh == 0 then
		for L, R in comment:gmatch("〔(.-)〕%s*【(.-)】") do
			table.insert(tlpa, L)
			table.insert(zh, R)
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
		for seg in tl:gmatch("[^']+") do
			table.insert(tl_list, seg)
		end
	end

	if bp ~= "" then
		bp = bp:gsub("'", " ") -- 將連續輸入分隔符號轉空白
		for seg in bp:gmatch("%S+") do
			seg = seg:gsub("'", "")
			table.insert(bp_list, seg)
		end
		-- 若仍只得到一段但原始含 '，再保底拆
		if #bp_list <= 1 and bp:find("'", 1, true) then
			for seg in bp:gmatch("[^']+") do
				seg = seg:gsub("%s+", "")
				if #seg > 0 then
					table.insert(bp_list, seg)
				end
			end
		end
	end
	return tl_list, bp_list
end

-----------------------------------------------------------------------
-- 可能已棄用之漢字標音轉換處理函數
-----------------------------------------------------------------------
local TPS_TIAU_HU = "[ˊˋ˪˫˙]"
local function strip_bpmf_marks_one(s)
	return s and s:gsub(TPS_TIAU_HU, "") or s
end

local function tlpa_with_supers(tl)
	if not tl then
		return tl
	end
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
local function tps_with_supers_by_tl(bpmf, tlpa)
	if not bpmf then
		return nil
	end
	local base = strip_bpmf_marks_one(bpmf)
	local t = tone_from_tlpa(tlpa)
	return t and (base .. (supers_digit[t] or "")) or base
end

-- 注音 + TLPA 調號 → 尾隨數字調
local function tps_with_digit_by_tl(bpmf, tlpa)
	if not bpmf then
		return nil
	end
	local base = strip_bpmf_marks_one(bpmf)
	local t = tone_from_tlpa(tlpa)
	return t and (base .. t) or base
end

-- 對列表逐一套函數，再用空白接回
local function map_join(list, f) -- f(elem, idx) -> string
	local out = {}
	for i, v in ipairs(list) do
		out[i] = f(v, i) or ""
	end
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
