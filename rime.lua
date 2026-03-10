-- Version: 0.2 (2026-3-3)
-- RIME API 依賴於運行時環境，無需顯式引入

---@diagnostic disable: undefined-global

-- === DICTIONARIES ===

-- === END DICTIONARIES ===

-- === DICTIONARIES ===
local sheng_mu_dict = {
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

local yun_mu_dict = {
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

local tone_map = {
	["一"] = 1,
	["二"] = 2,
	["三"] = 3,
	["四"] = 4,
	["五"] = 5,
	["六"] = 6,
	["七"] = 7,
	["八"] = 8,
}

local function convert_15_to_roman(s)
	local chars = {}
	for uchar in s:gmatch("[%z\1-\127\194-\244][\128-\191]*") do
		table.insert(chars, uchar)
	end
	if #chars ~= 3 then
		return nil
	end

	local yun = chars[1]
	local tone = chars[2]
	local sheng = chars[3]

	local tone_num = tone_map[tone]
	local sheng_roman = sheng_mu_dict[sheng]
	local yun_romans = yun_mu_dict[yun]

	if not tone_num or not sheng_roman or not yun_romans then
		return nil
	end

	local is_entering = (tone_num == 4 or tone_num == 8)
	local yun_roman = is_entering and yun_romans[2] or yun_romans[1]

	return sheng_roman .. yun_roman .. tone_num
end

local POJ_TONE_MARKS = {
	["1"] = "",
	["2"] = "́", -- U+0301
	["3"] = "̀", -- U+0300
	["4"] = "",
	["5"] = "̂", -- U+0302
	["6"] = "̌", -- U+030C
	["7"] = "̄", -- U+0304
	["8"] = "̍", -- U+030D
}

local function apply_poj_tone_mark(syllable)
	local base, tone = syllable:match("^(.-)([1-8])$")
	if not base or not tone then
		return syllable
	end
	local mark = POJ_TONE_MARKS[tone]
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
-- === END DICTIONARIES ===

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

-----------------------------------------------------------------------------------------
-- jump_select：【候選字清單】每一頁可顯示：5個選項。為求選字的操作便利性。
-- 能在【候選字清單】中，以快捷鍵移動【選擇游標】，能將選擇游標，快速移到：
-- 頂端（第1個選項）/中間（第3個選項）/底端（第5個選項）三種快捷鍵。
-----------------------------------------------------------------------------------------
-- 邏輯：先發送 Page_Up 重置到頁首，再依位移量補送 Down 鍵。
-- 快捷鍵（由右至左）：
-- （1）Ctrl+/（頂端 1st）
-- （2）Ctrl+.（中間 3rd）
-- （3）Ctrl+,（底端 5th）
-- 注意：已廢棄 F20/F24 代理鍵機制，直接使用系統原生鍵以提高相容性。
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
	elseif r == "Control+slash" or r == "Control+?" then
		-- 移到第1個 (Ctrl + /) -> 頂端
		offset = 0
	elseif r == "Control+period" or r == "Control+greater" or r == "Control+>" or r == "Control+." then
		-- 移到第3個 (Ctrl + .) -> 中間
		offset = 2
	elseif r == "Control+comma" or r == "Control+less" or r == "Control+<" then
		-- 移到第5個 (Ctrl + ,) -> 底端
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

-- ========== 注音聲調處理 ==========
local TONE_MARKS = "[ˊˋ˪˫˙]"
local function strip_bpmf_marks_one(s)
	return s and s:gsub(TONE_MARKS, "") or s
end

-- 使用【上標數字】標示聲調之【調號】值
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
local function bpmf_with_supers_by_tl(bpmf, tlpa)
	if not bpmf then
		return nil
	end
	local base = strip_bpmf_marks_one(bpmf)
	local t = tone_from_tlpa(tlpa)
	return t and (base .. (supers_digit[t] or "")) or base
end

-- 注音 + TLPA 調號 → 尾隨數字調
local function bpmf_with_digit_by_tl(bpmf, tlpa)
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

-- ============= 主函式：aux_commit（多音節友善） =============

function aux_commit(key, env)
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
		local tlpa_15_list, bpmf_list = {}, {}
		for t in gen_comm:gmatch("〔(.-)〕") do
			table.insert(tlpa_15_list, t)
		end
		for z in gen_comm:gmatch("【(.-)】") do
			table.insert(bpmf_list, z)
		end

		if #tlpa_15_list == 0 then
			return 2
		end

		local p_15 = ctx:get_option("piau_im_format_15")
		local p_bp = ctx:get_option("piau_im_format_bpmf")
		local p_tlpa = ctx:get_option("piau_im_format_tlpa")

		local out_list = {}

		if p_15 then
			for i, v in ipairs(tlpa_15_list) do
				out_list[i] = v
			end
		elseif p_bp then
			for i, v in ipairs(bpmf_list) do
				out_list[i] = v
			end
		else
			local is_tiau = ctx:get_option("tiau_mark")
			for i, v in ipairs(tlpa_15_list) do
				local roman = convert_15_to_roman(v)
				if roman then
					out_list[i] = is_tiau and apply_poj_tone_mark(roman) or roman
				else
					out_list[i] = v
				end
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

--------------------------------------------------------------------------
-- reformat_comment_filter：重排候選註解中的羅馬拼音與注音符號
--------------------------------------------------------------------------
-- 為處理【連續輸入】時，【候選字清單】中漢字的【羅馬拼音字母】、【注音符號】亦能正確顯示。
-- 輸入法自【拼音/注音輸入列】接收：羅馬拼音字母/注音符號後，在【候選字清單】的顯示，格式為：
-- 〔羅馬字母1〕 【注音符號1】  〔羅馬字母2〕 【注音符號2】 …
-- 透過 Lua filter: reformat_comment_filter 重排成：
-- 〔羅馬字母1〕 〔羅馬字母2〕 …  【注音符號1】 【注音符號2】 …
--------------------------------------------------------------------------

local function format_comment(s, display_roman)
	if type(s) ~= "string" or s == "" then
		return s
	end
	local tlpa, zu_im = {}, {}

	for t in s:gmatch("〔(.-)〕") do
		table.insert(tlpa, t)
	end
	for z in s:gmatch("【(.-)】") do
		table.insert(zu_im, z)
	end

	if #tlpa == 0 then
		return s
	end

	if display_roman then
		local new_zu_im = {}
		for i, t in ipairs(tlpa) do
			local roman = convert_15_to_roman(t)
			new_zu_im[i] = roman and roman or (zu_im[i] or "")
		end
		zu_im = new_zu_im
	end

	if #tlpa >= 2 and #tlpa == #zu_im then
		return "〔"
			.. table.concat(tlpa, "〕 〔")
			.. "〕"
			.. "  "
			.. "【"
			.. table.concat(zu_im, "】 【")
			.. "】"
	end

	-- 單字處理時，如果有切換模式，也要套用新格式
	local prefix = s:match("^(%s*)") or ""
	if display_roman and #tlpa == 1 and #zu_im == 1 then
		return prefix .. "〔" .. tlpa[1] .. "〕【" .. zu_im[1] .. "】"
	end

	return s
end

function reformat_comment_filter(input, env)
	-- 取得模式設定（開關 dict_mode 是否為開啟狀態）
	local display_roman = env.engine.context:get_option("dict_mode")
	for cand in input:iter() do
		local old = cand.comment or ""
		local new = format_comment(old, display_roman)

		if true then
			local c = cand:get_genuine()
			local nc = Candidate(c.type, c.start, c._end, c.text, new)
			nc.preedit = cand.preedit
			nc.quality = cand.quality
			yield(nc)
		else
			yield(cand)
		end
	end
end

-----------------------------------------------------------------------
