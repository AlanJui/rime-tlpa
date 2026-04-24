# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tools\\rime_installer.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('release-include.txt', '.'),          # 安裝清單
        ('*.yaml', '.'),                       # 根目錄所有 YAML 配置
        ('rime.lua', '.'),                     # 根目錄 Lua 主入口
        ('lua/*.lua', 'lua'),                  # lua/ 子目錄所有 Lua 插件
        ('config/default.custom.yaml', 'config'),  # 預設輸入法選單設定
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='RIME_TLPA_Installer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
