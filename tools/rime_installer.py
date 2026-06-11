#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RIME TLPA 專用安裝程式（圖形介面版）

安裝來源：使用者自 GitHub Release 下載之【輸入方案壓縮檔】（rime-tlpa-*.zip）。
本程式不再內嵌輸入方案檔；執行時會於下列位置尋找 .zip：
  1. 本程式（.exe）所在資料夾
  2. 使用者【下載 (Downloads)】資料夾
  3. 目前工作目錄
若找不到，提示使用者先行下載，或自行以檔案對話框指定。
default.custom.yaml（輸入法選單設定）仍隨 exe 內嵌提供。
"""

import queue
import shutil
import subprocess
import sys
import threading
import tkinter as tk
import zipfile
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

# 輸入方案壓縮檔檔名樣式（GitHub Release 產出，如 rime-tlpa-all-v0.1.0-alpha.zip）
SCHEME_ZIP_GLOB = "rime-tlpa-*.zip"
# 找不到壓縮檔時，提示使用者前往下載之網址
RELEASE_URL = "https://github.com/AlanJui/rime-tlpa/releases"


def get_exe_dir() -> Path:
    """取得執行檔（或開發時腳本）所在目錄——使用者通常會把下載的 zip 放這裡。"""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def get_bundle_dir() -> Path:
    """取得內嵌資源目錄（default.custom.yaml 所在）。

    打包後為 PyInstaller 解壓的暫存目錄（sys._MEIPASS）；
    開發環境則為專案根目錄（tools/ 之上一層）。
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent


def find_scheme_zips() -> list:
    """於 .exe 同資料夾、下載資料夾、目前工作目錄尋找輸入方案 zip（去重）。"""
    search_dirs = [
        get_exe_dir(),
        Path.home() / "Downloads",
        Path.cwd(),
    ]
    found = []
    seen = set()
    for directory in search_dirs:
        try:
            if not directory.exists():
                continue
            for zip_path in sorted(directory.glob(SCHEME_ZIP_GLOB)):
                resolved = zip_path.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    found.append(zip_path)
        except OSError:
            continue
    return found


