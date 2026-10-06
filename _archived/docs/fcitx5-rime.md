# Fcitx5-RIME 安裝指引 R7

在 Ubuntu / LinuxMing / DeepIn / ArchLinux... 作業系統的 Fcitx(小企鵝) 輸入法平台安裝【中州韻】輸入法。

## (1) 下載 rime-tlpa 輸入法


```
mkdir ~/tmp && cd $_
git clone https://github.com/AlanJui/rime-tlpa.git
cd rime-tlpa
```

## (2) 安裝輸入法

將 rime-tlpa 使用的輸入法設定檔，安裝到 Fcitx 輸入法平台的預設目錄路徑： `/usr/share/rime-data/default.yaml` 。

```
sudo cp *.yaml /usr/share/rime-data
```

## (3) 啟用 rime-tlpa 輸入法

變更 RIME 輸入法平台的設定，以便啟用 rime-tlpa 輸入法。RIME 輸入法平台的設定檔，存放於目錄路徑： /usr/share/rime-data/default.yaml 。

```shell
sudo vim /usr/share/rime-data/default.yaml .
```

設定檔的變更結果如下：

```shell
# Rime default settings
# encoding: utf-8

config_version: '0.40'

schema_list:
   - {schema: tlpa_peh_ue}               # 河洛白話（使用TLPA拼音輸入）
    - {schema: tlpa_peh_ue_cu_im}       # 河洛白話注音（使用拼音輸入，顯示注音符號標讀音）
    - {schema: tlpa_peh_ue_hong_im}     # 河洛白話方音（使用拼音輸入，顯示方音符號標讀音）
    - {schema: tlpa_peh_ue_cap_peh_im}  # 河洛白話十八音（使用拼音輸入，顯示十八音標讀音）
    #------------------------------------
    - {schema: tlpa_cu_im}          # 河洛注音
    - {schema: tlpa_holok_piau_im}  # 河洛標音（用注音符號標注音）
    - {schema: tlpa_hong_im}        # 河洛方音
    #------------------------------------
    - {schema: tlpa_sip_ngoo_im}    # 河洛十五音（使用雅俗通十五音韻書）
    - {schema: tlpa_kong_un}        # 河洛廣韻
    - {schema: tlpa_hong_im_kb}     # 方音按鍵練習
    #------------------------------------

patch:
  "style/font_face": "Iansui 094, Noto Sans CJK TC"
  "style/font_point": 28
  "style/horizontal": false

switcher:
  ......
```

## (4) 重新啟動 RIME 平台

重新啟動 RIME 輸入法平台，以便 RIME 設定檔的變更能夠立即生效，以便啟用 rime-tlpa 輸入法。

![Restart Fcitx 5](https://github.com/AlanJui/rime-tlpa/blob/main/docs/static/img/Fcitx_Restart.png)