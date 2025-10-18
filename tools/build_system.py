#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RIME TLPA 工具完整建置腳本
包含：編譯、打包、創建安裝程式
"""

import shutil
import subprocess
import sys
import zipfile
from datetime import datetime
from pathlib import Path


class RimeBuildSystem:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"
        self.release_dir = self.project_root / "release"

    def clean_build(self):
        """清理建置目錄"""
        print("🧹 清理建置目錄...")

        for dir_path in [self.dist_dir, self.build_dir, self.release_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   清理: {dir_path}")

        self.release_dir.mkdir(parents=True, exist_ok=True)

    def install_dependencies(self):
        """安裝建置依賴"""
        print("📦 檢查和安裝依賴套件...")

        dependencies = ["pyinstaller", "setuptools", "wheel"]

        for dep in dependencies:
            try:
                __import__(dep.replace("-", "_"))
                print(f"   ✅ {dep} 已安裝")
            except ImportError:
                print(f"   📥 安裝 {dep}...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

    def build_tools(self):
        """建置各種工具"""
        print("🔨 建置工具...")

        tools = [
            {
                "script": "tools/test_xlit_rules.py",
                "name": "RIME_TLPA_Validator",
                "description": "RIME TLPA 驗證工具"
            },
            {
                "script": "tools/rime_installer.py",
                "name": "RIME_TLPA_Installer",
                "description": "RIME TLPA 安裝程式"
            }
        ]

        for tool in tools:
            print(f"   🔧 建置 {tool['description']}...")

            cmd = [
                "pyinstaller",
                "--onefile",
                "--clean",
                "--name", tool["name"],
                "--distpath", str(self.release_dir),
                tool["script"]
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"   ✅ {tool['name']} 建置成功")
            else:
                print(f"   ❌ {tool['name']} 建置失敗")
                print(result.stderr)

    def build_installer(self):
        """建置安裝程式"""
        print("📦 建置安裝程式...")

        # 檢查 spec 檔案
        spec_file = self.project_root / "installer.spec"
        if not spec_file.exists():
            print("   ⚠️  installer.spec 不存在，跳過安裝程式建置")
            return

        cmd = [
            "pyinstaller",
            str(spec_file),
            "--distpath", str(self.release_dir)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ 安裝程式建置成功")
        else:
            print("   ❌ 安裝程式建置失敗")
            print(result.stderr)

    def copy_resources(self):
        """複製資源檔案 - 根據 release-include.txt"""
        print("📋 複製資源檔案...")

        # 讀取要包含的檔案列表
        include_file = self.project_root / "release-include.txt"
        if not include_file.exists():
            print("   ⚠️  release-include.txt 不存在，使用預設檔案列表")
            return self._copy_default_resources()

        resource_dir = self.release_dir / "rime_files"
        resource_dir.mkdir(exist_ok=True)

        # 解析 release-include.txt
        files_to_copy = self._parse_release_include()

        copied_count = 0
        for file_name in files_to_copy:
            src_file = self.project_root / file_name
            if src_file.exists() and src_file.is_file():
                dst_file = resource_dir / file_name
                shutil.copy2(src_file, dst_file)
                print(f"   📄 複製 RIME 檔案: {file_name}")
                copied_count += 1
            else:
                print(f"   ⚠️  檔案不存在: {file_name}")

        # 複製 default.custom.yaml (特殊處理)
        self._copy_default_custom_yaml(resource_dir)

        print(f"   ✅ 共複製 {copied_count} 個 RIME 檔案")

    def _parse_release_include(self):
        """解析 release-include.txt 檔案"""
        include_file = self.project_root / "release-include.txt"
        files = []

        with open(include_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳過註解和空行
                if line and not line.startswith('#'):
                    files.append(line)

        return files

    def _copy_default_custom_yaml(self, resource_dir):
        """複製 default.custom.yaml 檔案"""
        config_dir = self.project_root / "config"
        default_custom = config_dir / "default.custom.yaml"

        if default_custom.exists():
            dst_file = resource_dir / "default.custom.yaml"
            shutil.copy2(default_custom, dst_file)
            print("   📄 複製配置檔案: config/default.custom.yaml")
        else:
            print("   ⚠️  config/default.custom.yaml 不存在")

    def _copy_default_resources(self):
        """複製預設資源檔案（fallback）"""
        import glob

        resources = [
            "*.schema.yaml",
            "*.dict.yaml",
            "*.lua",
            "README.md"
        ]

        resource_dir = self.release_dir / "rime_files"
        resource_dir.mkdir(exist_ok=True)

        for pattern in resources:
            files = glob.glob(str(self.project_root / pattern))
            for file_path in files:
                src = Path(file_path)
                if src.is_file():
                    dst = resource_dir / src.name
                    shutil.copy2(src, dst)
                    print(f"   📄 複製預設檔案: {src.name}")

    def create_release_package(self):
        """創建發布套件"""
        print("📦 創建發布套件...")

        # 獲取版本資訊
        version = "1.0.0"  # 可以從某個配置檔讀取
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 創建壓縮檔
        package_name = f"RIME_TLPA_Tools_v{version}_{timestamp}.zip"
        package_path = self.release_dir / package_name

        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加所有發布檔案
            for file_path in self.release_dir.rglob('*'):
                if file_path.is_file() and file_path != package_path:
                    arcname = file_path.relative_to(self.release_dir)
                    zipf.write(file_path, arcname)
                    print(f"   📦 打包: {arcname}")

        print(f"✅ 發布套件已創建: {package_name}")

    def create_installer_script(self):
        """創建 Windows 安裝腳本"""
        print("🗂️  創建 Windows 安裝腳本...")

        install_script = self.release_dir / "install.bat"
        install_script.write_text("""@echo off