class RimeTLPAInstaller:
    def __init__(self, zip_path=None, log_func=None):
        self._log = log_func or print
        self.zip_path = Path(zip_path) if zip_path else None
        self.bundle_dir = get_bundle_dir()
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

    def check_scheme_zip(self):
        """確認已指定且存在合法之輸入方案 zip 檔。"""
        if not self.zip_path or not self.zip_path.exists():
            self._log("❌ 錯誤: 找不到輸入方案 .zip 壓縮檔")
            self._log("   請先至下列網址下載輸入方案壓縮檔：")
            self._log(f"   {RELEASE_URL}")
            self._log("   下載後，將 .zip 檔放到本程式所在資料夾或【下載】資料夾，")
            self._log("   再重新執行；或點擊【瀏覽…】自行指定壓縮檔。")
            return False

        if not zipfile.is_zipfile(self.zip_path):
            self._log(f"❌ 錯誤: 「{self.zip_path.name}」不是有效的 zip 壓縮檔")
            return False

        self._log(f"📦 使用輸入方案壓縮檔: {self.zip_path.name}")
        return True

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

    def extract_scheme_zip(self):
        """將輸入方案 zip 解壓縮至 RIME 配置目錄（保留 lua/ 等子目錄結構）。"""
        self._log("📄 開始解壓並安裝輸入方案檔案...")

        copied_count = 0
        failed_files = []
        rime_root = self.rime_dir.resolve()

        with zipfile.ZipFile(self.zip_path) as zf:
            for info in zf.infolist():
                if info.is_dir():
                    continue

                # 將壓縮檔內路徑（可能含 / 或 \）正規化為相對路徑
                rel_name = info.filename.replace("\\", "/")
                dst_file = self.rime_dir / rel_name

                try:
                    # 防止 Zip Slip：目標路徑須落在 RIME 配置目錄之內
                    resolved = dst_file.resolve()
                    if rime_root != resolved and rime_root not in resolved.parents:
                        self._log(f"   ⚠️  略過可疑路徑: {info.filename}")
                        failed_files.append(info.filename)
                        continue

                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    with zf.open(info) as src, open(dst_file, "wb") as out:
                        shutil.copyfileobj(src, out)
                    self._log(f"   ✅ 已安裝: {rel_name}")
                    copied_count += 1
                except Exception as e:
                    self._log(f"   ❌ 安裝失敗: {rel_name} - {e}")
                    failed_files.append(info.filename)

        self._log(f"📊 安裝結果: 成功 {copied_count} 個，失敗 {len(failed_files)} 個")

        if failed_files:
            self._log("❌ 失敗的檔案:")
            for file_name in failed_files:
                self._log(f"   - {file_name}")

        return copied_count, failed_files

    def copy_default_custom(self):
        """複製內嵌之 default.custom.yaml（輸入法選單設定）。"""
        config_src = self.bundle_dir / "config" / "default.custom.yaml"

        if config_src.exists():
            dst_file = self.rime_dir / "default.custom.yaml"
            shutil.copy2(config_src, dst_file)
            self._log("✅ 已複製 default.custom.yaml (輸入法選單設定)")
            return True

        self._log("⚠️  找不到內嵌的 default.custom.yaml")
        return False

    def deploy_rime(self):
        """RIME 重新部署
         1. 部署程式檔名為： WeaselDeployer.exe
         2. 部署程式存放目錄路徑為： C:\Program Files\Rime\weasel-<version>\WeaselDeployer.exe
            如： C:\Program Files\Rime\weasel-0.17.4\WeaselDeployer.exe
         3. 執行參數為： /deploy
         4. 執行前需先切換到 RIME 配置目錄，確保部署程式執行時能讀取配置檔案： default.custom.yaml。
        """
        self._log("🔄 嘗試觸發 RIME 重新部署...")

        # 查找最新版本的 WeaselDeployer.exe
        # 作法：遍歷【子目錄】，尋找 weasel-* 最近版本資料夾，並檢查其中是否存在 WeaselDeployer.exe
        rime_install_roots = [
            Path("C:/Program Files/Rime"),
            Path("C:/Program Files (x86)/Rime"),
        ]

        deployer_path = None
        server_path = None
        for rime_root in rime_install_roots:
            if not rime_root.exists():
                continue
            version_dirs = sorted(
                [d for d in rime_root.iterdir() if d.is_dir() and d.name.startswith("weasel-")],
                key=lambda d: d.stat().st_mtime,
                reverse=True
            )
            if version_dirs:
                candidate = version_dirs[0] / "WeaselDeployer.exe"
                if candidate.exists():
                    deployer_path = candidate
                    server_path = version_dirs[0] / "WeaselServer.exe"
                    break

        if not deployer_path:
            self._log("⚠️  找不到 RIME 部署程式，請手動重新部署")
            return False

        # 1. 停止 WeaselServer
        try:
            subprocess.run(["taskkill", "/F", "/IM", "WeaselServer.exe"],
                           capture_output=True)
            self._log("🛑 已停止 WeaselServer")
        except Exception:
            pass

        # 2. 切換工作目錄至 Rime 使用者設定目錄後執行部署
        #    WeaselDeployer.exe 會檢查工作目錄是否含 default.custom.yaml；
        #    若工作目錄不正確，會開啟【輸入法設定】視窗而非執行部署。
        try:
            subprocess.run(
                [str(deployer_path), "/deploy"],
                check=True,
                cwd=str(self.rime_dir)
            )
            self._log("✅ RIME 重新部署成功")
        except subprocess.CalledProcessError:
            self._log("⚠️  自動部署失敗，請手動重新部署")
            return False

        # 3. 重啟 WeaselServer
        if server_path and server_path.exists():
            try:
                subprocess.Popen([str(server_path)])
                self._log("🚀 已重啟 WeaselServer")
            except Exception as e:
                self._log(f"⚠️  重啟 WeaselServer 失敗: {e}")

        return True

    def install(self):
        """執行完整安裝流程"""
        self._log("=" * 50)
        self._log("🚀 RIME TLPA 閩南語輸入法配置工具安裝程式")
        self._log("=" * 50)

        # 1. 檢查 RIME 安裝
        if not self.check_rime_installation():
            return False

        # 2. 檢查輸入方案壓縮檔（找不到則中止，提示使用者下載）
        if not self.check_scheme_zip():
            return False

        # 3. 備份現有配置
        self.backup_default_custom()

        # 4. 解壓並安裝輸入方案檔案
        copied_count, failed_files = self.extract_scheme_zip()

        # 5. 複製新的 default.custom.yaml（內嵌之輸入法選單設定）
        self.copy_default_custom()

        # 6. 嘗試重新部署
        self.deploy_rime()

        # 7. 顯示完成訊息
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
        self._scan_zips()
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
            text=(
                "請先下載輸入方案壓縮檔（rime-tlpa-*.zip），放到本程式所在資料夾"
                "或【下載】資料夾。選擇要安裝的壓縮檔後，點擊【開始安裝】，"
                "程式將解壓輸入方案並重新部署 RIME。"
            ),
            font=("Segoe UI", 10),
            bg=self.BG,
            fg=self.FG,
            wraplength=480,
            justify="left",
        ).pack(padx=PAD, pady=(PAD, 4), anchor="w")

        # ── 輸入方案壓縮檔選擇 ──────────────────────────
        zip_frame = tk.Frame(self, bg=self.BG)
        zip_frame.pack(padx=PAD, pady=(0, 8), fill="x")

        tk.Label(
            zip_frame,
            text="輸入方案壓縮檔：",
            font=("Segoe UI", 10),
            bg=self.BG,
            fg=self.FG,
        ).pack(side="left")

        self._zip_var = tk.StringVar()
        self._zip_combo = ttk.Combobox(
            zip_frame,
            textvariable=self._zip_var,
            state="readonly",
            width=42,
        )
        self._zip_combo.pack(side="left", padx=(4, 4))

        self._browse_btn = tk.Button(
            zip_frame,
            text=" 瀏覽… ",
            font=("Segoe UI", 10),
            bg="#313244",
            fg=self.FG,
            activebackground="#45475a",
            relief="flat",
            cursor="hand2",
            command=self._on_browse,
        )
        self._browse_btn.pack(side="left")

        # 偵測到的 zip 路徑清單（與 combobox 顯示項目一一對應）
        self._zip_paths = []

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

    # ── 輸入方案壓縮檔偵測／選擇 ──────────────────────────
    def _refresh_zip_combo(self, select_index=0):
        """以 self._zip_paths 更新下拉選單顯示。"""
        display = [f"{p.name}  —  {p.parent}" for p in self._zip_paths]
        self._zip_combo["values"] = display
        if display:
            self._zip_combo.current(min(select_index, len(display) - 1))

    def _scan_zips(self):
        """啟動時自動掃描可用的輸入方案壓縮檔。"""
        self._zip_paths = find_scheme_zips()
        self._refresh_zip_combo()
        if self._zip_paths:
            self._enqueue_log(f"📦 偵測到 {len(self._zip_paths)} 個輸入方案壓縮檔：")
            for p in self._zip_paths:
                self._enqueue_log(f"   - {p.name}（{p.parent}）")
            self._enqueue_log("請於上方下拉選單選擇要安裝的壓縮檔，再點擊【開始安裝】。")
        else:
            self._enqueue_log("⚠️  尚未偵測到輸入方案壓縮檔（rime-tlpa-*.zip）。")
            self._enqueue_log(f"   請先至 {RELEASE_URL} 下載，")
            self._enqueue_log("   放到本程式所在資料夾或【下載】資料夾；或點擊【瀏覽…】自行指定。")

    def _on_browse(self):
        """讓使用者自行選取壓縮檔。"""
        path = filedialog.askopenfilename(
            title="選擇輸入方案壓縮檔",
            filetypes=[("Zip 壓縮檔", "*.zip"), ("所有檔案", "*.*")],
        )
        if not path:
            return
        chosen = Path(path)
        # 避免重複加入
        existing = next((i for i, p in enumerate(self._zip_paths)
                         if p.resolve() == chosen.resolve()), None)
        if existing is None:
            self._zip_paths.append(chosen)
            self._refresh_zip_combo(select_index=len(self._zip_paths) - 1)
        else:
            self._zip_combo.current(existing)
        self._enqueue_log(f"📦 已選擇壓縮檔: {chosen.name}")

    def _current_zip(self):
        """取得目前選定的壓縮檔路徑（未選則回傳 None）。"""
        idx = self._zip_combo.current()
        if 0 <= idx < len(self._zip_paths):
            return self._zip_paths[idx]
        return None

    # ── 安裝流程 ────────────────────────────────────────
    def _start_install(self):
        zip_path = self._current_zip()
        if zip_path is None:
            messagebox.showerror(
                "尚未選擇輸入方案壓縮檔",
                "找不到可安裝的輸入方案壓縮檔（rime-tlpa-*.zip）。\n\n"
                f"請先至下列網址下載：\n{RELEASE_URL}\n\n"
                "下載後放到本程式所在資料夾或【下載】資料夾，\n"
                "或點擊【瀏覽…】自行指定壓縮檔。",
            )
            return
        self._install_btn.configure(state="disabled")
        self._browse_btn.configure(state="disabled")
        self._progress.start(12)
        thread = threading.Thread(
            target=self._run_install, args=(zip_path,), daemon=True
        )
        thread.start()

    def _run_install(self, zip_path):
        installer = RimeTLPAInstaller(zip_path=zip_path, log_func=self._enqueue_log)
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
        self._browse_btn.configure(state="normal")
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

