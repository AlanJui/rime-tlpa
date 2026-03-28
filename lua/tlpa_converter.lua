-- lua/tlpa_converter.lua
-- TLPA（台語音標）→ 各閩南話標音系統 轉換模組
-- 相容 Lua 5.1（使用 \NNN 十進位跳脫，不使用 \xNN）
--
-- 支援轉換目標：
--   '十五音'   - 韻調聲格式，如 "公一地"
--   '方音符號' - TPS，如 "ㄉㆲ"
--   '國際音標' - IPA，如 "tɔŋ1"
--   '台語音標' - TLPA（原文還原），如 "tong1"
--   '台羅拼音' - TL，如 "tong"（含調符）
--   '白話字'   - POJ，如 "tong"（含調符）
--   '閩拼方案' - BP，如 "dōng"（含調符）
--   '閩拼調號' - BP2，如 "dong1"（含調號）
--
-- 使用方式：
--   local conv = require("tlpa_converter")
--   print(conv.convert("tong1", "十五音"))   -- "公一地"
--   print(conv.convert("hoo5",  "白話字"))   -- "hô͘"
--   print(conv.convert("ka1",   "台羅拼音")) -- "ka"

local M = {}

-- ============================================================
-- 聲母對照表（以台語音標為鍵）
-- 欄位：sni=十五音, tps=方音符號, ipa=國際音標, bp=閩拼方案
-- ============================================================
local INITIALS = {
    l   = {sni="柳", tps="ㄌ", ipa="l",    bp="l"   },
    p   = {sni="邊", tps="ㄅ", ipa="p",    bp="b"   },
    k   = {sni="求", tps="ㄍ", ipa="k",    bp="g"   },
    kh  = {sni="去", tps="ㄎ", ipa="k\202\176",  bp="k"   },  -- kʰ
    t   = {sni="地", tps="ㄉ", ipa="t",    bp="d"   },
    ph  = {sni="頗", tps="ㄆ", ipa="p\202\176",  bp="p"   },  -- pʰ
    th  = {sni="他", tps="ㄊ", ipa="t\202\176",  bp="t"   },  -- tʰ
    z   = {sni="曾", tps="ㄗ", ipa="\202\166",   bp="z"   },  -- ʦ
    j   = {sni="入", tps="ㆡ", ipa="\202\163",   bp="zz"  },  -- ʣ
    s   = {sni="時", tps="ㄙ", ipa="s",    bp="s"   },
    b   = {sni="門", tps="ㆠ", ipa="b",    bp="bb"  },
    g   = {sni="語", tps="ㆣ", ipa="\201\161",   bp="gg"  },  -- ɡ
    c   = {sni="出", tps="ㄘ", ipa="\202\166\202\176", bp="c" }, -- ʦʰ
    h   = {sni="喜", tps="ㄏ", ipa="h",    bp="h"   },
    m   = {sni="毛", tps="ㄇ", ipa="m",    bp="bbn" },
    n   = {sni="耐", tps="ㄋ", ipa="n",    bp="ln"  },
    ng  = {sni="雅", tps="ㄫ", ipa="\197\139",   bp="ggn" },  -- ŋ
    ji  = {sni="入", tps="ㆢ", ipa="\202\165",   bp="zzi" },  -- ʥ
    zi  = {sni="曾", tps="ㄐ", ipa="\202\168",   bp="zi"  },  -- ʨ
    ci  = {sni="出", tps="ㄑ", ipa="\202\168\202\176", bp="ci" }, -- ʨʰ
    si  = {sni="時", tps="ㄒ", ipa="\201\149",   bp="si"  },  -- ɕ
    -- 零聲母（英）
    ["\195\184"] = {sni="英", tps="\195\152", ipa="", bp="\195\152"},  -- ø → Ø
    ["\195\152"] = {sni="英", tps="\195\152", ipa="", bp="\195\152"},  -- Ø
}
-- 別名：ts=z, tsh=c（接受台羅拼音聲母輸入）
INITIALS["ts"]  = INITIALS["z"]
INITIALS["tsh"] = INITIALS["c"]
INITIALS["bb"]  = INITIALS["b"]
INITIALS["gg"]  = INITIALS["g"]

