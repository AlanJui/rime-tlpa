-- 【漢字附帶標音】設定檔
-- 供 rime.lua 之 aux_commit（Ctrl+Shift+Enter：輸出漢字附帶標音）使用。
-- 存放路徑：
--   開發環境： [ProjectRootDir]\lua\rime_env.lua
--   執行環境： [AppDataRootDir]\Roaming\Rime\lua\rime_env.lua
local config = {
    -- 輸入法識別號（schema_id）與其【漢字附帶標音】使用之標音系統。
    -- 設定值須為《變更【漢字標音選項】》章節所定義之選項名稱（key_in_piau_im_*）。
    -- 【註】此表為「方案未提供 key_in_piau_im_* 選項群」時之預設值；
    --       方案選單（F4）已切換選項者，以選單目前狀態為準。
    schema_id = {
        -- 反切輸入法類型
        huan_ciat_tlpa = "key_in_piau_im_tlpa", -- 台語音標
        huan_ciat_tps = "key_in_piau_im_tlpa", -- 台語音標（預設：方音符號 key_in_piau_im_tps）
        huan_ciat_ZapGooIm_bpm2 = "key_in_piau_im_bpm2", -- 台語注音二式（舊 schema_id）
        -- 十五音輸入法【韻+調+聲】（現行 sip_ngoo_im_*）
        -- sip_ngoo_im_tlpa = "key_in_piau_im_tlpa", -- 舊 schema_id（已更名）
        sip_ngoo_im_tl = "key_in_piau_im_tl", -- 台羅拼音（現行 schema_id）
        sip_ngoo_im_tps = "key_in_piau_im_tps", -- 方音符號
        sip_ngoo_im_bpm2 = "key_in_piau_im_bpm2", -- 台語注音二式
        -- 十八音輸入法（改良式新十五音，台羅拼音）
        tsap_peh_im_tl = "key_in_piau_im_tl", -- 台羅拼音
        -- 注音輸入法類型
        zu_im_bpm2 = "key_in_piau_im_bpm2", -- 台語注音二式
        zu_im_tlpa = "key_in_piau_im_tlpa_zu_im", -- 台語音標注音
        zu_im_tps = "key_in_piau_im_tps", -- 方音符號
        -- 拼音輸入法類型
        phing_im_bp = "key_in_piau_im_bp", -- 閩拼方案
        phing_im_bpm2 = "key_in_piau_im_bpm2", -- 台語注音二式
        phing_im_poj = "key_in_piau_im_poj", -- 白話字
        phing_im_tl = "key_in_piau_im_tl", -- 台羅拼音
        phing_im_tlpa = "key_in_piau_im_tlpa", -- 台語音標
    },
    -- 漢字標音用符號
    han_ji_piau_im_hu_ho = {
        left = "〔", -- 左分隔符號
        right = "〕", -- 右分隔符號
        im_zat = "-", -- 音節串接符號，多為【-】或【空白字元】兩種字元
    },
}

return config
