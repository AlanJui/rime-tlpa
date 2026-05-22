-- group_tlpa_bpmf.lua
-- 重新組織候選字註解格式：將交替的拼音注音格式改為分組格式
-- 例如：〔gim1〕 【ㄍㄧㆬˉ】  〔ya6〕 【ㄧㄚ^】
-- 改為：〔gim1〕 〔ya6〕  【ㄍㄧㆬˉ】 【ㄧㄚ^】

local function group_tlpa_bpmf_filter(input, env)
  -- 錯誤處理：確保函數不會因為異常而中斷
  local function safe_process(cand)
    local comment = cand.comment or ""
    
    -- 如果沒有註解或註解為空，直接返回原候選
    if comment == "" then
      return cand
    end
    
    -- 收集所有拼音和注音
    local tlpas, bpmfs = {}, {}
    
    -- 提取所有 〔拼音〕
    for tlpa in comment:gmatch("〔([^〕]*)〕") do
      table.insert(tlpas, tlpa)
    end
    
    -- 提取所有 【注音】
    local bpmf_count = 0
    for bpmf in comment:gmatch("【([^】]*)】") do
      table.insert(bpmfs, bpmf)
      bpmf_count = bpmf_count + 1
    end
    
    -- 只有在有多個音節時才重組
    if #tlpas >= 2 and #bpmfs >= 2 then
      -- 重組格式：所有拼音在前，所有注音在後
      local tlpa_part = "〔" .. table.concat(tlpas, "〕 〔") .. "〕"
      local bpmf_part = "【" .. table.concat(bpmfs, "】 【") .. "】"
      local new_comment = tlpa_part .. "  " .. bpmf_part
      
      -- 創建新的候選項
      local new_cand = cand:clone()
      new_cand.comment = new_comment
      return new_cand
    end
    
    -- 如果不需要重組或只有單個音節，返回原候選
    return cand
  end
  
  -- 主處理循環
  for cand in input:iter() do
    local result_cand = safe_process(cand)
    yield(result_cand)
  end
end

-- 返回 filter 函數
return group_tlpa_bpmf_filter
