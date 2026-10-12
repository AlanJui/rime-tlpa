-- 各輸入方案【方案選項】之初始值（手工維護，勿由程式覆寫）。
-- 方案首次啟用、且 lua/rime_env_state.lua 尚無該項紀錄時，
-- rime.lua 以此檔重設【漢字標音選項】、【音節連接符】、【聲調樣式】、【變調標示】。
-- 使用者按 F4 變更選項後，變更寫入 lua/rime_env_state.lua。
-- 顯示名稱須與各 schema switches 的 states 一致。
-- 方案若未定義某選項群（例如拼音方案沒有【聲調樣式】），該項於啟用時略過。
return {
    -- 十五音輸入法【韻+調+聲】（現行 sip_ngoo_im_*）
    sip_ngoo_im_tl = "台羅拼音", -- 台羅拼音（現行 schema_id）
    sip_ngoo_im_tps = "方音符號", -- 方音符號
    sip_ngoo_im_bpm2 = "台語注音二式", -- 台語注音二式
    -- 十八音輸入法（改良式新十五音）
    tsap_peh_im_tl = "台羅拼音", -- 台羅拼音
    tsap_peh_im_bpm2 = "台語注音二式", -- 台語注音二式
    tsap_peh_im_bp = "閩拼方案", -- 閩拼方案
    tsap_peh_im_tps = "方音符號", -- 方音符號
    -- 注音輸入法類型
    zu_im_bpm2 = "台語注音二式", -- 台語注音二式
    zu_im_tlpa = "台語音標注音", -- 台語音標注音
    zu_im_tps = "方音符號", -- 方音符號
    -- 拼音輸入法類型
    phing_im_bp = "閩拼方案", -- 閩拼方案
    phing_im_bpm2 = "台語注音二式", -- 台語注音二式
    phing_im_poj = "白話字", -- 白話字
    phing_im_tl = "台羅拼音", -- 台羅拼音
    phing_im_tlpa = "台語音標", -- 台語音標
    -- 音節連接符
    im_zat = {
        -- 十五音輸入法【韻+調+聲】（現行 sip_ngoo_im_*）
        sip_ngoo_im_tl = "連字號", -- 台羅拼音（現行 schema_id）
        sip_ngoo_im_tps = "連字號", -- 方音符號
        sip_ngoo_im_bpm2 = "連字號", -- 台語注音二式
        -- 十八音輸入法（改良式新十五音）
        tsap_peh_im_tl = "連字號", -- 台羅拼音
        tsap_peh_im_bpm2 = "連字號", -- 台語注音二式
        tsap_peh_im_bp = "撇號", -- 閩拼方案
        tsap_peh_im_tps = "連字號", -- 方音符號
        -- 注音輸入法類型
        zu_im_bpm2 = "空白", -- 台語注音二式
        zu_im_tlpa = "空白", -- 台語音標注音
        zu_im_tps = "空白", -- 方音符號
        -- 拼音輸入法類型
        phing_im_bp = "撇號", -- 閩拼方案
        phing_im_bpm2 = "連字號", -- 台語注音二式
        phing_im_poj = "連字號", -- 白話字
        phing_im_tl = "連字號", -- 台羅拼音
        phing_im_tlpa = "連字號", -- 台語音標
    },
    -- 聲調樣式
    siann_tiau_iunn_sik = {
        -- 十五音輸入法【韻+調+聲】（現行 sip_ngoo_im_*）
        sip_ngoo_im_tl = "調符", -- 台羅拼音（現行 schema_id）
        sip_ngoo_im_tps = "調符", -- 方音符號
        sip_ngoo_im_bpm2 = "標準調號", -- 台語注音二式
        -- 十八音輸入法（改良式新十五音）
        tsap_peh_im_tl = "調符", -- 台羅拼音
        tsap_peh_im_bpm2 = "標準調號", -- 台語注音二式
        tsap_peh_im_bp = "調符", -- 閩拼方案
        tsap_peh_im_tps = "調符", -- 方音符號
        -- 注音輸入法類型
        zu_im_bpm2 = "標準調號", -- 台語注音二式
        zu_im_tlpa = "標準調號", -- 台語音標注音
        zu_im_tps = "調符", -- 方音符號
        -- 拼音輸入法類型
        phing_im_bp = "調符", -- 閩拼方案
        phing_im_bpm2 = "標準調號", -- 台語注音二式
        phing_im_poj = "調符", -- 白話字
        phing_im_tl = "調符", -- 台羅拼音
        phing_im_tlpa = "標準調號", -- 台語音標
    },
    -- 變調標示
    piau_piann_tiau = {
        -- 十五音輸入法【韻+調+聲】（現行 sip_ngoo_im_*）
        sip_ngoo_im_tl = "無變調", -- 台羅拼音（現行 schema_id）
        sip_ngoo_im_tps = "無變調", -- 方音符號
        sip_ngoo_im_bpm2 = "無變調", -- 台語注音二式
        -- 十八音輸入法（改良式新十五音）
        tsap_peh_im_tl = "無變調", -- 台羅拼音
        tsap_peh_im_bpm2 = "無變調", -- 台語注音二式
        tsap_peh_im_bp = "無變調", -- 閩拼方案
        tsap_peh_im_tps = "無變調", -- 方音符號
        -- 注音輸入法類型
        zu_im_bpm2 = "無變調", -- 台語注音二式
        zu_im_tlpa = "無變調", -- 台語音標注音
        zu_im_tps = "無變調", -- 方音符號
        -- 拼音輸入法類型
        phing_im_bp = "無變調", -- 閩拼方案
        phing_im_bpm2 = "無變調", -- 台語注音二式
        phing_im_poj = "無變調", -- 白話字
        phing_im_tl = "無變調", -- 台羅拼音
        phing_im_tlpa = "無變調", -- 台語音標
    },
}
