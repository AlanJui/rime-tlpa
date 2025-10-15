#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RIME 工具打包腳本
使用 PyInstaller 將 Python 腳本打包成 .exe 檔案
"""

import importlib.util
import os
import subprocess
import sys


def install_pyinstaller():
    """安裝 PyInstaller"""
    # 檢查 PyInstaller 是否已安裝
    if importlib.util.find_spec("PyInstaller") is not None:
        print("✅ PyInstaller 已安裝")
        return True
    else:
        print("📦 正在安裝 PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller 安裝成功")
            return True
        except subprocess.CalledProcessError:
            print("❌ PyInstaller 安裝失敗")
            return False

def build_exe(script_path, output_name=None, console=True, icon=None):
    """
    打包 Python 腳本為 .exe 檔案

    Args:
        script_path: Python 腳本路徑
        output_name: 輸出檔案名稱
        console: 是否顯示控制台視窗
        icon: 圖示檔案路徑
    """
    if not os.path.exists(script_path):
        print(f"❌ 找不到腳本文件: {script_path}")
        return False

    # 建立 PyInstaller 命令
    cmd = [
        "pyinstaller",
        "--onefile",  # 產生單一檔案
        "--clean",    # 清除暫存檔案
    ]

    # 設定輸出檔名
    if output_name:
        cmd.extend(["--name", output_name])

    # 設定是否顯示控制台
    if console:
        cmd.append("--console")
    else:
        cmd.append("--windowed")

    # 設定圖示
    if icon and os.path.exists(icon):
        cmd.extend(["--icon", icon])

    # 添加腳本路徑
    cmd.append(script_path)

    print(f"🔨 執行打包命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 打包成功!")
            print(f"📁 輸出目錄: {os.path.join(os.getcwd(), 'dist')}")
            return True
        else:
            print("❌ 打包失敗:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 執行錯誤: {e}")
        return False

def build_from_spec(spec_file):
    """使用 spec 檔案打包"""
    if not os.path.exists(spec_file):
        print(f"❌ 找不到 spec 檔案: {spec_file}")
        return False

    cmd = ["pyinstaller", spec_file]
    print(f"🔨 執行 spec 打包命令: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ spec 打包成功!")
            return True
        else:
            print("❌ spec 打包失敗:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ spec 執行錯誤: {e}")
        return False

def main():
    """主函式"""
    print("=== RIME 工具打包程式 ===\n")

    # 檢查並安裝 PyInstaller
    if not install_pyinstaller():
        return

    # 定義要打包的腳本
    scripts = [
        {
            "path": "tools/test_xlit_rules.py",
            "name": "RIME_TLPA_Validator",
            "console": True
        },
        {
            "path": "tools/installer_gui.py",
            "name": "RIME_TLPA_Installer_GUI",
            "console": False
        }
    ]

    # 使用 spec 檔案打包安裝程式
    print("\n📦 使用 spec 檔案打包完整安裝程式...")
    if os.path.exists("installer.spec"):
        success = build_from_spec("installer.spec")
        if success:
            print("✅ 完整安裝程式打包完成")
        else:
            print("❌ 完整安裝程式打包失敗")

    # 打包每個腳本
    for script in scripts:
        print(f"\n📦 打包 {script['path']}...")
        success = build_exe(
            script_path=script["path"],
            output_name=script["name"],
            console=script["console"]
        )

        if success:
            print(f"✅ {script['name']}.exe 打包完成")
        else:
            print(f"❌ {script['name']} 打包失敗")

    print("\n🎉 打包程序完成!")
    print("📁 所有 .exe 檔案都在 dist/ 目錄中")

if __name__ == "__main__":
    main()