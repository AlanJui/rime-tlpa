# BP i/u 與鼻化韻 逐條測試字串清單

## 使用方式
1. 方案切到 phing_im_bp。
2. 每次輸入下表一條字串。
3. 觀察候選清單左欄（BP）是否符合預期關鍵結果。
4. 建議優先檢查前綴是否正確：
   - i 系列：yi 或 y
   - u 系列：wu 或 w
   - 鼻化韻：n 開頭（如 ni, niao, nua, nui）

## A. i 開頭（含鼻化韻）

| 勾選 | 測試輸入 | 預期關鍵結果 | 覆蓋項目 |
|---|---|---|---|
| ☐ | i1 | yi1 | i |
| ☐ | ih4 | yih4 | ih |
| ☐ | inn1 | ni1 | ni |
| ☐ | im1 | yim1 | im |
| ☐ | ip8 | yip8 | ip |
| ☐ | ing1 | ying1 | ing |
| ☐ | ik8 | yik8 | ik |
| ☐ | in1 | yin1 | in |
| ☐ | it8 | yit8 | it |
| ☐ | iau1 | yao1 | iao |
| ☐ | iauh4 | yaoh4 | iaoh |
| ☐ | iaunn2 | niao2 | niao |
| ☐ | ia1 | ya1 | ia |
| ☐ | iah4 | yah4 | iah |
| ☐ | iann2 | nia2 | nia |
| ☐ | iannh4 | niah4 | niah |
| ☐ | ioonn5 | nioo5 | nioo |
| ☐ | io1 | yo1 | io |
| ☐ | ioh4 | yoh4 | ioh |
| ☐ | iu1 | yu1 | iu |
| ☐ | iunn2 | niu2 | niu |
| ☐ | iunnh4 | niuh4 | niuh |
| ☐ | iam3 | yam3 | iam |
| ☐ | iap8 | yap8 | iap |
| ☐ | iong2 | yong2 | iong |
| ☐ | iok8 | yok8 | iok |
| ☐ | iang1 | yang1 | iang |
| ☐ | iak8 | yak8 | iak |
| ☐ | ian2 | yan2 | ian |
| ☐ | iat8 | yat8 | iat |

## B. u 開頭（含鼻化韻）

| 勾選 | 測試輸入 | 預期關鍵結果 | 覆蓋項目 |
|---|---|---|---|
| ☐ | u1 | wu1 | u |
| ☐ | uh4 | wuh4 | uh |
| ☐ | ua1 | wa1 | ua |
| ☐ | uah4 | wah4 | uah |
| ☐ | uann2 | nua2 | nua |
| ☐ | uai1 | wai1 | uai |
| ☐ | uaih4 | waih4 | uaih |
| ☐ | uainn2 | nuai2 | nuai |
| ☐ | uainnh4 | nuaih4 | nuaih |
| ☐ | uan2 | wan2 | uan |
| ☐ | uat8 | wat8 | uat |
| ☐ | uang1 | wang1 | uang |
| ☐ | ue3 | we3 | ue |
| ☐ | ueh4 | weh4 | ueh |
| ☐ | ui7 | wi7 | ui |
| ☐ | uih4 | wih4 | uih |
| ☐ | uinn2 | nui2 | nui |
| ☐ | un2 | wun2 | un |
| ☐ | ut8 | wut8 | ut |

## C. 連續輸入（多音節）回歸測試

| 勾選 | 測試輸入 | 預期關鍵結果 |
|---|---|---|
| ☐ | hong5 ho5 uan2 it4 | 第 3 音節為 wan，第 4 音節為 yit |
| ☐ | iaunn2 iat8 uinn2 ueh4 | 依序含 niao, yat, nui, weh |
| ☐ | i1 uh4 iau1 uai1 | 依序含 yi, wuh, yao, wai |
| ☐ | iann2 iunnh4 uainnh4 | 依序含 nia, niuh, nuaih |

## 驗收準則（通過條件）
1. i/u 開頭規則正確分流：
   - i 或 i+韻尾（m/n/ng/p/t/k/h）前加 y（yi...）
   - ia/io/iu 系列改寫成 y...
   - u 或 u+韻尾（n/t/h）前加 w（wu...）
   - ua/ui/ue 系列改寫成 w...
2. 鼻化韻（nn）會先轉 n 前綴，不可被誤改成 y/w 前綴。
3. 多音節輸入時，每個音節都要被轉換，不能只命中第一個音節。
