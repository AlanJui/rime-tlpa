--[[
輸入字串格式：〔biek8〕 【ㄅㄧㆤㆻ˙】  〔sui2〕 【ㄙㄨㄧˋ】

輸出字串格式：
  〔biek8〕〔sui2〕  【ㄅㄧㆤㆻ˙】 【ㄙㄨㄧˋ】

程式碼說明：
  1. 抓出所有 〔...〕 放入 tlpa 陣列
  2. 抓出所有 【...】 放入 zh 陣列
  3. 如果兩陣列數量相同且 >= 2，則重組輸出
  4. 否則原樣輸出

正規表達式說明：
  "〔(.-)〕"：非貪婪模式，匹配最短的內容
  "(.-)" 是 Lua 樣式的非貪婪擷取，會吃到下一個對應括號為止；
  這樣即使中間有奇怪的空白、零寬字元、或你實際上用的是另一個很像的右括號，都比較不易誤判。
--]]
local function regroup_pairs_safe(s)
  if type(s) ~= "string" or s == "" then return s end
  local tlpa, zh = {}, {}

  -- 抓所有 〔...〕（最小擷取）
  for t in s:gmatch("〔(.-)〕") do
    table.insert(tlpa, t)
  end

  -- 抓所有 【...】（最小擷取）
  for z in s:gmatch("【(.-)】") do
    table.insert(zh, z)
  end

  if #tlpa >= 2 and #tlpa == #zh then
    return "〔" .. table.concat(tlpa, "〕〔") .. "〕"
           .. "  "
           .. "【" .. table.concat(zh, "】 【") .. "】"
  end
  return s
end

local comment_str = "〔biek8〕 【ㄅㄧㆤㆻ˙】  〔sui2〕 【ㄙㄨㄧˋ】"
-- print(regroup_pairs_safe(comment_str))
local result = regroup_pairs_safe(comment_str)
-- 預期：〔biek8〕〔sui2〕  【ㄅㄧㆤㆻ˙】 【ㄙㄨㄧˋ】
local expected = "〔biek8〕〔sui2〕  【ㄅㄧㆤㆻ˙】 【ㄙㄨㄧˋ】"
print(assert(result == expected))
