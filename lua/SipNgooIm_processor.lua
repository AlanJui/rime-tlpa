-- C:\Users\AlanJui\AppData\Roaming\Rime\lua\SipNgooIm_processor.lua
local function processor(key_event, env)
    local engine = env.engine
    local context = engine.context
    local input = context.input -- 獲取原始輸入，如 "hing5"

    -- 調試訊息
    log.info("sip_ngoo_im: Processor loaded")
    log.info("Key pressed: " .. key_event:repr())
    log.info("Input: " .. input)

    -- 檢測 Ctrl+Return
    local key_repr = key_event:repr()
    if key_repr == "Control+Return" or key_repr == "Control+return" then
        log.info("Ctrl+Return detected")
        if input and input ~= "" then
            -- 定義轉換函數
            local function to_sip_ngoo(input)
                -- 聲母映射
                local initials = {
                    h = "喜", p = "邊", ph = "頗", m = "毛", b = "門",
                    t = "地", th = "他", n = "耐", l = "柳",
                    k = "求", kh = "去", g = "語", ng = "雅",
                    z = "曾", c = "出", s = "時", j = "入", [""] = "英"
                }
                -- 韻母映射
                local finals = {
                    ing = "經", im = "金", in = "巾",
                    ang = "江", an = "干", am = "甘"
                    -- 可擴展其他韻母...
                }
                -- 調號映射
                local tones = {
                    ["1"] = "一", ["2"] = "二", ["3"] = "三",
                    ["5"] = "五", ["7"] = "七", ["4"] = "四", ["8"] = "八"
                }

                -- 分解輸入
                local init = input:match("^([ptk]?h?|[bmgzncjls]?g?)")
                local fin = input:match("[ptk]?h?(.*[mng])[0-8]?$") or input:match("[ptk]?h?(.*)[0-8]?$")
                local tone = input:match("([0-8])$") or "1"

                -- 轉換
                local i = initials[init] or "英"
                local f = finals[fin] or fin -- 若無映射，保留原始
                local t = tones[tone] or "一"
                return f .. t .. i -- 韻調聲順序
            end

            local sip_ngoo = to_sip_ngoo(input)
            log.info("Converted to: " .. sip_ngoo)
            engine:commit_text(sip_ngoo) -- 提交 "經五喜"
            context:clear()
            return 1
        end
        return 1 -- 無輸入時仍標記已處理
    end

    return 2
end

return {
    processor = processor
}