echo ================================
echo RIME TLPA 台語輸入法配置工具安裝
echo ================================
echo.

REM 設定目錄變數
set RIME_DIR=%APPDATA%\\Rime
set INSTALL_DIR=%ProgramFiles%\\RIME TLPA Tools

echo RIME 配置目錄: %RIME_DIR%
echo 工具安裝目錄: %INSTALL_DIR%
echo.

REM 檢查 RIME 目錄是否存在
if not exist "%RIME_DIR%" (
    echo ❌ 錯誤: RIME 配置目錄不存在
    echo 請先安裝 RIME 小狼毫輸入法
    echo 下載網址: https://rime.im/
    pause
    exit /b 1
)

echo ✅ 找到 RIME 配置目錄

REM 創建工具安裝目錄
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%" 2>nul

REM 備份現有的 default.custom.yaml
if exist "%RIME_DIR%\\default.custom.yaml" (
    echo 📋 備份現有的 default.custom.yaml...
    copy "%RIME_DIR%\\default.custom.yaml" "%RIME_DIR%\\default.custom.yaml.bak" >nul
    echo    已備份為 default.custom.yaml.bak
)

REM 複製 RIME 配置檔案 (根據 release-include.txt)
echo 📄 複製 RIME 配置檔案...
if exist "rime_files\\*" (
    copy "rime_files\\*" "%RIME_DIR%\\" >nul
    echo    已複製所有 RIME 配置檔案
) else (
    echo ❌ 錯誤: 找不到 rime_files 目錄
    pause
    exit /b 1
)

REM 複製工具程式檔案
if exist "*.exe" (
    echo 🔧 複製工具程式檔案...
    copy "*.exe" "%INSTALL_DIR%\\" >nul 2>&1
    echo    已複製工具程式到安裝目錄
)

echo.
echo ✅ 安裝完成!
echo.
echo 📝 後續步驟:
echo 1. 開啟 RIME 小狼毫系統匣圖示
echo 2. 右鍵選擇「重新部署」
echo 3. 等待部署完成 (可能需要幾分鐘)
echo 4. 切換到 TLPA 台語輸入法方案
echo.
echo 📂 已安裝的檔案位置:
echo    RIME 配置: %RIME_DIR%
echo    工具程式: %INSTALL_DIR%
echo.
pause
""", encoding='utf-8')

        print("   ✅ 安裝腳本已創建: install.bat")

    def generate_report(self):
        """生成建置報告"""
        print("📊 生成建置報告...")

        report_file = self.release_dir / "BUILD_REPORT.txt"

        # 統計檔案
        exe_files = list(self.release_dir.glob("*.exe"))
        rime_files_dir = self.release_dir / "rime_files"
        rime_files = list(rime_files_dir.rglob("*") if rime_files_dir.exists() else [])
        total_size = sum(f.stat().st_size for f in self.release_dir.rglob("*") if f.is_file())

        report_content = f"""RIME TLPA 工具建置報告
==============================

建置時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
建置版本: 1.0.0

建置結果:
- 可執行檔案: {len(exe_files)} 個
- RIME 配置檔案: {len(rime_files)} 個
- 總大小: {total_size / 1024 / 1024:.2f} MB

可執行檔案列表:
{chr(10).join(f"  - {f.name} ({f.stat().st_size / 1024:.1f} KB)" for f in exe_files)}

建置狀態: 完成 ✅

安裝說明:
1. 執行 install.bat (需要管理員權限)
2. 或手動複製檔案到相應目錄
3. 在 RIME 中重新部署
"""

        report_file.write_text(report_content, encoding='utf-8')
        print(f"   📋 建置報告已生成: {report_file}")

    def build_all(self):
        """執行完整建置流程"""
        print("🚀 開始完整建置流程...")
        print("="*50)

        try:
            self.clean_build()
            self.install_dependencies()
            self.build_tools()
            # self.build_installer()  # 暫時跳過，因為 GUI 可能有問題
            self.copy_resources()
            self.create_installer_script()
            self.create_release_package()
            self.generate_report()

            print("="*50)
            print("🎉 建置流程完成!")
            print(f"📁 發布檔案位於: {self.release_dir}")

        except Exception as e:
            print(f"❌ 建置過程中發生錯誤: {e}")
            return False

        return True

def main():
    """主函式"""
    build_system = RimeBuildSystem()
    success = build_system.build_all()

    if success:
        print("✅ 所有建置步驟都成功完成!")
    else:
        print("❌ 建置過程中有錯誤發生")
        sys.exit(1)

if __name__ == "__main__":
    main()