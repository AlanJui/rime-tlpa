

```bash
c:\>cd "c:\Program Files\Rime\weasel-0.17.4"

c:\Program Files\Rime\weasel-0.17.4>ls rime-install.bat
rime-install.bat

c:\Program Files\Rime\weasel-0.17.4>rime-install.bat

Rime package installer

Working directory: c:\Program Files\Rime\weasel-0.17.4
Package installer directory: c:\Program Files\Rime\weasel-0.17.4\
Download cache directory: C:\Users\AlanJui\AppData\Local\Temp
Rime user directory: C:\Users\AlanJui\AppData\Roaming\Rime


Enter package name, URL, user/repo or downloaded ZIP to install: AlanJui/rime-tlpa
Updating package: AlanJui/rime-tlpa
remote: Enumerating objects: 208, done.
remote: Counting objects: 100% (208/208), done.
remote: Compressing objects: 100% (65/65), done.
remote: Total 202 (delta 94), reused 188 (delta 80), pack-reused 0 (from 0)
Receiving objects: 100% (202/202), 15.07 MiB | 11.46 MiB/s, done.
Resolving deltas: 100% (94/94), completed with 6 local objects.
From https://github.com/AlanJui/rime-tlpa
   2117ade..7b96584  main       -> origin/main
 * [new tag]         v0.1       -> v0.1
Updating 2117ade..7b96584
Fast-forward
 .gitattributes                                     |  21 ++
 .github/workflows/release-yamls.yml                | 195 +++++++++++
 README_Backup.md => _archived/README_Backup.md     |   0
 .../bp_kb_zu_im.schema.yaml                        |   0
 .../kb_tlpa_zu_im.schema.yaml                      |   0
 .../zu_im_2_hong_im_r4.schema.yaml                 |   0
 .../zu_im_2_kb.schema.yaml                         |   0
 .../zu_im_2_libs_r1.yaml                           |   0
 .../zu_im_2_phing_im.schema_模組化.yaml            |   0
 docs/_ops-git-tags.md                              | 176 ++++++++++
 docs/_版本發行作業指引.md                          | 363 +++++++++++++++++++++
 docs/yaml-debug.md                                 |   0
 .../漢字閩南語標音【台羅拼音】.xlsx                | Bin
 docs/鍵盤對映.md                                   |  16 -
 docs/鍵盤設計規格_方音符號.xlsx                    | Bin 599342 -> 602647 bytes
 hl-packages.conf                                   |  11 -
 my_test.schema.yaml => my_lab/my_test.schema.yaml  |   0
 release-include.txt                                |  35 ++
 EUDC.EUF => src/EUDC.EUF                           | Bin
 EUDC.TTE => src/EUDC.TTE                           | Bin
 Han_Gi_Ziann_Ji.csv => src/Han_Gi_Ziann_Ji.csv     |   0
 .../convert_tl_to_bpm2.py_bak                      |   0
 .../convert_tlpa_to_bp_for_rime_dict.py_bak        |   0
 .../convert_tlpa_to_mps2_for_rime_dict.py_bak      |   0
 install.bat => src/install.bat                     |   0
 install.sh => src/install.sh                       |   0
 src/mylist.txt                                     |  37 +++
 .../settings_to_append.txt                         |   0
 {src => tools}/bp_ji_khoo.dict.yaml                |   0
 clear_rime_cache.bat => tools/clear_rime_cache.bat |   0
 {src => tools}/convert_tl_to_bpm2.py               |   0
 {src => tools}/convert_tlpa_to_bp_for_rime_dict.py |   0
 {src => tools}/convert_tlpa_to_mps2.py             |   0
 {src => tools}/convert_tlpa_to_mps2_for_excel.py   |   0
 .../convert_tlpa_to_mps2_for_rime_dict copy.py     |   0
 .../convert_tlpa_to_mps2_for_rime_dict.py          |   0
 tools/delete-tags-by-tags-list.sh                  | 201 ++++++++++++
 tools/delete-tags.sh                               | 192 +++++++++++
 {src => tools}/mod_convert_TLPA_to_BP.py           |   0
 .../restart_rime_service.bat                       |   0
 {src => tools}/tl_phing_im.xlsx                    | Bin
 {src => tools}/tl_phing_im_out.xlsx                | Bin
 {src => tools}/tl_to_zu_im_2.py                    |   0
 {src => tools}/tlpa_ji_khoo.dict.yaml              |   0
 {src => tools}/tlpa_ji_khoo_out.dict.yaml          |   0
 {src => tools}/漢字閩南語標音【台羅拼音】.xlsx     | Bin
 {src => tools}/轉換規則.xlsx                       | Bin
 47 files changed, 1220 insertions(+), 27 deletions(-)
 create mode 100644 .gitattributes
 create mode 100644 .github/workflows/release-yamls.yml
 rename README_Backup.md => _archived/README_Backup.md (100%)
 rename BP_kb_zu_im.schema.yaml => _archived/bp_kb_zu_im.schema.yaml (100%)
 rename kb_tlpa_zu_im.schema.yaml => _archived/kb_tlpa_zu_im.schema.yaml (100%)
 rename zu_im_2_hong_im_r4.schema.yaml => _archived/zu_im_2_hong_im_r4.schema.yaml (100%)
 rename zu_im_2_kb.schema.yaml => _archived/zu_im_2_kb.schema.yaml (100%)
 rename zu_im_2_libs_r1.yaml => _archived/zu_im_2_libs_r1.yaml (100%)
 rename zu_im_2_phing_im.schema_模組化.yaml => _archived/zu_im_2_phing_im.schema_模組化.yaml (100%)
 create mode 100644 docs/_ops-git-tags.md
 create mode 100644 docs/_版本發行作業指引.md
 create mode 100644 docs/yaml-debug.md
 rename 漢字閩南語標音【台羅拼音】.xlsx => docs/漢字閩南語標音【台羅拼音】.xlsx (100%)
 delete mode 100644 docs/鍵盤對映.md
 delete mode 100644 hl-packages.conf
 rename my_test.schema.yaml => my_lab/my_test.schema.yaml (100%)
 create mode 100644 release-include.txt
 rename EUDC.EUF => src/EUDC.EUF (100%)
 rename EUDC.TTE => src/EUDC.TTE (100%)
 rename Han_Gi_Ziann_Ji.csv => src/Han_Gi_Ziann_Ji.csv (100%)
 rename convert_tl_to_bpm2.py_bak => src/convert_tl_to_bpm2.py_bak (100%)
 rename convert_tlpa_to_bp_for_rime_dict.py_bak => src/convert_tlpa_to_bp_for_rime_dict.py_bak (100%)
 rename convert_tlpa_to_mps2_for_rime_dict.py_bak => src/convert_tlpa_to_mps2_for_rime_dict.py_bak (100%)
 rename install.bat => src/install.bat (100%)
 rename install.sh => src/install.sh (100%)
 mode change 100755 => 100644
 create mode 100644 src/mylist.txt
 rename settings_to_append.txt => src/settings_to_append.txt (100%)
 rename {src => tools}/bp_ji_khoo.dict.yaml (100%)
 rename clear_rime_cache.bat => tools/clear_rime_cache.bat (100%)
 rename {src => tools}/convert_tl_to_bpm2.py (100%)
 rename {src => tools}/convert_tlpa_to_bp_for_rime_dict.py (100%)
 rename {src => tools}/convert_tlpa_to_mps2.py (100%)
 rename {src => tools}/convert_tlpa_to_mps2_for_excel.py (100%)
 rename {src => tools}/convert_tlpa_to_mps2_for_rime_dict copy.py (100%)
 rename {src => tools}/convert_tlpa_to_mps2_for_rime_dict.py (100%)
 create mode 100644 tools/delete-tags-by-tags-list.sh
 create mode 100644 tools/delete-tags.sh
 rename {src => tools}/mod_convert_TLPA_to_BP.py (100%)
 rename restart_rime_service.bat => tools/restart_rime_service.bat (100%)
 rename {src => tools}/tl_phing_im.xlsx (100%)
 rename {src => tools}/tl_phing_im_out.xlsx (100%)
 rename {src => tools}/tl_to_zu_im_2.py (100%)
 rename {src => tools}/tlpa_ji_khoo.dict.yaml (100%)
 rename {src => tools}/tlpa_ji_khoo_out.dict.yaml (100%)
 rename {src => tools}/漢字閩南語標音【台羅拼音】.xlsx (100%)
 rename {src => tools}/轉換規則.xlsx (100%)
Installing: release-include.txt
Updated ~ 1 files from 1 packages in 'C:\Users\AlanJui\AppData\Roaming\Rime'

Enter package name, URL, user/repo or downloaded ZIP to install:
```

