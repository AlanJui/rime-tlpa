local function contains(array, element)
    for _, value in pairs(array) do
        if value == element then
            return true
        end
    end
    return false
end

local function num2suzhou(num)
    local suzhou = {"〇", "〡", "〢", "〣", "〤", "〥", "〦", "〧", "〨", "〩"}
    local horizontalSuzhou = {"一", "二", "三"}
    local oneTwoThree = {table.unpack(suzhou, 2, 4)}  -- {"〡", "〢", "〣"}
    local result = ""
    if num == nil then return "" end
    -- 遍历整个字符串
    for pos = 1, string.len(num) do
        -- 将每个字符转为数字
        digit = tonumber(string.sub(num, pos, pos))
        if pos > 1 then
            -- 数字若为 {"〡", "〢", "〣"}
            if digit > 0 and digit < 4 then
                -- 且前一个字符也为 {"〡", "〢", "〣"}
                -- `-3` 即取末一个汉字，utf-8 中一个汉字 3 字节
                if contains(oneTwoThree, string.sub(result, -3)) then
                    -- 就使用横式的 {"一", "二", "三"}
                    result = result .. horizontalSuzhou[digit]
                    goto continue
                end
            end
        end
        -- 其他情况或其他数字都使用竖式
        result = result .. suzhou[digit + 1]
        ::continue::
    end
    return result
end

-- 若输入数字带有小数，将其切分为整数、小数点、小数 3 个部分
local function splitNumPart(str)
    local part = {}
    part.int, part.dot, part.dec = string.match(str, "^(%d*)(%.?)(%d*)")
    return part
end

-- 字符串处理流程
function numberTranslatorFunc(num)
    -- 切分小数
    local numberPart = splitNumPart(num)
    local result = {}
    -- 整数和小数部分分别用 num2suzhou() 转换，再将整数、小数点、小数三者连起来
    -- 最后将结果存入 result
    table.insert(
        result,
        {
            -- 候选结果
            num2suzhou(numberPart.int) .. numberPart.dot .. num2suzhou(numberPart.dec),
            -- 候选备注
            "〔蘇州碼〕"
        }
    )
    return result
end

-- 接入 RIME 引擎
function translator(input, seg)
    local str, num, numberPart
    -- 匹配 "S + 数字 + 小数点（可有可无） + 数字（可有可无）" 的模版
    if string.match(input, "^(S%d+)(%.?)(%d*)$") ~= nil then
        -- 去除字符串首的字母
        str = string.gsub(input, "^(%a+)", "")
        numberPart = numberTranslatorFunc(str)
        if #numberPart > 0 then
            for i = 1, #numberPart do
                -- numberTranslatorFunc()
                yield(
                    Candidate(
                        input,
                        seg.start,
                        seg._end,
                        numberPart[i][1],   -- 候选结果
                        numberPart[i][2]    -- 候选备注
                    )
                )
            end
        end
    end
end

return translator
