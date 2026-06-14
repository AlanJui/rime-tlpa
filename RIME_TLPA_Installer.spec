# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tools\\rime_installer.py'],
    pathex=[],
    binaries=[],
    datas=[
        # 僅內嵌【輸入法選單設定】；輸入方案檔（schema/dict/lua…）改由
        # 使用者下載之 rime-tlpa-*.zip 提供，不再打包進 exe。
        ('config/default.custom.yaml', 'config'),  # 全部輸入方案選單設定
        ('config/default.custom.zu_im.yaml', 'config'),  # 注音類輸入方案選單設定
        ('config/default.custom.phing_im.yaml', 'config'),  # 拼音類輸入方案選單設定
        ('config/default.custom.huan_ciat.yaml', 'config'),  # 反切類輸入方案選單設定
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