```bash
c:\>cd "c:\Program Files\Rime\weasel-0.17.4"

c:\Program Files\Rime\weasel-0.17.4>ls rime-install.bat
rime-install.bat

c:\Program Files\Rime\weasel-0.17.4>rime-install.bat

Rime package installer

Working directory: c:\Program Files\Rime\weasel-0.17.4
Package installer directory: c:\Program Files\Rime\weasel-0.17.4\
Download cache directory: C:\Users\AlanJui\AppData\Local\Temp
Rime user directory: C:\Users\AlanJui\AppData\Roaming\Rime


Enter package name, URL, user/repo or downloaded ZIP to install: c:\Users\AlanJui\Downloads\rime-tlpa-0.1.zip

Unpacking c:\Users\AlanJui\Downloads\rime-tlpa-0.1.zip ...


7-Zip 24.05 (x86) : Copyright (c) 1999-2024 Igor Pavlov : 2024-05-14

Scanning the drive for archives:
1 file, 590683 bytes (577 KiB)

Extracting archive: c:\Users\AlanJui\Downloads\rime-tlpa-0.1.zip
--
Path = c:\Users\AlanJui\Downloads\rime-tlpa-0.1.zip
Type = zip
Physical Size = 590683
Comment = 2747b04a5575d690871f1586d97b28e2eff79d2c

Everything is Ok

Folders: 6
Files: 61
Size:       2405040
Compressed: 590683

Installing bp_hong_im.schema.yaml ...

        1 file(s) copied.

Installing bp_ji_khoo.dict.yaml ...

        1 file(s) copied.

Installing BP_kb_zu_im.schema.yaml ...

        1 file(s) copied.

Installing bp_libs.yaml ...

        1 file(s) copied.

Installing bp_phing_im.schema.yaml ...

        1 file(s) copied.

Installing kb_hong_im.schema.yaml ...

        1 file(s) copied.

Installing kb_ipa.schema.yaml ...

        1 file(s) copied.

Installing kb_tlpa_zu_im.schema.yaml ...

        1 file(s) copied.

Installing keymap_piau_tian.yaml ...

        1 file(s) copied.

Installing lib_hau_suan_ji_tuann.yaml ...

        1 file(s) copied.

Installing lib_phing_im.yaml ...

        1 file(s) copied.

Installing lib_sip_ngoo_im.yaml ...

        1 file(s) copied.

Installing lib_sip_ngoo_im2.yaml ...

        1 file(s) copied.

Installing lib_zu_im.yaml ...

        1 file(s) copied.

Installing tlpa_hong_im.schema.yaml ...

        1 file(s) copied.

Installing tlpa_lib_hau_suan_ji_tuann.yaml ...

        1 file(s) copied.

Installing tlpa_phing_im.schema.yaml ...

        1 file(s) copied.

Installing tl_ji_khoo_ciann_ji.dict.yaml ...

        1 file(s) copied.

Installing tl_ji_khoo_kah_kut_bun.dict.yaml ...

        1 file(s) copied.

Installing tl_ji_khoo_kong_un.dict.yaml ...

        1 file(s) copied.

Installing tl_ji_khoo_nga_siok_thong.dict.yaml ...

        1 file(s) copied.

Installing tl_ji_khoo_peh_ue.dict.yaml ...

        1 file(s) copied.

Installing tl_ji_khoo_peh_ue_zu_ting.dict.yaml ...

        1 file(s) copied.

Installing zu_im_2.dict.yaml ...

        1 file(s) copied.

Installing zu_im_2_hau_suan_zzi_duann.yaml ...

        1 file(s) copied.

Installing zu_im_2_hong_im.schema.yaml ...

        1 file(s) copied.

Installing zu_im_2_kb.schema.yaml ...

        1 file(s) copied.

Installing zu_im_2_libs.yaml ...

        1 file(s) copied.

Installing zu_im_2_phing_im.schema.yaml ...

        1 file(s) copied.

Installing release-include.txt ...

        1 file(s) copied.

Enter package name, URL, user/repo or downloaded ZIP to install:

Installed 1 packages.

c:\Program Files\Rime\weasel-0.17.4>
```