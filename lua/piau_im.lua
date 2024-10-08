function piau_im(input, seg)
    -- 定义键与注音符号的映射表
    local key_to_piau_im = {
      ["-"] = "ｎ",
      ["1"] = "ㄅ",
      ["!"] = "ㄅㄏ",
      ["q"] = "ㄆ",
      ["a"] = "ㄇ",
      ["2"] = "ㄉ",
      ["w"] = "ㄊ",
      ["s"] = "ㄋ",
      ["x"] = "ㄌ",
      ["e"] = "ㄍ",
      ["E"] = "ㄍㄏ",
      ["d"] = "ㄎ",
      ["c"] = "ㄏ",
      ["y"] = "ㄗ",
      ["h"] = "ㄘ",
      ["n"] = "ㄙ",
      ["b"] = "ㄖ",
      ["Y"] = "ㄐㄧ",
      ["H"] = "ㄑㄧ",
      ["N"] = "ㄒㄧ",
      ["?"] = "ㄥ",
      ["u"] = "ㄧ",
      ["U"] = "ㄥㄧ",
      ["j"] = "ㄨ",
      ["J"] = "ㄥㄨ",
      ["8"] = "ㄚ",
      ["*"] = "ㄥㄚ",
      [","] = "ㄝ",
      ["<"] = "ㄥㄝ",
      ["i"] = "ㄛ",
      ["I"] = "ㄥㄛ",
      ["k"] = "ㄜ",
      ["0"] = "ㄢ",
      ["9"] = "ㄞ",
      ["("] = "ㄥㄞ",
      ["l"] = "ㄠ",
      ["L"] = "ㄥㄠ",
      ["M"] = "ㄛㄇ",
      ["m"] = "ㄚㄇ",
      [":"] = "ㄛㄥ",
      [";"] = "ㄤ",
      ["o"] = "ㆨ",
      ["/"] = "ㄥ",
      ["A"] = "ㄇ",
      ["p"] = "ㄣ",
      [" "] = "ˉ",
      ["4"] = "ˋ",
      ["3"] = "_",
      ["6"] = "ˇ",
      ["5"] = "+",
      ["7"] = "ˊ",
    }
    
    -- 检查输入的键是否在映射表中
    local cu_im = key_to_piau_im[input]
    if cu_im then
      -- 将注音符号作为候选项
      yield(Candidate("cu_im", seg.start, seg._end, cu_im, "台語音標"))
    end
end

return piau_im

    -- local key_to_piau_im = {
    --   ["ｎ"] = "N",
    --   ["ㆠ"] = "b",
    --   ["ㄆ"] = "ph",
    --   ["ㄇ"] = "m",
    --   ["ㄉ"] = "t",
    --   ["ㄊ"] = "th",
    --   ["ㄋ"] = "n",
    --   ["ㄌ"] = "l",
    --   ["ㄍ"] = "k",
    --   ["ㆣ"] = "g",
    --   ["ㄎ"] = "kh",
    --   ["ㄏ"] = "h",
    --   ["ㄗ"] = "c",
    --   ["ㄘ"] = "ch",
    --   ["ㄙ"] = "s",
    --   ["ㆡ"] = "j",
    --   ["ㄗㄧ"] = "ci-",
    --   ["ㄘㄧ"] = "chi-",
    --   ["ㄙㄧ"] = "si-",
    --   ["ㄫ"] = "ng",
    --   ["ㄧ"] = "i",
    --   ["ㆪ"] = "Ni",
    --   ["ㄨ"] = "u",
    --   ["ㆫ"] = "Nu",
    --   ["ㄚ"] = "a",
    --   ["ㆩ"] = "Na",
    --   ["ㄝ"] = "e",
    --   ["ㆥ"] = "Ne",
    --   ["ㄛ"] = "oo",
    --   ["ㆧ"] = "Noo",
    --   ["ㄜ"] = "o",
    --   ["ㄢ"] = "an",
    --   ["ㄞ"] = "ai",
    --   ["ㆮ"] = "Nai",
    --   ["ㄠ"] = "au",
    --   ["ㆯ"] = "Nau",
    --   ["ㆱ"] = "om",
    --   ["ㆰ"] = "am",
    --   ["ㆲ"] = "ong",
    --   ["ㄤ"] = "ang",
    --   ["ㆨ"] = "ir",
    --   ["ㆭ"] = "ng",
    --   ["ㆬ"] = "m",
    --   ["ㄣ"] = "n",
    --   ["ˉ"] = "1",
    --   ["ˋ"] = "2",
    --   ["˪"] = "3",
    --   ["ˊ"] = "5",
    --   ["˫"] = "7",
    --   ["˙"] = "8",
    -- }
