#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RIME TLPA 專用安裝程式（圖形介面版）
根據 release-include.txt 指定的檔案進行安裝
並處理 default.custom.yaml 的備份和替換
"""

import queue
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk


class RimeTLPAInstaller:
    def __init__(self, log_func=None):
        self._log = log_func or print
        # 智能檢測資源目錄位置
        current_dir = Path.cwd()
        exe_dir = Path(sys._MEIPASS) if hasattr(sys, '_MEIPASS') else Path(__file__).parent

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
            self._log("❌ 錯誤: RIME 配置目錄不存在")
            self._log(f"   預期位置: {self.rime_dir}")
            self._log("   請先安裝 RIME 小狼毫輸入法")
            self._log("   下載網址: https://rime.im/")
            return False

        self._log(f"✅ 找到 RIME 配置目錄: {self.rime_dir}")
        return True

    def parse_release_include(self):
        """解析 release-include.txt 檔案"""
        include_file = self.project_root / "release-include.txt"

        if not include_file.exists():
            self._log("❌ 錯誤: 找不到 release-include.txt")
            return []

        files = []
        with open(include_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳過註解和空行
                if line and not line.startswith('#'):
                    files.append(line)

        self._log(f"📋 從 release-include.txt 讀取到 {len(files)} 個檔案")
        return files

    def backup_default_custom(self):
        """備份現有的 default.custom.yaml"""
        default_custom = self.rime_dir / "default.custom.yaml"

        if default_custom.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"default.custom.yaml.bak_{timestamp}"
            backup_path = self.rime_dir / backup_name

            shutil.copy2(default_custom, backup_path)
            self._log(f"📋 已備份 default.custom.yaml 為: {backup_name}")
            return True
        else:
            self._log("📋 default.custom.yaml 不存在，無需備份")
            return False

    def copy_rime_files(self):
        """複製 RIME 配置檔案"""
        self._log("📄 開始複製 RIME 配置檔案...")

        # 檢查是否有預先打包的 rime_files 目錄
        rime_files_dir = self.project_root / "rime_files"
        if rime_files_dir.exists():
            return self._copy_from_rime_files_dir(rime_files_dir)
        else:
            # 回到原始邏輯，從 release-include.txt 複製
            return self._copy_from_release_include()

    def _copy_from_rime_files_dir(self, rime_files_dir):
        """從 rime_files 目錄複製所有檔案"""
        self._log("   📁 從 rime_files 目錄複製...")

        copied_count = 0
        failed_files = []

        # 複製 rime_files 目錄中的所有檔案
        for src_file in rime_files_dir.iterdir():
            if src_file.is_file():
                dst_file = self.rime_dir / src_file.name
                try:
                    shutil.copy2(src_file, dst_file)
                    self._log(f"   ✅ 已複製: {src_file.name}")
                    copied_count += 1
                except Exception as e:
                    self._log(f"   ❌ 複製失敗: {src_file.name} - {e}")
                    failed_files.append(src_file.name)

        self._log(f"📊 複製結果: 成功 {copied_count} 個，失敗 {len(failed_files)} 個")

        if failed_files:
            self._log("❌ 失敗的檔案:")
            for file_name in failed_files:
                self._log(f"   - {file_name}")

        return copied_count, failed_files

    def _copy_from_release_include(self):
        """從 release-include.txt 指定的檔案複製"""
        self._log("   📋 根據 release-include.txt 複製...")

        files_to_copy = self.parse_release_include()
        copied_count = 0
        failed_files = []

        for file_name in files_to_copy:
            src_file = self.project_root / file_name
            dst_file = self.rime_dir / file_name

            if src_file.exists() and src_file.is_file():
                try:
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src_file, dst_file)
                    self._log(f"   ✅ 已複製: {file_name}")
                    copied_count += 1
                except Exception as e:
                    self._log(f"   ❌ 複製失敗: {file_name} - {e}")
                    failed_files.append(file_name)
            else:
                self._log(f"   ⚠️  檔案不存在: {file_name}")
                failed_files.append(file_name)

        self._log(f"📊 複製結果: 成功 {copied_count} 個，失敗 {len(failed_files)} 個")

        if failed_files:
            self._log("❌ 失敗的檔案:")
            for file_name in failed_files:
                self._log(f"   - {file_name}")

        return copied_count, failed_files

    def copy_default_custom(self):
        """複製新的 default.custom.yaml"""
        # 優先從 rime_files 目錄複製
        rime_files_dir = self.project_root / "rime_files"
        rime_files_src = rime_files_dir / "default.custom.yaml"

        if rime_files_src.exists():
            dst_file = self.rime_dir / "default.custom.yaml"
            shutil.copy2(rime_files_src, dst_file)
            self._log("✅ 已複製新的 default.custom.yaml (從 rime_files)")
            return True

        # 回退到 config 目錄
        config_dir = self.project_root / "config"
        config_src = config_dir / "default.custom.yaml"

        if config_src.exists():
            dst_file = self.rime_dir / "default.custom.yaml"
            shutil.copy2(config_src, dst_file)
            self._log("✅ 已複製新的 default.custom.yaml (從 config)")
            return True
        else:
            self._log("⚠️  找不到 default.custom.yaml")
            return False

    def deploy_rime(self):
        """觸發 RIME 重新部署"""
        self._log("🔄 嘗試觸發 RIME 重新部署...")

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
                self._log("✅ RIME 重新部署成功")
                return True
            except subprocess.CalledProcessError:
                self._log("⚠️  自動部署失敗，請手動重新部署")
                return False
        else:
            self._log("⚠️  找不到 RIME 部署程式，請手動重新部署")
            return False

    def install(self):
        """執行完整安裝流程"""
        self._log("=" * 50)
        self._log("🚀 RIME TLPA 閩南語輸入法配置工具安裝程式")
        self._log("=" * 50)

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
        self._log("\n" + "=" * 50)
        self._log("🎉 安裝完成!")
        self._log("=" * 50)

        self._log("\n📝 後續步驟:")
        self._log("1. 如果 RIME 沒有自動重新部署，請：")
        self._log("   - 右鍵點擊 RIME 小狼毫系統匣圖示")
        self._log("   - 選擇「重新部署」")
        self._log("   - 等待部署完成 (可能需要幾分鐘)")
        self._log("2. 切換到 TLPA 閩南語輸入法方案")
        self._log("3. 開始使用閩南語輸入法")

        self._log("\n📊 安裝統計:")
        self._log(f"   - 成功複製檔案: {copied_count} 個")
        self._log(f"   - 失敗檔案: {len(failed_files)} 個")
        self._log(f"   - RIME 配置目錄: {self.rime_dir}")

        if failed_files:
            self._log(f"\n⚠️  有 {len(failed_files)} 個檔案複製失敗，可能影響功能")

        return len(failed_files) == 0

class InstallerApp(tk.Tk):
    """RIME TLPA 安裝程式圖形介面"""

    BG = "#1e1e2e"
    FG = "#cdd6f4"
    ACCENT = "#89b4fa"
    SUCCESS = "#a6e3a1"
    WARNING = "#f9e2af"
    ERROR = "#f38ba8"
    LOG_BG = "#181825"

    def __init__(self):
        super().__init__()
        self.title("RIME TLPA 閩南語輸入法 安裝程式")
        self.resizable(False, False)
        self.configure(bg=self.BG)
        self._queue = queue.Queue()
        self._build_ui()
        self._center()
        self.after(100, self._poll_queue)

    def _build_ui(self):
        PAD = 16

        # ── 標題列 ─────────────────────────────────────
        header = tk.Frame(self, bg=self.ACCENT, pady=10)
        header.pack(fill="x")
        tk.Label(
            header,
            text="RIME TLPA  閩南語輸入法安裝程式",
            font=("Segoe UI", 16, "bold"),
            bg=self.ACCENT,
            fg=self.BG,
        ).pack()

        # ── 說明文字 ────────────────────────────────────
        tk.Label(
            self,
            text="點擊【開始安裝】，程式將自動複製輸入方案並重新部署 RIME。",
            font=("Segoe UI", 10),
            bg=self.BG,
            fg=self.FG,
            wraplength=480,
            justify="left",
        ).pack(padx=PAD, pady=(PAD, 4), anchor="w")

        # ── 記錄視窗 ────────────────────────────────────
        log_frame = tk.Frame(self, bg=self.BG)
        log_frame.pack(padx=PAD, pady=(0, 8), fill="both", expand=True)

        self._log_text = tk.Text(
            log_frame,
            width=62,
            height=18,
            bg=self.LOG_BG,
            fg=self.FG,
            font=("Consolas", 9),
            state="disabled",
            relief="flat",
            bd=0,
            wrap="word",
        )
        scrollbar = ttk.Scrollbar(log_frame, command=self._log_text.yview)
        self._log_text.configure(yscrollcommand=scrollbar.set)
        self._log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 文字標籤顏色設定
        self._log_text.tag_config("ok",   foreground=self.SUCCESS)
        self._log_text.tag_config("warn", foreground=self.WARNING)
        self._log_text.tag_config("err",  foreground=self.ERROR)
        self._log_text.tag_config("info", foreground=self.ACCENT)

        # ── 進度條 ──────────────────────────────────────
        self._progress = ttk.Progressbar(
            self, mode="indeterminate", length=480
        )
        self._progress.pack(padx=PAD, pady=(0, 8))

        # ── 按鈕列 ──────────────────────────────────────
        btn_frame = tk.Frame(self, bg=self.BG)
        btn_frame.pack(pady=(0, PAD))

        self._install_btn = tk.Button(
            btn_frame,
            text="  開始安裝  ",
            font=("Segoe UI", 11, "bold"),
            bg=self.ACCENT,
            fg=self.BG,
            activebackground="#74c7ec",
            relief="flat",
            cursor="hand2",
            command=self._start_install,
        )
        self._install_btn.pack(side="left", padx=8)

        self._close_btn = tk.Button(
            btn_frame,
            text="  關閉  ",
            font=("Segoe UI", 11),
            bg="#313244",
            fg=self.FG,
            activebackground="#45475a",
            relief="flat",
            cursor="hand2",
            command=self.destroy,
        )
        self._close_btn.pack(side="left", padx=8)

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

    # ── 執行緒安全的記錄 ────────────────────────────────
    def _enqueue_log(self, msg: str):
        self._queue.put(msg)

    def _poll_queue(self):
        try:
            while True:
                msg = self._queue.get_nowait()
                self._append_log(msg)
        except queue.Empty:
            pass
        self.after(50, self._poll_queue)

    def _append_log(self, msg: str):
        self._log_text.configure(state="normal")
        if msg.startswith("✅") or msg.startswith("🎉"):
            tag = "ok"
        elif msg.startswith("⚠️") or msg.startswith("📋") or msg.startswith("📝"):
            tag = "warn"
        elif msg.startswith("❌"):
            tag = "err"
        elif msg.startswith("🚀") or msg.startswith("=" * 3):
            tag = "info"
        else:
            tag = None
        self._log_text.insert("end", msg + "\n", tag)
        self._log_text.see("end")
        self._log_text.configure(state="disabled")

    # ── 安裝流程 ────────────────────────────────────────
    def _start_install(self):
        self._install_btn.configure(state="disabled")
        self._progress.start(12)
        thread = threading.Thread(target=self._run_install, daemon=True)
        thread.start()

    def _run_install(self):
        installer = RimeTLPAInstaller(log_func=self._enqueue_log)
        success = False
        try:
            success = installer.install()
        except Exception as exc:
            self._enqueue_log(f"❌ 發生未預期的錯誤: {exc}")

        # 回到主執行緒更新 UI
        self.after(0, self._on_install_done, success)

    def _on_install_done(self, success: bool):
        self._progress.stop()
        self._progress.configure(value=0)
        self._install_btn.configure(state="normal")
        if success:
            messagebox.showinfo(
                "安裝完成",
                "RIME TLPA 閩南語輸入法已成功安裝！\n\n"
                "如 RIME 尚未自動重新部署，請右鍵點擊\n"
                "系統匣的小狼毫圖示，選擇「重新部署」。",
            )
        else:
            messagebox.showwarning(
                "安裝結束（含警告）",
                "安裝過程中有部分檔案未能複製。\n"
                "請查看記錄視窗中標示 ❌ 的項目。",
            )


def main():
    """主函式"""
    app = InstallerApp()
    app.mainloop()


if __name__ == "__main__":
    main()