-- ============================================================
-- 韻母對照表（以台語音標為鍵）
-- 欄位：sni=十五音, tps=方音符號, ipa=國際音標
-- ============================================================
-- IPA 促聲尾：U+031A 未除阻符號 = \204\154（\xCC\x9A）
local _ua = "\204\154"

local FINALS = {
    -- 君韻
    un     = {sni="君", tps="ㄨㄣ",   ipa="un"        },
    ut     = {sni="君", tps="ㄨㆵ",   ipa="ut".._ua   },
    -- 堅韻
    ian    = {sni="堅", tps="ㄧㄢ",   ipa="ian"       },
    iat    = {sni="堅", tps="ㄧㄚㆵ", ipa="iat".._ua  },
    -- 金韻
    im     = {sni="金", tps="ㄧㆬ",   ipa="im"        },
    ip     = {sni="金", tps="一ㆴ",   ipa="ip".._ua   },
    -- 規韻
    ui     = {sni="規", tps="ㄨㄧ",   ipa="ui"        },
    -- 嘉韻
    ee     = {sni="嘉", tps="ㄝ",     ipa="\201\155"  },  -- ɛ
    eeh    = {sni="嘉", tps="ㄝㆷ",   ipa="\201\155\202\148" }, -- ɛʔ
    -- 干韻
    an     = {sni="干", tps="ㄢ",     ipa="an"        },
    at     = {sni="干", tps="ㄚㆵ",   ipa="at".._ua   },
    -- 公韻
    ong    = {sni="公", tps="ㆲ",     ipa="\201\148\197\139" }, -- ɔŋ
    ok     = {sni="公", tps="ㆦㆻ",   ipa="\201\148k".._ua }, -- ɔk̚
    -- 乖韻
    uai    = {sni="乖", tps="ㄨㄞ",   ipa="uai"       },
    uaih   = {sni="乖", tps="ㄨㄞㆷ", ipa="uai\202\148" }, -- uaiʔ
    -- 經韻
    ing    = {sni="經", tps="ㄧㄥ",   ipa="i\197\139" },  -- iŋ
    ik     = {sni="經", tps="ㄧㆻ",   ipa="ik".._ua   },
    -- 觀韻
    uan    = {sni="觀", tps="ㄨㄢ",   ipa="uan"       },
    uat    = {sni="觀", tps="ㄨㄚㆵ", ipa="uat".._ua  },
    -- 沽韻
    oo     = {sni="沽", tps="ㆦ",     ipa="ou"        },
    -- 嬌韻
    iau    = {sni="嬌", tps="ㄧㄠ",   ipa="iau"       },
    iauh   = {sni="嬌", tps="ㄧㄠㆷ", ipa="iau\202\148" }, -- iauʔ
    -- 稽韻
    ei     = {sni="稽", tps="ㆤ",     ipa="ei"        },
    -- 恭韻
    iong   = {sni="恭", tps="ㄧㆲ",   ipa="i\201\148\197\139" }, -- iɔŋ
    iok    = {sni="恭", tps="ㄧㆦㆻ", ipa="i\201\148k".._ua }, -- iɔk̚
    -- 高韻
    o      = {sni="高", tps="ㄜ",     ipa="o"         },
    oh     = {sni="高", tps="ㄜㆷ",   ipa="o\202\148" },  -- oʔ
    -- 皆韻
    ai     = {sni="皆", tps="ㄞ",     ipa="ai"        },
    -- 巾韻
    ["in"] = {sni="巾", tps="ㄧㄣ",   ipa="in"        },
    it     = {sni="巾", tps="ㄧㆵ",   ipa="it".._ua   },
    -- 姜韻
    iang   = {sni="姜", tps="ㄧㄤ",   ipa="ia\197\139" }, -- iaŋ
    iak    = {sni="姜", tps="ㄧㄚㆻ", ipa="iak".._ua  },
    -- 甘韻
    am     = {sni="甘", tps="ㆰ",     ipa="am"        },
    ap     = {sni="甘", tps="ㄚㆴ",   ipa="ap".._ua   },
    -- 瓜韻
    ua     = {sni="瓜", tps="ㄨㄚ",   ipa="ua"        },
    uah    = {sni="瓜", tps="ㄨㄚㆷ", ipa="ua\202\148" }, -- uaʔ
    -- 江韻
    ang    = {sni="江", tps="ㄤ",     ipa="a\197\139" },  -- aŋ
    ak     = {sni="江", tps="ㄚㆻ",   ipa="ak".._ua   },
    -- 兼韻
    iam    = {sni="兼", tps="ㄧㆰ",   ipa="iam"       },
    iap    = {sni="兼", tps="ㄧㄚㆴ", ipa="iap".._ua  },
    -- 交韻
    au     = {sni="交", tps="ㄠ",     ipa="au"        },
    auh    = {sni="交", tps="ㄠㆷ",   ipa="au\202\148" }, -- auʔ
    -- 迦韻
    ia     = {sni="迦", tps="ㄧㄚ",   ipa="ia"        },
    iah    = {sni="迦", tps="ㄧㄚㆷ", ipa="ia\202\148" }, -- iaʔ
    -- 檜韻
    ue     = {sni="檜", tps="ㄨㆤ",   ipa="uei"       },
    ueh    = {sni="檜", tps="ㄨㆤㆷ", ipa="uei\202\148" }, -- ueiʔ
    -- 監韻（鼻化）
    ann    = {sni="監", tps="ㆩ",     ipa="\195\163"  },  -- ã
    ahnn   = {sni="監", tps="ㆩㆷ",   ipa="\195\163\202\148" }, -- ãʔ
    -- 艍韻
    u      = {sni="艍", tps="ㄨ",     ipa="u"         },
    uh     = {sni="艍", tps="ㄨㆷ",   ipa="u\202\148" },  -- uʔ
    -- 膠韻
    a      = {sni="膠", tps="ㄚ",     ipa="a"         },
    ah     = {sni="膠", tps="ㄚㆷ",   ipa="a\202\148" },  -- aʔ
    -- 居韻
    i      = {sni="居", tps="ㄧ",     ipa="i"         },
    ih     = {sni="居", tps="ㄧㆷ",   ipa="i\202\148" },  -- iʔ
    -- 丩韻
    iu     = {sni="丩", tps="ㄧㄨ",   ipa="iu"        },
    -- 更韻（鼻化）
    enn    = {sni="更", tps="ㆥ",     ipa="\201\155\204\131" }, -- ɛ̃（ɛ + combining tilde）
    ehnn   = {sni="更", tps="ㆥㆷ",   ipa="\201\155\204\131\202\148" }, -- ɛ̃ʔ
    -- 褌韻（鼻化）
    uinn   = {sni="褌", tps="ㄨㆪ",   ipa="ui\204\131" }, -- uĩ
    -- 茄韻
    io     = {sni="茄", tps="ㄧㄜ",   ipa="io"        },
    ioh    = {sni="茄", tps="ㄧㄜㆷ", ipa="io\202\148" }, -- ioʔ
    -- 梔韻（鼻化）
    inn    = {sni="梔", tps="ㆪ",     ipa="i\204\131" },  -- ĩ
    ihnn   = {sni="梔", tps="ㆪㆷ",   ipa="i\204\131\202\148" }, -- ĩʔ
    -- 薑韻（鼻化）
    ionn   = {sni="薑", tps="ㄧㆧ",   ipa="i\201\148\204\131" }, -- iɔ̃
    -- 驚韻（鼻化）
    iann   = {sni="驚", tps="ㄧㆩ",   ipa="i\195\163" }, -- iã
    -- 官韻（鼻化）
    uann   = {sni="官", tps="ㄨㆩ",   ipa="u\195\163" }, -- uã
    -- 鋼韻（成音節鼻音）
    ng     = {sni="鋼", tps="ㆭ",     ipa="\197\139\204\141" }, -- ŋ̍
    -- 伽韻
    e      = {sni="伽", tps="ㆤ",     ipa="e"         },
    eh     = {sni="伽", tps="ㆤㆷ",   ipa="e\202\148" },  -- eʔ
    -- 閒韻（鼻化）
    ainn   = {sni="閒", tps="ㆮ",     ipa="\195\163i" }, -- ãi
    -- 姑韻（鼻化）
    oonn   = {sni="姑", tps="ㆧ",     ipa="\195\181u" }, -- õu
    -- 姆韻（成音節鼻音）
    m      = {sni="姆", tps="ㆬ",     ipa="m\204\169" }, -- m̩（m + combining vertical line below）
    -- 光韻
    uang   = {sni="光", tps="ㄨㄤ",   ipa="ua\197\139" }, -- uaŋ
    uak    = {sni="光", tps="ㄨㄚㆻ", ipa="uak".._ua  },
    -- 閂韻（鼻化）
    uainn  = {sni="閂", tps="ㄨㆮ",   ipa="u\195\163i" }, -- uãi
    uaihnn = {sni="閂", tps="ㄨㆮㆷ", ipa="u\195\163i\202\148" }, -- uãiʔ
    -- 糜韻（鼻化）
    uenn   = {sni="糜", tps="ㄨㆥ",   ipa="u\196\169i" }, -- uẽi（ẽ = e + combining tilde）
    -- 嘄韻（鼻化）
    iaunn  = {sni="嘄", tps="ㄧㆯ",   ipa="i\195\163u" }, -- iãu
    iauhnn = {sni="嘄", tps="ㄧㆯㆷ", ipa="i\195\163u\202\148" }, -- iãuʔ
    -- 箴韻
    om     = {sni="箴", tps="ㆱ",     ipa="\201\148m" }, -- ɔm
    op     = {sni="箴", tps="ㆦㆴ",   ipa="\201\148p".._ua }, -- ɔp̚
    -- 爻韻（鼻化）
    aunn   = {sni="爻", tps="ㆯ",     ipa="\195\163u" }, -- ãu
    -- 扛韻（鼻化）
    onn    = {sni="扛", tps="ㆧ",     ipa="\195\181"  }, -- õ
    ohnn   = {sni="扛", tps="ㆧㆷ",   ipa="\195\181\202\148" }, -- õʔ
    -- 牛韻（鼻化）
    iunn   = {sni="牛", tps="ㄧㆫ",   ipa="i\204\131u" }, -- ĩu
}

