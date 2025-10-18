#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RIME TLPA 專用安裝程式
根據 release-include.txt 指定的檔案進行安裝
並處理 default.custom.yaml 的備份和替換
"""

import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class RimeTLPAInstaller:
    def __init__(self):
        # 智能檢測資源目錄位置
        current_dir = Path.cwd()
        exe_dir = Path(__file__).parent if hasattr(sys, '_MEIPASS') else current_dir

        # 可能的資源目錄位置
        possible_dirs = [
            current_dir,  # 當前目錄
            exe_dir,      # 執行檔目錄
            current_dir.parent,  # 上級目錄
            exe_dir.parent       # 執行檔上級目錄
        ]

        self.project_root = None
        for directory in possible_dirs:
            if (directory / "rime_files").exists() or (directory / "release-include.txt").exists():
                self.project_root = directory
                break

        if self.project_root is None:
            self.project_root = current_dir

        self.rime_dir = Path.home() / "AppData" / "Roaming" / "Rime"

    def check_rime_installation(self):
        """檢查 RIME 是否已安裝"""
        if not self.rime_dir.exists():
            print("❌ 錯誤: RIME 配置目錄不存在")
            print(f"   預期位置: {self.rime_dir}")
            print("   請先安裝 RIME 小狼毫輸入法")
            print("   下載網址: https://rime.im/")
            return False

        print(f"✅ 找到 RIME 配置目錄: {self.rime_dir}")
        return True

    def parse_release_include(self):
        """解析 release-include.txt 檔案"""
        include_file = self.project_root / "release-include.txt"

        if not include_file.exists():
            print("❌ 錯誤: 找不到 release-include.txt")
            return []

        files = []
        with open(include_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳過註解和空行
                if line and not line.startswith('#'):
                    files.append(line)

        print(f"📋 從 release-include.txt 讀取到 {len(files)} 個檔案")
        return files

    def backup_default_custom(self):
        """備份現有的 default.custom.yaml"""
        default_custom = self.rime_dir / "default.custom.yaml"

        if default_custom.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"default.custom.yaml.bak_{timestamp}"
            backup_path = self.rime_dir / backup_name

            shutil.copy2(default_custom, backup_path)
            print(f"📋 已備份 default.custom.yaml 為: {backup_name}")
            return True
        else:
            print("📋 default.custom.yaml 不存在，無需備份")
            return False

    def copy_rime_files(self):
        """複製 RIME 配置檔案"""
        print("📄 開始複製 RIME 配置檔案...")

        # 檢查是否有預先打包的 rime_files 目錄
        rime_files_dir = self.project_root / "rime_files"
        if rime_files_dir.exists():
            return self._copy_from_rime_files_dir(rime_files_dir)
        else:
            # 回到原始邏輯，從 release-include.txt 複製
            return self._copy_from_release_include()

    def _copy_from_rime_files_dir(self, rime_files_dir):
        """從 rime_files 目錄複製所有檔案"""
        print("   📁 從 rime_files 目錄複製...")

        copied_count = 0
        failed_files = []

        # 複製 rime_files 目錄中的所有檔案
        for src_file in rime_files_dir.iterdir():
            if src_file.is_file():
                dst_file = self.rime_dir / src_file.name
                try:
                    shutil.copy2(src_file, dst_file)
                    print(f"   ✅ 已複製: {src_file.name}")
                    copied_count += 1
                except Exception as e:
                    print(f"   ❌ 複製失敗: {src_file.name} - {e}")
                    failed_files.append(src_file.name)

        print(f"📊 複製結果: 成功 {copied_count} 個，失敗 {len(failed_files)} 個")

        if failed_files:
            print("❌ 失敗的檔案:")
            for file_name in failed_files:
                print(f"   - {file_name}")

        return copied_count, failed_files

    def _copy_from_release_include(self):
        """從 release-include.txt 指定的檔案複製"""
        print("   📋 根據 release-include.txt 複製...")

        files_to_copy = self.parse_release_include()
        copied_count = 0
        failed_files = []

        for file_name in files_to_copy:
            src_file = self.project_root / file_name
            dst_file = self.rime_dir / file_name

            if src_file.exists() and src_file.is_file():
                try:
                    shutil.copy2(src_file, dst_file)
                    print(f"   ✅ 已複製: {file_name}")
                    copied_count += 1
                except Exception as e:
                    print(f"   ❌ 複製失敗: {file_name} - {e}")
                    failed_files.append(file_name)
            else:
                print(f"   ⚠️  檔案不存在: {file_name}")
                failed_files.append(file_name)

        print(f"📊 複製結果: 成功 {copied_count} 個，失敗 {len(failed_files)} 個")

        if failed_files:
            print("❌ 失敗的檔案:")
            for file_name in failed_files:
                print(f"   - {file_name}")

        return copied_count, failed_files

    def copy_default_custom(self):
        """複製新的 default.custom.yaml"""
        # 優先從 rime_files 目錄複製
        rime_files_dir = self.project_root / "rime_files"
        rime_files_src = rime_files_dir / "default.custom.yaml"

        if rime_files_src.exists():
            dst_file = self.rime_dir / "default.custom.yaml"
            shutil.copy2(rime_files_src, dst_file)
            print("✅ 已複製新的 default.custom.yaml (從 rime_files)")
            return True

        # 回退到 config 目錄
        config_dir = self.project_root / "config"
        config_src = config_dir / "default.custom.yaml"

        if config_src.exists():
            dst_file = self.rime_dir / "default.custom.yaml"
            shutil.copy2(config_src, dst_file)
            print("✅ 已複製新的 default.custom.yaml (從 config)")
            return True
        else:
            print("⚠️  找不到 default.custom.yaml")
            return False

    def deploy_rime(self):
        """觸發 RIME 重新部署"""
        print("🔄 嘗試觸發 RIME 重新部署...")

        # 查找 RIME 部署程式
        possible_paths = [
            Path("C:/Program Files/Rime/weasel-*/WeaselDeployer.exe"),
            Path("C:/Program Files (x86)/Rime/weasel-*/WeaselDeployer.exe")
        ]

        deployer_path = None
        for path_pattern in possible_paths:
            matches = list(path_pattern.parent.parent.glob(path_pattern.name))
            if matches:
                deployer_path = matches[0]
                break

        if deployer_path and deployer_path.exists():
            try:
                subprocess.run([str(deployer_path), "/deploy"], check=True)
                print("✅ RIME 重新部署成功")
                return True
            except subprocess.CalledProcessError:
                print("⚠️  自動部署失敗，請手動重新部署")
                return False
        else:
            print("⚠️  找不到 RIME 部署程式，請手動重新部署")
            return False

    def install(self):
        """執行完整安裝流程"""
        print("=" * 50)
        print("🚀 RIME TLPA 台語輸入法配置工具安裝程式")
        print("=" * 50)

        # 1. 檢查 RIME 安裝
        if not self.check_rime_installation():
            return False

        # 2. 備份現有配置
        self.backup_default_custom()

        # 3. 複製 RIME 配置檔案
        copied_count, failed_files = self.copy_rime_files()

        # 4. 複製新的 default.custom.yaml
        self.copy_default_custom()

        # 5. 嘗試重新部署
        self.deploy_rime()

        # 6. 顯示完成訊息
        print("\n" + "=" * 50)
        print("🎉 安裝完成!")
        print("=" * 50)

        print("\n📝 後續步驟:")
        print("1. 如果 RIME 沒有自動重新部署，請：")
        print("   - 右鍵點擊 RIME 小狼毫系統匣圖示")
        print("   - 選擇「重新部署」")
        print("   - 等待部署完成 (可能需要幾分鐘)")
        print("2. 切換到 TLPA 台語輸入法方案")
        print("3. 開始使用台語輸入法")

        print("\n📊 安裝統計:")
        print(f"   - 成功複製檔案: {copied_count} 個")
        print(f"   - 失敗檔案: {len(failed_files)} 個")
        print(f"   - RIME 配置目錄: {self.rime_dir}")

        if failed_files:
            print(f"\n⚠️  有 {len(failed_files)} 個檔案複製失敗，可能影響功能")

        return len(failed_files) == 0

def main():
    """主函式"""
    installer = RimeTLPAInstaller()

    try:
        success = installer.install()
        if success:
            print("\n✅ 所有檔案都安裝成功!")
        else:
            print("\n⚠️  安裝過程中有部分問題，請檢查上述訊息")

    except KeyboardInterrupt:
        print("\n❌ 安裝被使用者中斷")
    except Exception as e:
        print(f"\n❌ 安裝過程中發生錯誤: {e}")

    input("\n按 Enter 鍵結束...")

if __name__ == "__main__":
    main()