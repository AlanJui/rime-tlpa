# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec 檔案
用於自訂 RIME 工具的打包設定
"""

block_cipher = None

# 分析階段：指定要打包的腳本和相關設定
a = Analysis(
    ['tools/installer_gui.py'],  # 主要腳本
    pathex=[],  # 額外的 Python 路徑
    binaries=[],  # 二進制檔案
    datas=[
        # 包含資料檔案
        ('*.yaml', '.'),  # 所有 YAML 檔案
        ('tools/*.md', 'tools'),  # 工具說明文件
        ('dist/RIME_TLPA_Validator.exe', '.'),  # 已編譯的驗證工具
    ],
    hiddenimports=[  # 隱藏匯入的模組
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[  # 排除不需要的模組以減小檔案大小
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
        'PIL',
        'cv2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# PYZ 階段：Python 字節碼歸檔
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE 階段：可執行檔案設定
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RIME_TLPA_Installer',  # 輸出檔案名稱
    debug=False,  # 除錯模式
    bootloader_ignore_signals=False,
    strip=False,  # 是否移除符號表
    upx=True,  # 使用 UPX 壓縮 (需要安裝 UPX)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不顯示控制台視窗
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows 特有設定
    version='version_info.txt',  # 版本資訊檔案
    icon='icon.ico',  # 圖示檔案 (如果有的話)
)