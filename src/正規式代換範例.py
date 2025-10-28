import re

pattern = r"〔([^〕]*)O([^〕]*)〕"
replacement = r"〔\1o\2〕"

tests = ["〔hOng5〕", "〔hO7〕", "〔Oa1〕"]
for t in tests:
    print(re.sub(pattern, replacement, t))