-- ============================================================
-- 內部工具函數
-- ============================================================

-- 移除 UTF-8 連接調符（U+0300–U+036F）
-- 在 Lua 5.1 中使用十進制跳脫：
--   U+0300–U+033F = byte1:204(\204), byte2:128-191(\128-\191)
--   U+0340–U+036F = byte1:205(\205), byte2:128-175(\128-\175)
local function strip_diacritics(s)
    s = s:gsub("\204[\128-\191]", "")
    s = s:gsub("\205[\128-\175]", "")
    return s
end

-- 切分 TLPA 音節為 {siann, un, tiau}
-- 輸入範例："khing5", "tong1", "a2", "oo7"
-- 輸出範例：{siann="kh", un="ing", tiau="5"}
local function split_tlpa(tlpa)
    if not tlpa or tlpa == "" then return nil end
    local p = tlpa:lower()

    -- 提取末尾聲調數字
    local tiau
    local last = p:sub(-1)
    if last:match("%d") then
        tiau = last
        p = p:sub(1, -2)
    else
        -- 無顯式調號：依韻尾判斷入聲（第 4 調）
        if last == "p" or last == "t" or last == "k" or last == "h" then
            tiau = "4"
        else
            tiau = "1"
        end
    end

    -- 依長度排序比對聲母（longest-match）
    local initials_list = {
        "tsh", "kh", "ph", "th", "ng", "bb", "gg",
        "ts", "z", "c", "p", "k", "t", "l", "s", "h",
        "b", "g", "m", "n", "j"
    }
    local siann = ""
    local un = p
    for _, ini in ipairs(initials_list) do
        if p:sub(1, #ini) == ini then
            siann = ini
            un = p:sub(#ini + 1)
            break
        end
    end
    if siann == "" then
        siann = "\195\184"  -- ø（零聲母，U+00F8）
    end

    return {siann = siann, un = un, tiau = tiau}
end

-- 依優先規則在羅馬拼音中標注調符
-- system: "台羅拼音" | "白話字" | "閩拼方案"
local function apply_tone_mark(base, tiau, system)
    -- Combining diacritical marks（Lua 5.1 十進制跳脫）
    -- U+0301 acute    = \204\129
    -- U+0300 grave    = \204\128
    -- U+0302 circum.  = \204\130
    -- U+030C caron    = \204\140
    -- U+0304 macron   = \204\132
    -- U+030D vert.ln  = \204\141
    local TL_MARKS = {
        ["2"] = "\204\129",
        ["3"] = "\204\128",
        ["5"] = "\204\130",
        ["6"] = "\204\140",
        ["7"] = "\204\132",
        ["8"] = "\204\141",
    }
    local POJ_MARKS = {
        ["2"] = "\204\129",
        ["3"] = "\204\128",
        ["5"] = "\204\130",
        ["7"] = "\204\132",
        ["8"] = "\204\141",
    }
    local BP_MARKS = {
        ["1"] = "\204\132",  -- macron（陰平）
        ["5"] = "\204\129",  -- acute（陽平）
        ["2"] = "\204\140",  -- caron（上聲）
        ["6"] = "\204\140",
        ["3"] = "\204\128",  -- grave（陰去）
        ["7"] = "\204\130",  -- circumflex（陽去）
        ["4"] = "\204\132",  -- macron（陰入）
        ["8"] = "\204\129",  -- acute（陽入）
    }

    local marks
    if system == "白話字" then
        marks = POJ_MARKS
    elseif system == "台羅拼音" then
        marks = TL_MARKS
    else
        marks = BP_MARKS  -- 閩拼方案
    end

    local mark = marks[tiau]
    if not mark then return base end

    -- 移除既有調符，取得乾淨的 ASCII 字串
    local s = strip_diacritics(base)

    -- 依優先順序找標調母音位置（1-based byte index）
    local pos = -1
    if s:find("ere", 1, true) then
        pos = (s:find("ere", 1, true)) + 2  -- 標在最後的 e
    elseif s:find("iu", 1, true) then
        pos = s:find("u", 1, true)           -- iu 標在 u
    elseif s:find("ui", 1, true) then
        pos = s:find("i", 1, true)           -- ui 標在 i
    elseif s:find("oo", 1, true) then
        pos = s:find("o", 1, true)           -- oo 標在第一個 o
    elseif s:find("ng", 1, true) and not s:find("[aeiou]") then
        pos = s:find("n", 1, true)           -- 純 ng 韻標在 n
    elseif not s:find("[aeiou]") and s:find("m", 1, true) then
        pos = s:find("m", 1, true)           -- 純 m 韻標在 m
    else
        -- 響度順序：a > o > e > i > u > v
        for _, v in ipairs({"a", "o", "e", "i", "u", "v"}) do
            local p2 = s:find(v, 1, true)
            if p2 then pos = p2; break end
        end
    end

    local result
    if pos == -1 then
        result = s .. mark
    else
        result = s:sub(1, pos) .. mark .. s:sub(pos + 1)
    end

    -- 白話字特殊處理：oo → o͘（o + U+0358 = \205\152）
    -- U+0358 combining dot above right
    if system == "白話字" and base:find("o\205\152", 1, true) then
        result = result:gsub("o", "o\205\152", 1)
    end

    return result
end

-- ============================================================
-- 主要轉換函數
-- ============================================================

--- 將 TLPA 音節轉換為指定標音系統
-- @param tlpa   string  台語音標字串（如 "ka1", "hoo5", "tong1"）
-- @param target string  目標系統（見模組說明列表）
-- @return string 轉換後的字串
local function convert_tlpa(tlpa, target)
    if not target or target == "" then return "" end
    local parts = split_tlpa(tlpa)
    if not parts then return "" end

    -- 零聲母：ø (U+00F8 = \195\184) 或 Ø (U+00D8 = \195\152)
    local is_zero = (parts.siann == "\195\184" or parts.siann == "\195\152")
    local ini_match = INITIALS[parts.siann]
    local fin_match = FINALS[parts.un]
    local result = ""

    -- ---- 十五音（韻 + 調漢字 + 聲） ----
    if target == "十五音" then
        local i_sni = ini_match and ini_match.sni or (is_zero and "英" or "")
        local f_sni = fin_match and fin_match.sni or ""
        local tone_cn = {"一","二","三","四","五","六","七","八"}
        local t_cn = tone_cn[tonumber(parts.tiau)] or parts.tiau
        result = f_sni .. t_cn .. i_sni

    -- ---- 方音符號（TPS）----
    elseif target == "方音符號" then
        local i_tps = (ini_match and ini_match.tps) or ""
        local f_tps = (fin_match and fin_match.tps) or ""

        -- 顎化規則：韻母以 i 起頭 + 特定聲母
        local sn = parts.siann
        if parts.un:sub(1,1) == "i" then
            if sn == "s" then
                i_tps = "ㄒ"
            elseif sn == "j" or sn == "ji" then
                i_tps = "ㆢ"
            elseif sn == "z" or sn == "ts" then
                i_tps = "ㄐ"
            elseif sn == "c" or sn == "tsh" then
                i_tps = "ㄑ"
            end
        end

        -- 方音調符（U+02CB ˋ, U+02EA ˪, U+02CA ˊ, U+02EB ˫, U+02D9 ˙）
        -- 以 Lua 5.1 十進制：U+02CB=\203\139, U+02EA=\203\170,
        --                    U+02CA=\203\138, U+02EB=\203\171, U+02D9=\203\153
        local tps_tones = {
            ["1"] = "",
            ["2"] = "\203\139",  -- U+02CB ˋ
            ["3"] = "\203\170",  -- U+02EA ˪
            ["4"] = "",
            ["5"] = "\203\138",  -- U+02CA ˊ
            ["6"] = "",
            ["7"] = "\203\171",  -- U+02EB ˫
            ["8"] = "\203\153",  -- U+02D9 ˙
        }
        local t_tps = tps_tones[parts.tiau] or ""

        -- 零聲母符號 Ø 不顯示
        if i_tps == "\195\152" or i_tps == "\195\184" then i_tps = "" end
        result = i_tps .. f_tps .. t_tps

    -- ---- 國際音標（IPA）----
    elseif target == "國際音標" then
        local i_ipa = (ini_match and ini_match.ipa) or ""
        local f_ipa = (fin_match and fin_match.ipa) or parts.un
        if i_ipa == "\195\152" or i_ipa == "\195\184" then i_ipa = "" end
        result = i_ipa .. f_ipa .. parts.tiau  -- 調號以數字附於末尾

    -- ---- 台語音標（TLPA 原文還原）----
    elseif target == "台語音標" then
        local s = is_zero and "" or parts.siann
        result = s .. parts.un .. parts.tiau

    -- ---- 台羅拼音（TL）----
    elseif target == "台羅拼音" then
        local b_siann = is_zero and "" or parts.siann
        local b_un = parts.un
        -- 聲母：z→ts, c→tsh
        if b_siann == "z" then b_siann = "ts" end
        if b_siann == "c" then b_siann = "tsh" end
        result = apply_tone_mark(b_siann .. b_un, parts.tiau, "台羅拼音")

    -- ---- 白話字（POJ）----
    elseif target == "白話字" then
        local b_siann = is_zero and "" or parts.siann
        local b_un = parts.un
        -- 聲母轉換
        if b_siann == "ts" or b_siann == "z" then
            b_siann = "ch"
        elseif b_siann == "tsh" or b_siann == "c" then
            b_siann = "chh"
        end
        -- 韻母鼻化：先處理 nnh→hⁿ，再處理 nn→ⁿ
        -- U+207F ⁿ = \226\129\191（UTF-8 三位元組）
        b_un = b_un:gsub("nnh", "h\226\129\191")
        b_un = b_un:gsub("nn",  "\226\129\191")
        -- 韻母字形轉換
        b_un = b_un:gsub("ue",  "oe")
        b_un = b_un:gsub("ua",  "oa")
        b_un = b_un:gsub("ik",  "ek")
        b_un = b_un:gsub("ing", "eng")
        -- oo → o͘（o + U+0358 = \205\152）
        b_un = b_un:gsub("oo",  "o\205\152")
        result = apply_tone_mark(b_siann .. b_un, parts.tiau, "白話字")

    -- ---- 閩拼方案（BP）/ 閩拼調號（BP2）----
    elseif target == "閩拼方案" or target == "閩拼調號" then
        local b_siann = is_zero and "" or parts.siann
        local b_un = parts.un

        -- 1. 韻母 au → ao
        b_un = b_un:gsub("au", "ao")

        -- 2. 鼻化韻母前置：末尾 nn → n + 核心韻母
        if b_un:sub(-2) == "nn" then
            local core = b_un:sub(1, -3)
            if core == "io" then
                core = "ioo"
            elseif core == "o" then
                core = "oo"
            end
            b_un = "n" .. core
        end

        -- 3. 零聲母 y/w 替換
        if b_siann == "" then
            if b_un:sub(1,1) == "i" then
                b_siann = "y"
                -- i 單獨或後接 n/m/t/p/k/h 時保留 i；其餘去掉前導 i
                if b_un ~= "i" and not b_un:match("^i[nmtpkh]") then
                    b_un = b_un:sub(2)
                end
            elseif b_un:sub(1,1) == "u" then
                b_siann = "w"
                -- u 單獨或後接 n/t/h 時保留 u；其餘去掉前導 u
                if b_un ~= "u" and not b_un:match("^u[nth]") then
                    b_un = b_un:sub(2)
                end
            end
        else
            -- 依對照表取得閩拼方案聲母
            b_siann = (ini_match and ini_match.bp) or b_siann
        end

        if target == "閩拼調號" then
            -- TLPA 調號 → BP 調號對照
            local num_map = {
                ["1"]="1", ["5"]="2", ["2"]="3", ["6"]="4",
                ["3"]="5", ["7"]="6", ["4"]="7", ["8"]="8"
            }
            result = b_siann .. b_un .. (num_map[parts.tiau] or parts.tiau)
        else
            result = apply_tone_mark(b_siann .. b_un, parts.tiau, "閩拼方案")
        end

    else
        -- 未知系統：原樣返回 TLPA
        local s = is_zero and "" or parts.siann
        result = s .. parts.un .. parts.tiau
    end

    return result
end

-- ============================================================
-- 模組公開介面
-- ============================================================
M.convert          = convert_tlpa    -- 主要轉換函數
M.split            = split_tlpa      -- TLPA 切分函數
M.apply_tone_mark  = apply_tone_mark -- 調符標注函數
M.strip_diacritics = strip_diacritics -- 調符移除函數
M.INITIALS         = INITIALS        -- 聲母對照表
M.FINALS           = FINALS          -- 韻母對照表

return M
