# 專案摘要

台灣的河洛話（俗稱：台語），傳自遠古漢族人的語言。隨著歷史的推演，朝代的更迭，
可惜這語言不再是漢人使用的官話，故而日常使用變得式微，更糟的是能說一口流利河洛
話的人，亦無法正確地使用漢字書寫河洛話。本專案所發展之【河洛話輸入法】，期待可
協助能說河洛話之人，使用正確的漢字書寫河洛話。

中州韻輸入法引擎（以下簡稱：RIME），是一個跨平台的輸入法框架；或說是：輸入法
執行平台。專案的産出：【河洛話輸入法】，係架構在 RIME 平台之上的輸入法。選擇
RIME 作為輸入法平台，主要是借重 RIME 可於 Windows, macOS, Linux 多種作業系統
運作的特性。

【河洛話輸入法】屬「拼音輸入法」類型，對於「漢字」之注音，採用：
「[臺灣語言音標方案（以下簡稱：TLPA 拼音）](https://zh.wikipedia.org/zh-tw/%E8%87%BA%E7%81%A3%E8%AA%9E%E8%A8%80%E9%9F%B3%E6%A8%99%E6%96%B9%E6%A1%88)」。
方法標注漢字讀音。TLPA 是台灣語文學會於 1991 年期間，針對臺灣主要語言，所制定的
音標系統，適用於為：臺灣閩南語、臺灣客家語、臺灣原住民語標注讀音。之後教育部
更在 2003 年 2 月，將「閩南語」部份與「國際語音符號（國際音標）」、「教會羅馬字
」系統整合，隨後於 2006 年 10 月 14 日公布為「臺灣閩南語羅馬字拼音方案（簡稱：
台羅拼音）」。

河洛話特有的四聲、八調，用於誦讀：古文、詩、詞，乃至經文，總能讓我感受到一股濃濃
的風雅韻味。先祖的漢字、雅音，這個珍貴的遺産，祈願得以永世流傳，不使斷絕！

   - 鼠鬚管：`~/Library/Rime/`(macOS)

   - 小狼毫：`"%APPDATA%\Rime"`(Windows)

   - 中州韻：`~/.config/ibus/rime/`(如：Ubuntu, ArchLinux，採用 Gnome 桌面＋ ibus 輸入作業平台)

4. **重新部署 RIME 輸入法**：將作業系統使用中的輸入法，先切換成 RIME，再執行 RIME
   輸入法中的「重新部署」指令。

## 輸入法鍵盤

### 河洛白話

本輸入法，只需輸入 TLPA 音標，即可顯示相對應之漢字；至於「聲調」，可略去不用。
對於喜歡指明聲調者，則可參考以下之鍵盤，於 TLPA 音標之後，補入「聲調」。

![聲調鍵盤](./docs/static/img/keymap_tlpa_peh_ue.png)

### 河洛方音

![方音符號鍵盤](./docs/static/img/keymap_tlpa_fong_im.png)

### 河洛注音

![注音符號鍵盤](./docs/static/img/keymap_tlpa_cu_im.png)

## 字形

以下建議使用之字形，均為開源、免費字形：

- [思源黑體](https://github.com/adobe-fonts/source-han-sans)

- [Noto Sans Traditional Chinese](https://fonts.google.com/noto/specimen/Noto+Sans+TC)

- [字咍](https://github.com/ButTaiwan/taigivs/releases)

- [豆腐烏](https://github.com/glll4678/tshiuthau)

- [Fira Sans](https://github.com/mozilla/Fira)

![操作畫面](./docs/static/img/rime-taigi.png)
| 調號 | 四聲八調 | 聲調按鍵 | 漢字 | 台羅拼音 | 按鍵輸入 |
| :--: | :-------- | :------: | :--: | :------- | :------- |
| 1 | 陰平 (a) | [ | 東 | tang | tang[ |
| 2 | 陰上 (á) | / | 黨 | tóng | tong/ |
| 3 | 陰去 (à) | \ | 棟 | tòng | tong\ |
| 4 | 陰入 (ah) | ] | 督 | tok | tok] |
| 5 | 陽平 (â) | 9 | 同 | tông | tong9 |
| 6 | 陽上 (ǎ) | 0 | 動 | tǒng | tong0 |
| 7 | 陽入 (ā) | - | 洞 | tōng | tong- |
| 8 | 陽去 (a̍h) | ' | 毒 | to̍k | tok' |

![注音符號鍵盤](./docs/static/img/keyboard.png)
